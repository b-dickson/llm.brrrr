"""
Code Generator — Forge Your Creation
=====================================
Emits OLMo-core v2.5.0+ compatible model configs and training scripts.

Targets the post-SequenceMixer API surface introduced around 2.5.0:

* ``TransformerBlockConfig(sequence_mixer=…)`` instead of ``attention=…``
* ``AttentionConfig(name=AttentionType.default/fused/normalized, rope=RoPEConfig(…))``
  — RoPE lives *inside* the AttentionConfig now.
* ``AttentionConfig.qk_norm`` is a ``LayerNormConfig`` (or ``None``), not a bool.
* ``AttentionConfig.backend`` takes ``AttentionBackendName`` (a ``StrEnum``).
* ``GatedDeltaNetConfig`` from ``olmo_core.nn.attention.recurrent`` is a native
  ``SequenceMixerConfig`` — no FLA wrapper, no extra block class needed.
* Hybrid models lean on ``TransformerConfig.block`` as a ``dict`` plus
  ``block_pattern`` (a list of keys) for clean per-layer mixing.
* MoE blocks set ``feed_forward_moe=MoEConfig(…)`` with
  ``router=MoERouterConfig(top_k=…, gating_function=…)``.
* ``LayerNormConfig(name=LayerNormType.{rms,fused_rms,l2_norm,default})`` is the
  one true norm config — there are no separate ``RMSNormConfig`` classes.

The TUI itself never imports olmo-core; we only emit *strings* of Python that
the user runs separately. That keeps ``uv sync`` instant.

    "I used to roll my own configs like you, then I took an OLMo-core import
    to the knee."
"""

from __future__ import annotations

from datetime import datetime
from textwrap import dedent

from .config import (
    AttentionBackend,
    AttentionType,
    BlockType,
    MLPType,
    ModelConfig,
    MoEGatingFunction,
    NormType,
    Optimizer,
    PositionEncoding,
    RoPEScaling,
    SequenceModelType,
)


# ---------------------------------------------------------------------------
# String mapping helpers
# ---------------------------------------------------------------------------

_ATTENTION_TYPE_NAME = {
    AttentionType.DEFAULT: "AttentionType.default",
    AttentionType.FUSED: "AttentionType.fused",
    AttentionType.NORMALIZED: "AttentionType.normalized",
}

_ATTENTION_BACKEND_NAME = {
    AttentionBackend.TORCH: "AttentionBackendName.torch",
    AttentionBackend.FLASH_2: "AttentionBackendName.flash_2",
    AttentionBackend.FLASH_3: "AttentionBackendName.flash_3",
    AttentionBackend.FLASH_4: "AttentionBackendName.flash_4",
    AttentionBackend.TRANSFORMER_ENGINE: "AttentionBackendName.te",
}

_BLOCK_TYPE_NAME = {
    BlockType.PRE_NORM: "TransformerBlockType.default",
    BlockType.REORDERED: "TransformerBlockType.reordered_norm",
    BlockType.PERI_NORM: "TransformerBlockType.peri_norm",
    BlockType.NORMALIZED: "TransformerBlockType.normalized",
    BlockType.MOE: "TransformerBlockType.moe",
    BlockType.MOE_REORDERED: "TransformerBlockType.moe_reordered_norm",
    BlockType.MOE_HYBRID: "TransformerBlockType.moe_hybrid",
}

_LAYER_NORM_NAME = {
    NormType.LAYER_NORM: "LayerNormType.default",
    NormType.RMS_NORM: "LayerNormType.rms",
    NormType.FUSED_RMS_NORM: "LayerNormType.fused_rms",
    NormType.L2_NORM: "LayerNormType.l2_norm",
}

_ROPE_TYPE_NAME = {
    PositionEncoding.ROPE: "RoPEType.default",
    PositionEncoding.FUSED_ROPE: "RoPEType.fused",
    PositionEncoding.COMPLEX_ROPE: "RoPEType.complex",
}

_ROPE_SCALING_BUILDER = {
    RoPEScaling.NONE: None,
    RoPEScaling.ABF: "ABFRoPEScalingConfig()",
    RoPEScaling.PI: "PIRoPEScalingConfig(factor=2.0)",
    RoPEScaling.LLAMA3: "StepwiseRoPEScalingConfig()",
    RoPEScaling.YARN: "YaRNRoPEScalingConfig()",
}


def _safe_filename(name: str) -> str:
    """Sanitize a model name into a usable file/identifier stem."""
    # Strip everything that isn't safe for filenames or Python identifiers,
    # collapse runs of underscores, and lowercase. Falls back to ``model``
    # if the user gave us an empty string.
    cleaned = []
    for ch in name.lower():
        if ch.isalnum():
            cleaned.append(ch)
        elif ch in (" ", "-", "_", "."):
            cleaned.append("_")
    stem = "".join(cleaned).strip("_")
    while "__" in stem:
        stem = stem.replace("__", "_")
    return stem or "model"


def _ensure_multiple_of(value: int, multiple: int = 256) -> int:
    return ((value + multiple - 1) // multiple) * multiple


def _hidden_size_for(config: ModelConfig) -> int:
    """Pick a sensible feed-forward hidden size for the model."""
    if config.mlp_type == MLPType.SWIGLU:
        # Llama-style: 8/3 * d_model, rounded up to a clean multiple.
        target = int(config.n_embd * (config.mlp_ratio if config.mlp_ratio else 8 / 3))
        return _ensure_multiple_of(target, 256)
    return int(config.n_embd * config.mlp_ratio)


# ---------------------------------------------------------------------------
# Snippet builders (Python code as strings)
# ---------------------------------------------------------------------------

def _rope_snippet(config: ModelConfig, indent: str) -> str:
    """Build a ``rope=RoPEConfig(...)`` argument for AttentionConfig."""
    if config.position_encoding not in _ROPE_TYPE_NAME:
        return ""

    rope_type = _ROPE_TYPE_NAME[config.position_encoding]
    scaling_expr = _ROPE_SCALING_BUILDER.get(config.rope_scaling)
    scaling_line = f"\n{indent}    scaling={scaling_expr}," if scaling_expr else ""
    return (
        f"\n{indent}rope=RoPEConfig(\n"
        f"{indent}    name={rope_type},\n"
        f"{indent}    theta={int(config.rope_theta)},{scaling_line}\n"
        f"{indent}),"
    )


def _attention_config_block(config: ModelConfig, base_indent: str) -> str:
    """Render an ``AttentionConfig(...)`` expression.

    ``base_indent`` is the indentation of the line containing the opening
    paren ``AttentionConfig(``. Inner fields get one extra level (4 spaces);
    the closing paren sits back at ``base_indent``.
    """
    inner = base_indent + "    "
    name = _ATTENTION_TYPE_NAME.get(config.attention_type, "AttentionType.default")
    backend = _ATTENTION_BACKEND_NAME.get(config.attention_backend)
    rope = _rope_snippet(config, inner)
    qk_norm_line = (
        f"\n{inner}qk_norm=LayerNormConfig(name=LayerNormType.rms),"
        if config.qk_norm
        else ""
    )
    backend_line = f"\n{inner}backend={backend}," if backend else ""

    n_kv_heads_line = ""
    if config.n_kv_heads and config.n_kv_heads != config.n_heads:
        n_kv_heads_line = f"\n{inner}n_kv_heads={config.n_kv_heads},"

    bias_line = "" if config.attention_bias else f"\n{inner}bias=False,"

    return (
        f"AttentionConfig(\n"
        f"{inner}name={name},\n"
        f"{inner}n_heads={config.n_heads},{n_kv_heads_line}"
        f"{bias_line}"
        f"{qk_norm_line}"
        f"{rope}"
        f"{backend_line}\n"
        f"{base_indent})"
    )


def _gdn_config_block(config: ModelConfig, base_indent: str) -> str:
    """Render a ``GatedDeltaNetConfig(...)`` expression."""
    inner = base_indent + "    "
    n_v_heads_line = (
        f"\n{inner}n_v_heads={config.gdn_n_v_heads},"
        if config.gdn_n_v_heads
        else ""
    )
    return (
        f"GatedDeltaNetConfig(\n"
        f"{inner}n_heads={config.n_heads},{n_v_heads_line}\n"
        f"{inner}expand_v={float(config.gdn_expand_v)},\n"
        f"{inner}allow_neg_eigval={config.gdn_allow_neg_eigval},\n"
        f"{inner}conv_size={config.gdn_conv_size},\n"
        f"{base_indent})"
    )


def _moe_config_block(config: ModelConfig, hidden_size: int, base_indent: str) -> str:
    """Render a ``MoEConfig(...)`` for use as ``feed_forward_moe``."""
    inner = base_indent + "    "
    gating = (
        "MoERouterGatingFunction.softmax"
        if config.moe_gating == MoEGatingFunction.SOFTMAX
        else "MoERouterGatingFunction.sigmoid"
    )
    shared_line = ""
    if config.moe_shared_mlp:
        shared_line = (
            f"\n{inner}shared_mlp=FeedForwardConfig(\n"
            f"{inner}    hidden_size={hidden_size},\n"
            f"{inner}    bias=False,\n"
            f"{inner}),"
        )
    lb_line = (
        f"\n{inner}lb_loss_weight={config.moe_lb_weight},"
        if config.moe_load_balancing
        else f"\n{inner}lb_loss_weight=None,"
    )
    return (
        f"MoEConfig(\n"
        f"{inner}num_experts={config.num_experts},\n"
        f"{inner}hidden_size={hidden_size},\n"
        f"{inner}router=MoERouterConfig(\n"
        f"{inner}    top_k={config.experts_per_token},\n"
        f"{inner}    gating_function={gating},\n"
        f"{inner}),"
        f"{shared_line}"
        f"{lb_line}\n"
        f"{inner}z_loss_weight={config.moe_z_loss_weight},\n"
        f"{base_indent})"
    )


def _imports_for(config: ModelConfig, *, hybrid: bool = False) -> str:
    """Build the import block at the top of a generated config file."""
    pure_gdn = (
        config.sequence_model == SequenceModelType.GATED_DELTANET or config.is_mamba
    ) and not hybrid

    imports: list[str] = ["from olmo_core.config import DType"]

    if not pure_gdn:
        imports.append(
            "from olmo_core.nn.attention import (\n"
            "    AttentionBackendName,\n"
            "    AttentionConfig,\n"
            "    AttentionType,\n"
            ")"
        )

    # We deliberately do NOT import ``ActivationFunction``: it was added to
    # ``feed_forward`` in olmo-core 2.5.0, but the default of SiLU/SwiGLU
    # already covers every preset. Omitting both the import and the
    # ``activation=…`` field keeps generated configs runnable against
    # PyPI's older 2.4.0 release as well as the newer 2.5.0 GitHub source.
    imports.extend(
        [
            "from olmo_core.nn.feed_forward import FeedForwardConfig, FeedForwardType",
            "from olmo_core.nn.layer_norm import LayerNormConfig, LayerNormType",
            "from olmo_core.nn.lm_head import LMHeadConfig, LMHeadType",
            "from olmo_core.nn.transformer import (\n"
            "    TransformerBlockConfig,\n"
            "    TransformerBlockType,\n"
            "    TransformerConfig,\n"
            "    TransformerType,\n"
            ")",
        ]
    )

    if not pure_gdn and config.position_encoding in _ROPE_TYPE_NAME:
        imports.append("from olmo_core.nn.rope import RoPEConfig, RoPEType")
        scaling_classes: list[str] = []
        if config.rope_scaling == RoPEScaling.ABF:
            scaling_classes.append("ABFRoPEScalingConfig")
        elif config.rope_scaling == RoPEScaling.PI:
            scaling_classes.append("PIRoPEScalingConfig")
        elif config.rope_scaling == RoPEScaling.LLAMA3:
            scaling_classes.append("StepwiseRoPEScalingConfig")
        elif config.rope_scaling == RoPEScaling.YARN:
            scaling_classes.append("YaRNRoPEScalingConfig")
        if scaling_classes:
            imports.append(
                "from olmo_core.nn.rope import " + ", ".join(scaling_classes)
            )

    if (
        config.sequence_model == SequenceModelType.GATED_DELTANET
        or config.is_hybrid
        or config.is_mamba
    ):
        imports.append(
            "from olmo_core.nn.attention.recurrent import GatedDeltaNetConfig"
        )

    if config.is_moe:
        imports.append(
            "from olmo_core.nn.moe import (\n"
            "    MoEConfig,\n"
            "    MoERouterConfig,\n"
            "    MoERouterGatingFunction,\n"
            ")"
        )

    return "\n".join(imports)


# ---------------------------------------------------------------------------
# Top-level config emitters
# ---------------------------------------------------------------------------

def _file_header(config: ModelConfig, subtitle: str) -> str:
    return (
        f'"""\n'
        f"{config.name} — {subtitle}\n"
        f"{'=' * (len(config.name) + len(subtitle) + 3)}\n\n"
        f"Race        : {config.race}\n"
        f"Parameters  : ~{config.param_str()}\n"
        f"Memory      : {config.memory_str('bf16')} (bf16)\n"
        f"Architecture: {config.get_architecture_summary()}\n\n"
        f"Generated by The Elder Models V: LLMRIM\n"
        f'"Fus Ro Brrr… your training begins."\n'
        f'"""\n\n'
    )


def generate_olmo_config(config: ModelConfig) -> str:
    """Generate a standard transformer config (Attention + FFN)."""
    stem = _safe_filename(config.name)
    builder = f"build_{stem}_config"
    hidden_size = _hidden_size_for(config)
    base = "        "  # indentation for fields of TransformerBlockConfig

    transformer_type = (
        "TransformerType.normalized"
        if config.block_type == BlockType.NORMALIZED
        else "TransformerType.moe"
        if config.is_moe
        else "TransformerType.default"
    )
    block_name = _BLOCK_TYPE_NAME.get(config.block_type, "TransformerBlockType.default")
    norm_name = _LAYER_NORM_NAME.get(config.norm_type, "LayerNormType.rms")

    sequence_mixer = _attention_config_block(config, base)

    feed_forward = ""
    feed_forward_moe = ""
    if config.is_moe:
        moe_block = _moe_config_block(config, hidden_size, base)
        feed_forward_moe = f"\n{base}feed_forward_moe={moe_block},"
    else:
        ff_type = (
            "FeedForwardType.normalized"
            if config.block_type == BlockType.NORMALIZED
            else "FeedForwardType.default"
        )
        bias_line = "" if config.mlp_bias else f"\n{base}    bias=False,"
        feed_forward = (
            f"\n{base}feed_forward=FeedForwardConfig(\n"
            f"{base}    name={ff_type},\n"
            f"{base}    hidden_size={hidden_size},"
            f"{bias_line}\n"
            f"{base}),"
        )

    return (
        _file_header(config, "OLMo-core Transformer Config")
        + _imports_for(config)
        + "\n\n\n"
        + f"def {builder}() -> TransformerConfig:\n"
        f'    """Build the {config.name} model configuration."""\n'
        f"    layer_norm = LayerNormConfig(name={norm_name}, eps=1e-5, bias=False)\n"
        f"\n"
        f"    block = TransformerBlockConfig(\n"
        f"{base}name={block_name},\n"
        f"{base}sequence_mixer={sequence_mixer},"
        f"{feed_forward}{feed_forward_moe}\n"
        f"{base}layer_norm=layer_norm,\n"
        f"    )\n"
        f"\n"
        f"    return TransformerConfig(\n"
        f"        name={transformer_type},\n"
        f"        d_model={config.n_embd},\n"
        f"        n_layers={config.n_layers},\n"
        f"        vocab_size={config.vocab_size},\n"
        f"        block=block,\n"
        f"        lm_head=LMHeadConfig(\n"
        f"            name=LMHeadType.default,\n"
        f"            layer_norm=layer_norm,\n"
        f"            bias=False,\n"
        f"        ),\n"
        f"        dtype=DType.bfloat16,\n"
        f"        init_seed=42,\n"
        f"    )\n"
        f"\n\n"
        f"if __name__ == \"__main__\":\n"
        f"    cfg = {builder}()\n"
        f"    model = cfg.build(init_device=\"meta\")\n"
        f"    print(f\"{config.name}: {{cfg.num_params:,}} params \"\n"
        f"          f\"({{cfg.num_active_params:,}} active)\")\n"
    )


def generate_gdn_config(config: ModelConfig) -> str:
    """Generate a pure GatedDeltaNet config (linear attention only)."""
    stem = _safe_filename(config.name)
    builder = f"build_{stem}_config"
    hidden_size = _hidden_size_for(config)
    base = "        "
    sequence_mixer = _gdn_config_block(config, base)
    norm_name = _LAYER_NORM_NAME.get(config.norm_type, "LayerNormType.rms")

    return (
        _file_header(config, "OLMo-core GatedDeltaNet Config")
        + _imports_for(config)
        + "\n\n\n"
        + f"def {builder}() -> TransformerConfig:\n"
        f'    """Build the {config.name} GatedDeltaNet model.\n'
        f"\n"
        f"    GatedDeltaNet is a native ``SequenceMixerConfig`` in olmo-core,\n"
        f"    so it slots straight into ``TransformerBlockConfig.sequence_mixer``\n"
        f"    with no FLA wrapper. The recurrent state is constant-size in the\n"
        f"    sequence length — long contexts cost no extra memory.\n"
        f'    """\n'
        f"    layer_norm = LayerNormConfig(name={norm_name}, eps=1e-5, bias=False)\n"
        f"\n"
        f"    block = TransformerBlockConfig(\n"
        f"        name=TransformerBlockType.default,\n"
        f"        sequence_mixer={sequence_mixer},\n"
        f"        feed_forward=FeedForwardConfig(\n"
        f"            name=FeedForwardType.default,\n"
        f"            hidden_size={hidden_size},\n"
        f"            bias=False,\n"
        f"        ),\n"
        f"        layer_norm=layer_norm,\n"
        f"    )\n"
        f"\n"
        f"    return TransformerConfig(\n"
        f"        name=TransformerType.default,\n"
        f"        d_model={config.n_embd},\n"
        f"        n_layers={config.n_layers},\n"
        f"        vocab_size={config.vocab_size},\n"
        f"        block=block,\n"
        f"        lm_head=LMHeadConfig(\n"
        f"            name=LMHeadType.default,\n"
        f"            layer_norm=layer_norm,\n"
        f"            bias=False,\n"
        f"        ),\n"
        f"        dtype=DType.bfloat16,\n"
        f"        init_seed=42,\n"
        f"    )\n"
        f"\n\n"
        f"if __name__ == \"__main__\":\n"
        f"    cfg = {builder}()\n"
        f"    model = cfg.build(init_device=\"meta\")\n"
        f"    print(f\"{config.name}: {{cfg.num_params:,}} params\")\n"
        f"    print(\"GatedDeltaNet uses constant-size recurrent state — \"\n"
        f"          \"context length costs no memory.\")\n"
    )


def generate_hybrid_config(config: ModelConfig) -> str:
    """Generate a hybrid Attention + GatedDeltaNet config.

    Uses ``TransformerConfig.block`` as a dict + ``block_pattern`` so each
    layer index is mapped to either the attention block or the GDN block.
    """
    stem = _safe_filename(config.name)
    builder = f"build_{stem}_config"
    hidden_size = _hidden_size_for(config)
    norm_name = _LAYER_NORM_NAME.get(config.norm_type, "LayerNormType.rms")

    fla_layers = sorted(set(config.fla_layers or list(range(0, config.n_layers, 2))))
    layer_keys = [
        '"gdn"' if i in fla_layers else '"attn"' for i in range(config.n_layers)
    ]
    # Wrap the pattern list — six entries per line keeps it readable for any
    # plausible model depth without becoming a wall of text.
    pattern_lines = []
    for start in range(0, len(layer_keys), 6):
        chunk = ", ".join(layer_keys[start : start + 6])
        pattern_lines.append(f"            {chunk},")
    pattern = "\n".join(pattern_lines)

    attention_mixer = _attention_config_block(config, "        ")
    gdn_mixer = _gdn_config_block(config, "        ")

    return (
        _file_header(config, "OLMo-core Hybrid (Attention + GatedDeltaNet)")
        + _imports_for(config, hybrid=True)
        + "\n\n\n"
        + f"def {builder}() -> TransformerConfig:\n"
        f'    """Build the {config.name} hybrid model.\n'
        f"\n"
        f"    Each layer is either a softmax attention block or a GatedDeltaNet\n"
        f"    block, dictated by ``block_pattern``. Both share the same FFN and\n"
        f"    layer norm — only the sequence mixer changes.\n"
        f'    """\n'
        f"    layer_norm = LayerNormConfig(name={norm_name}, eps=1e-5, bias=False)\n"
        f"    feed_forward = FeedForwardConfig(\n"
        f"        name=FeedForwardType.default,\n"
        f"        hidden_size={hidden_size},\n"
        f"        bias=False,\n"
        f"    )\n"
        f"\n"
        f"    attention_block = TransformerBlockConfig(\n"
        f"        name=TransformerBlockType.default,\n"
        f"        sequence_mixer={attention_mixer},\n"
        f"        feed_forward=feed_forward,\n"
        f"        layer_norm=layer_norm,\n"
        f"    )\n"
        f"\n"
        f"    gdn_block = TransformerBlockConfig(\n"
        f"        name=TransformerBlockType.default,\n"
        f"        sequence_mixer={gdn_mixer},\n"
        f"        feed_forward=feed_forward,\n"
        f"        layer_norm=layer_norm,\n"
        f"    )\n"
        f"\n"
        f"    return TransformerConfig(\n"
        f"        name=TransformerType.default,\n"
        f"        d_model={config.n_embd},\n"
        f"        n_layers={config.n_layers},\n"
        f"        vocab_size={config.vocab_size},\n"
        f'        block={{"attn": attention_block, "gdn": gdn_block}},\n'
        f"        block_pattern=[\n{pattern}\n        ],\n"
        f"        lm_head=LMHeadConfig(\n"
        f"            name=LMHeadType.default,\n"
        f"            layer_norm=layer_norm,\n"
        f"            bias=False,\n"
        f"        ),\n"
        f"        dtype=DType.bfloat16,\n"
        f"        init_seed=42,\n"
        f"    )\n"
        f"\n\n"
        f"if __name__ == \"__main__\":\n"
        f"    cfg = {builder}()\n"
        f"    model = cfg.build(init_device=\"meta\")\n"
        f"    print(f\"{config.name}: {{cfg.num_params:,}} params\")\n"
        f"    print(f\"layout = {{cfg.block_pattern}}\")\n"
    )


def generate_model_code(config: ModelConfig) -> str:
    """Dispatch to the appropriate generator for this config."""
    if config.is_hybrid:
        return generate_hybrid_config(config)
    if (
        config.sequence_model == SequenceModelType.GATED_DELTANET
        or config.is_mamba  # mamba presets re-route to GDN under v2.5.0
    ):
        return generate_gdn_config(config)
    return generate_olmo_config(config)


# ---------------------------------------------------------------------------
# Training script
# ---------------------------------------------------------------------------

def generate_training_script(config: ModelConfig) -> str:
    """Generate a minimal but functional training script using olmo-core."""
    stem = _safe_filename(config.name)
    builder = f"build_{stem}_config"

    optim_class = (
        "AdamWConfig" if config.optimizer == Optimizer.ADAMW else "SkipStepAdamWConfig"
    )

    return (
        f'"""\n'
        f"{config.name} — Training Script\n"
        f"{'=' * (len(config.name) + 20)}\n\n"
        f"Generated by The Elder Models V: LLMRIM. Edit DATA_PATHS, run name and\n"
        f"hyperparameters before launching with torchrun.\n"
        f"\n"
        f"    torchrun --nproc-per-node=8 {stem}_train.py\n"
        f'"""\n'
        f"\n"
        f"from __future__ import annotations\n"
        f"\n"
        f"from olmo_core.config import DType\n"
        f"from olmo_core.data import (\n"
        f"    NumpyDataLoaderConfig,\n"
        f"    NumpyFSLDatasetConfig,\n"
        f"    TokenizerConfig,\n"
        f")\n"
        f"from olmo_core.distributed.parallel import DataParallelType\n"
        f"from olmo_core.optim import {optim_class}, CosWithWarmup, OptimGroupOverride\n"
        f"from olmo_core.train import (\n"
        f"    Duration,\n"
        f"    TrainerConfig,\n"
        f"    prepare_training_environment,\n"
        f"    teardown_training_environment,\n"
        f")\n"
        f"from olmo_core.train.callbacks import (\n"
        f"    CheckpointerCallback,\n"
        f"    GPUMemoryMonitorCallback,\n"
        f")\n"
        f"from olmo_core.train.train_module import (\n"
        f"    TransformerDataParallelConfig,\n"
        f"    TransformerTrainModuleConfig,\n"
        f")\n"
        f"\n"
        f"from {stem}_config import {builder}\n"
        f"\n"
        f"\n"
        f"RUN_NAME = \"{stem}\"\n"
        f"SAVE_FOLDER = f\"./checkpoints/{{RUN_NAME}}\"\n"
        f"SEQUENCE_LENGTH = {config.seq_length}\n"
        f"GLOBAL_BATCH_SIZE = 256 * 1024  # tokens, not instances\n"
        f"DATA_PATHS = [\n"
        f"    # Replace with your tokenized .npy shards.\n"
        f"    \"./data/train.npy\",\n"
        f"]\n"
        f"\n"
        f"\n"
        f"def main() -> None:\n"
        f"    prepare_training_environment()\n"
        f"\n"
        f"    tokenizer = TokenizerConfig.gpt2()\n"
        f"    model_config = {builder}()\n"
        f"    model = model_config.build(init_device=\"meta\")\n"
        f"\n"
        f"    train_module_config = TransformerTrainModuleConfig(\n"
        f"        rank_microbatch_size=16 * 1024,\n"
        f"        max_sequence_length=SEQUENCE_LENGTH,\n"
        f"        optim={optim_class}(\n"
        f"            lr={config.learning_rate},\n"
        f"            weight_decay={config.weight_decay},\n"
        f"            betas=({config.beta1}, {config.beta2}),\n"
        f"            group_overrides=[\n"
        f"                OptimGroupOverride(\n"
        f"                    params=[\"embeddings.weight\"],\n"
        f"                    opts=dict(weight_decay=0.0),\n"
        f"                ),\n"
        f"            ],\n"
        f"        ),\n"
        f"        compile_model=True,\n"
        f"        dp_config=TransformerDataParallelConfig(\n"
        f"            name=DataParallelType.fsdp,\n"
        f"            param_dtype=DType.bfloat16,\n"
        f"            reduce_dtype=DType.float32,\n"
        f"        ),\n"
        f"        max_grad_norm=1.0,\n"
        f"        scheduler=CosWithWarmup(warmup_steps=2000),\n"
        f"    )\n"
        f"    train_module = train_module_config.build(model)\n"
        f"\n"
        f"    dataset = NumpyFSLDatasetConfig(\n"
        f"        paths=DATA_PATHS,\n"
        f"        sequence_length=SEQUENCE_LENGTH,\n"
        f"        tokenizer=tokenizer,\n"
        f"        work_dir=\"./.cache\",\n"
        f"    ).build()\n"
        f"    data_loader = NumpyDataLoaderConfig(\n"
        f"        global_batch_size=GLOBAL_BATCH_SIZE,\n"
        f"        seed=0,\n"
        f"        num_workers=4,\n"
        f"    ).build(dataset, dp_process_group=train_module.dp_process_group)\n"
        f"\n"
        f"    trainer = (\n"
        f"        TrainerConfig(\n"
        f"            save_folder=SAVE_FOLDER,\n"
        f"            save_overwrite=True,\n"
        f"            metrics_collect_interval=10,\n"
        f"            cancel_check_interval=5,\n"
        f"            max_duration=Duration.epochs(1),\n"
        f"        )\n"
        f"        .with_callback(\"gpu_monitor\", GPUMemoryMonitorCallback())\n"
        f"        .with_callback(\n"
        f"            \"checkpointer\",\n"
        f"            CheckpointerCallback(\n"
        f"                save_interval=1000,\n"
        f"                ephemeral_save_interval=100,\n"
        f"                save_async=True,\n"
        f"            ),\n"
        f"        )\n"
        f"        .build(train_module, data_loader)\n"
        f"    )\n"
        f"\n"
        f"    trainer.fit()\n"
        f"    teardown_training_environment()\n"
        f"\n"
        f"\n"
        f"if __name__ == \"__main__\":\n"
        f"    main()\n"
    )


# ---------------------------------------------------------------------------
# Full package (config + train + README)
# ---------------------------------------------------------------------------

def _readme_for(config: ModelConfig) -> str:
    """Generate a README markdown file for the model package."""
    stem = _safe_filename(config.name)

    if config.sequence_model == SequenceModelType.GATED_DELTANET:
        mixer = "GatedDeltaNet (native SequenceMixer, O(n) linear attention)"
    elif config.is_mamba:
        mixer = "Mamba/SSM preset → emitted as GatedDeltaNet (the closest native olmo-core sequence mixer)"
    elif config.is_hybrid:
        gdn = len(config.fla_layers or [])
        mixer = f"Hybrid: {gdn} GatedDeltaNet + {config.n_layers - gdn} Attention"
    else:
        mixer = f"{config.attention_type.name.title()} attention"

    moe_section = ""
    if config.is_moe:
        moe_section = dedent(
            f"""
            ## Mixture of Experts

            | Setting | Value |
            |---|---|
            | Experts | {config.num_experts} |
            | Top-k | {config.experts_per_token} |
            | Gating | {config.moe_gating.value} |
            | LB loss | {config.moe_lb_weight} |
            | Z loss  | {config.moe_z_loss_weight} |
            | Shared MLP | {config.moe_shared_mlp} |
            """
        ).strip("\n")

    return dedent(
        f"""
        # {config.name}

        > Generated by **The Elder Models V: LLMRIM** on
        > {datetime.now().strftime("%Y-%m-%d %H:%M")}.

        | Field | Value |
        |---|---|
        | Race | {config.race} |
        | Parameters | ~{config.param_str()} |
        | Memory (bf16) | {config.memory_str("bf16")} |
        | Sequence mixer | {mixer} |
        | MLP | {config.mlp_type.name} |
        | Norm | {config.norm_type.name} |
        | Position | {config.position_encoding.name} |
        | Context length | {config.seq_length:,} |
        | Vocabulary | {config.vocab_size:,} |
        | d_model × layers | {config.n_embd} × {config.n_layers} |
        | Heads / KV heads | {config.n_heads} / {config.kv_heads} |

        {moe_section}

        ## Build the model

        ```python
        from {stem}_config import build_{stem}_config

        cfg = build_{stem}_config()
        model = cfg.build(init_device="meta")
        print(f"{{cfg.num_params:,}} parameters")
        ```

        ## Train

        ```bash
        torchrun --nproc-per-node=8 {stem}_train.py
        ```

        Edit ``DATA_PATHS`` and ``GLOBAL_BATCH_SIZE`` in ``{stem}_train.py`` first.

        ## Requirements

        * Python ≥ 3.10
        * `ai2-olmo-core ≥ 2.5.0` (native `GatedDeltaNetConfig` lives there)
        * `flash-attn` if you want a Flash backend
        * `flash-linear-attention` if you use GatedDeltaNet (it powers the kernels)

        ---

        *"It is in the determination of one's destiny that the true nature of
        architecture is revealed."*
        """
    ).strip() + "\n"


def generate_full_package(config: ModelConfig) -> dict[str, str]:
    """Return a {filename: contents} mapping for a complete model package."""
    stem = _safe_filename(config.name)
    return {
        f"{stem}_config.py": generate_model_code(config),
        f"{stem}_train.py": generate_training_script(config),
        "README.md": _readme_for(config),
    }
