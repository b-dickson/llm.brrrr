"""
ModelConfig - The Dragonborn's Build
Configuration dataclass for LLM architectures with OLMo-core integration.

Supports transformer, Mamba, MoE, and hybrid architectures.
"""

from dataclasses import dataclass, field
from typing import Optional, List
from enum import Enum
from copy import deepcopy


# =============================================================================
# Architecture Enums
# =============================================================================

class SequenceModelType(Enum):
    """Core sequence modeling approach."""
    TRANSFORMER = "transformer"       # Standard attention-based
    MAMBA = "mamba"                   # Mamba SSM
    MAMBA2 = "mamba2"                 # Mamba2 (improved)
    GATED_DELTANET = "gated_deltanet" # GatedDeltaNet linear attention
    HYBRID = "hybrid"                 # Alternating attention + FLA blocks


class AttentionType(Enum):
    """Attention mechanism variants (for transformer/hybrid modes)."""
    DEFAULT = "Attention"             # OLMo default with GQA support
    FUSED = "FusedAttention"          # Flash-attention optimized
    NORMALIZED = "NormalizedAttention" # nGPT-style normalized


class AttentionBackend(Enum):
    """Attention computation backend."""
    TORCH = "torch"                   # PyTorch SDPA
    FLASH_2 = "flash_2"               # Flash Attention 2
    FLASH_3 = "flash_3"               # Flash Attention 3 (H100+)
    FLASH_4 = "flash_4"               # Flash Attention 4 CUTE
    TRANSFORMER_ENGINE = "te"          # NVIDIA TransformerEngine


class MLPType(Enum):
    """MLP/FFN variants."""
    STANDARD = "FeedForward"          # Standard with GELU
    SWIGLU = "SwiGLU"                 # Gated with SiLU (LLaMA-style)


class BlockType(Enum):
    """Transformer block normalization order."""
    PRE_NORM = "TransformerBlock"                    # Standard LLaMA-style
    REORDERED = "ReorderedNormTransformerBlock"      # Norm on attention output
    PERI_NORM = "PeriNormTransformerBlock"           # 6 layer norms
    NORMALIZED = "NormalizedTransformerBlock"        # nGPT architecture
    MOE = "MoETransformerBlock"                      # MoE variant
    MOE_REORDERED = "MoEReorderedNormTransformerBlock"
    MOE_HYBRID = "MoEHybridTransformerBlock"         # Dense + sparse


class NormType(Enum):
    """Normalization layer type."""
    LAYER_NORM = "LayerNorm"
    RMS_NORM = "RMSNorm"
    FUSED_RMS_NORM = "FusedRMSNorm"
    L2_NORM = "L2Norm"                # For nGPT


class PositionEncoding(Enum):
    """Positional encoding type.

    olmo-core 2.5.0 has no learned-positional-embedding implementation, so
    we don't expose one — every transformer-style model uses some flavor of
    RoPE, and recurrent mixers (Mamba, GatedDeltaNet) use NONE.
    """
    ROPE = "rope"
    FUSED_ROPE = "fused_rope"         # OLMo fused RoPE
    COMPLEX_ROPE = "complex_rope"     # Complex number RoPE
    NONE = "none"


class RoPEScaling(Enum):
    """RoPE scaling strategy for long context."""
    NONE = "none"
    ABF = "abf"                       # Absolute Base Frequency
    PI = "pi"                         # Position Interpolation
    LLAMA3 = "llama3"                 # LLaMA-3.1 stepwise
    YARN = "yarn"                     # YaRN scaling


class Optimizer(Enum):
    """Optimizer type."""
    ADAMW = "AdamW"
    MUON = "Muon"


class MoERouterType(Enum):
    """MoE routing mechanism."""
    LINEAR = "MoELinearRouter"        # Simple linear projection
    # Future: could add more sophisticated routers


class MoEGatingFunction(Enum):
    """MoE gating activation."""
    SOFTMAX = "softmax"
    SIGMOID = "sigmoid"


# =============================================================================
# Model Configuration
# =============================================================================

@dataclass
class ModelConfig:
    """
    Configuration for LLM architecture - The Dragonborn's Build.

    Now with support for:
    - Transformer (standard attention)
    - Mamba/Mamba2 (state space models)
    - GatedDeltaNet (linear attention)
    - Hybrid (alternating attention + linear blocks)
    - Mixture of Experts (MoE)

    All integrated with OLMo-core for production-quality implementations.
    """

    # === Identity ===
    name: str = "Dovahkiin"
    race: str = "Custom"

    # === Core Attributes (The Main Stats) ===
    n_embd: int = 768
    n_layers: int = 12
    n_heads: int = 12
    n_kv_heads: Optional[int] = None  # For GQA (None = same as n_heads)
    seq_length: int = 1024
    vocab_size: int = 50257

    # === Sequence Model Type (The Soul) ===
    sequence_model: SequenceModelType = SequenceModelType.TRANSFORMER

    # For hybrid models: which layers use FLA vs attention
    # e.g., [0, 2, 4] means layers 0, 2, 4 use FLA, others use attention
    fla_layers: Optional[List[int]] = None

    # === Architecture Choices (Combat Style) ===
    attention_type: AttentionType = AttentionType.DEFAULT
    attention_backend: AttentionBackend = AttentionBackend.TORCH
    mlp_type: MLPType = MLPType.STANDARD
    block_type: BlockType = BlockType.PRE_NORM
    norm_type: NormType = NormType.LAYER_NORM
    position_encoding: PositionEncoding = PositionEncoding.ROPE

    # === MLP Specifics ===
    mlp_ratio: float = 4.0
    mlp_bias: bool = True

    # === Attention Specifics ===
    qk_norm: bool = False
    attention_dropout: float = 0.0
    attention_bias: bool = True
    sliding_window: Optional[int] = None  # For sliding window attention
    qk_clip: Optional[float] = None       # QK clipping for stability

    # === Regularization (Mage Stone) ===
    dropout: float = 0.0
    embed_dropout: float = 0.0

    # === Efficiency (Thief Stone) ===
    tie_embeddings: bool = False
    use_flash_attention: bool = True
    gradient_checkpointing: bool = False

    # === Training (Warrior Stone) ===
    optimizer: Optimizer = Optimizer.ADAMW
    learning_rate: float = 3e-4
    weight_decay: float = 0.1
    beta1: float = 0.9
    beta2: float = 0.95

    # === RoPE Specifics ===
    rope_theta: float = 10000.0
    rope_scaling: RoPEScaling = RoPEScaling.NONE
    rope_scaling_factor: float = 1.0

    # === Mixture of Experts (MoE) - The Guild ===
    use_moe: bool = False
    num_experts: int = 8
    experts_per_token: int = 2          # top-k
    moe_router: MoERouterType = MoERouterType.LINEAR
    moe_gating: MoEGatingFunction = MoEGatingFunction.SOFTMAX
    moe_load_balancing: bool = True
    moe_lb_weight: float = 0.01         # Load balancing loss weight
    moe_z_loss_weight: float = 0.001    # Z-loss for entropy
    moe_shared_mlp: bool = False        # Include a shared dense MLP alongside experts
    moe_jitter: float = 0.0             # Router jitter for load balancing

    # === Mamba/FLA Specifics (The Automaton's Soul) ===
    mamba_d_state: int = 16             # SSM state dimension
    mamba_d_conv: int = 4               # Conv kernel size
    mamba_expand: int = 2               # Expansion factor

    # === GatedDeltaNet Native Config (The Hist's Wisdom) ===
    # These map to olmo-core's GatedDeltaNetConfig (SequenceMixer API)
    gdn_expand_v: float = 2.0          # Value expansion ratio
    gdn_allow_neg_eigval: bool = True   # Allow negative eigenvalues in recurrence
    gdn_conv_size: int = 4              # Causal 1D convolution kernel size
    gdn_n_v_heads: Optional[int] = None # Separate value head count (Grouped Value Attn)

    @property
    def head_dim(self) -> int:
        """Dimension per attention head."""
        return self.n_embd // self.n_heads

    @property
    def kv_heads(self) -> int:
        """Number of key-value heads (for GQA)."""
        return self.n_kv_heads if self.n_kv_heads else self.n_heads

    @property
    def is_mamba(self) -> bool:
        """Check if this is a Mamba-based architecture."""
        return self.sequence_model in (
            SequenceModelType.MAMBA,
            SequenceModelType.MAMBA2,
            SequenceModelType.GATED_DELTANET
        )

    @property
    def is_hybrid(self) -> bool:
        """Check if this is a hybrid architecture."""
        return self.sequence_model == SequenceModelType.HYBRID

    @property
    def is_moe(self) -> bool:
        """Check if this uses MoE."""
        return self.use_moe or self.block_type in (
            BlockType.MOE, BlockType.MOE_REORDERED, BlockType.MOE_HYBRID
        )

    def param_count(self) -> int:
        """Calculate total parameter count."""
        # Embedding params
        embed_params = self.vocab_size * self.n_embd
        # No learned positional embeddings supported — RoPE/none have zero
        # positional parameters of their own.
        pos_params = 0

        # Per-layer params depend on architecture
        if self.is_mamba:
            layer_params = self._mamba_layer_params()
        else:
            layer_params = self._transformer_layer_params()

        # Final layer norm
        final_norm = self.n_embd if self.norm_type in (NormType.RMS_NORM, NormType.FUSED_RMS_NORM) else 2 * self.n_embd

        # Unembedding (lm_head)
        unembed_params = 0 if self.tie_embeddings else self.n_embd * self.vocab_size

        total = embed_params + pos_params + (layer_params * self.n_layers) + final_norm + unembed_params
        return total

    def _transformer_layer_params(self) -> int:
        """Calculate params for a single transformer layer."""
        # Attention params
        if self.n_kv_heads and self.n_kv_heads != self.n_heads:
            # GQA: Q projection + K projection + V projection + O projection
            q_params = self.n_embd * self.n_heads * self.head_dim
            kv_params = 2 * self.n_embd * self.kv_heads * self.head_dim
            o_params = self.n_embd * self.n_embd
            attn_params = q_params + kv_params + o_params
        else:
            # MHA: QKV combined projection + O projection
            attn_params = self.n_embd * 3 * self.n_embd + self.n_embd * self.n_embd

        # Add bias if applicable
        if self.attention_bias:
            if self.n_kv_heads and self.n_kv_heads != self.n_heads:
                attn_params += self.n_heads * self.head_dim + 2 * self.kv_heads * self.head_dim + self.n_embd
            else:
                attn_params += 3 * self.n_embd + self.n_embd

        # QK norm params
        if self.qk_norm:
            attn_params += 2 * self.head_dim  # Q and K norms

        # MLP params
        if self.is_moe:
            mlp_params = self._moe_params()
        elif self.mlp_type == MLPType.SWIGLU:
            hidden = int(self.n_embd * self.mlp_ratio)
            hidden = ((hidden + 255) // 256) * 256  # Round to 256
            mlp_params = 3 * self.n_embd * hidden  # gate, up, down
            if self.mlp_bias:
                mlp_params += 2 * hidden + self.n_embd
        else:
            hidden = int(self.n_embd * self.mlp_ratio)
            mlp_params = 2 * self.n_embd * hidden
            if self.mlp_bias:
                mlp_params += hidden + self.n_embd

        # Norm params
        if self.norm_type in (NormType.RMS_NORM, NormType.FUSED_RMS_NORM, NormType.L2_NORM):
            norm_params = 2 * self.n_embd  # 2 norms per layer
        else:
            norm_params = 4 * self.n_embd  # 2 norms * (weight + bias)

        # Peri-norm has more norms
        if self.block_type == BlockType.PERI_NORM:
            norm_params *= 1.5

        return int(attn_params + mlp_params + norm_params)

    def _mamba_layer_params(self) -> int:
        """Calculate params for a single Mamba layer."""
        # Mamba block params (approximate)
        # in_proj (2 * expand * d), conv1d, x_proj, dt_proj, A, D, out_proj
        expand = self.mamba_expand
        d_inner = expand * self.n_embd
        d_state = self.mamba_d_state
        d_conv = self.mamba_d_conv

        in_proj = self.n_embd * (2 * d_inner)
        conv1d = d_inner * d_conv
        x_proj = d_inner * (d_state + d_state + 1)  # dt, B, C
        dt_proj = d_inner * d_inner
        A_params = d_inner * d_state
        D_params = d_inner
        out_proj = d_inner * self.n_embd

        mamba_params = in_proj + conv1d + x_proj + dt_proj + A_params + D_params + out_proj

        # Norm params
        if self.norm_type in (NormType.RMS_NORM, NormType.FUSED_RMS_NORM):
            norm_params = self.n_embd
        else:
            norm_params = 2 * self.n_embd

        return int(mamba_params + norm_params)

    def _moe_params(self) -> int:
        """Calculate params for MoE layer."""
        hidden = int(self.n_embd * self.mlp_ratio)
        hidden = ((hidden + 255) // 256) * 256

        # Each expert
        if self.mlp_type == MLPType.SWIGLU:
            expert_params = 3 * self.n_embd * hidden
        else:
            expert_params = 2 * self.n_embd * hidden

        total_expert_params = expert_params * self.num_experts

        # Router params
        router_params = self.n_embd * self.num_experts

        # Shared MLP if enabled
        shared_params = 0
        if self.moe_shared_mlp:
            shared_params = expert_params

        return total_expert_params + router_params + shared_params

    def memory_estimate(self, dtype: str = "fp32") -> int:
        """Estimate memory in bytes for model weights."""
        bytes_per_param = {"fp32": 4, "fp16": 2, "bf16": 2, "int8": 1}
        return self.param_count() * bytes_per_param.get(dtype, 4)

    def memory_str(self, dtype: str = "fp32") -> str:
        """Human-readable memory estimate."""
        mem = self.memory_estimate(dtype)
        if mem >= 1e9:
            return f"{mem / 1e9:.1f} GB"
        elif mem >= 1e6:
            return f"{mem / 1e6:.1f} MB"
        else:
            return f"{mem / 1e3:.1f} KB"

    def param_str(self) -> str:
        """Human-readable parameter count."""
        params = self.param_count()
        if params >= 1e9:
            return f"{params / 1e9:.1f}B"
        elif params >= 1e6:
            return f"{params / 1e6:.1f}M"
        else:
            return f"{params / 1e3:.1f}K"

    def copy(self) -> "ModelConfig":
        """Create a deep copy of this config."""
        return deepcopy(self)

    def validate(self) -> list[str]:
        """Validate configuration and return list of issues."""
        issues = []

        if self.n_embd % self.n_heads != 0:
            issues.append(f"n_embd ({self.n_embd}) must be divisible by n_heads ({self.n_heads})")

        if self.n_kv_heads is not None:
            if self.n_heads % self.n_kv_heads != 0:
                issues.append(f"n_heads ({self.n_heads}) must be divisible by n_kv_heads ({self.n_kv_heads})")

        if self.position_encoding in (PositionEncoding.ROPE, PositionEncoding.FUSED_ROPE, PositionEncoding.COMPLEX_ROPE):
            if self.head_dim % 2 != 0:
                issues.append(f"RoPE requires even head_dim, got {self.head_dim}")

        if self.is_moe:
            if self.experts_per_token > self.num_experts:
                issues.append(f"experts_per_token ({self.experts_per_token}) cannot exceed num_experts ({self.num_experts})")

        if self.attention_type == AttentionType.FUSED:
            if self.position_encoding not in (PositionEncoding.FUSED_ROPE, PositionEncoding.ROPE):
                issues.append("FusedAttention requires RoPE position encoding")

        if self.attention_type == AttentionType.NORMALIZED:
            if self.qk_norm:
                issues.append("NormalizedAttention should not use additional QK normalization")

        if self.is_hybrid and not self.fla_layers:
            issues.append("Hybrid mode requires fla_layers to specify which layers use GatedDeltaNet")

        if self.is_hybrid and self.fla_layers is not None:
            bad = [i for i in self.fla_layers if not 0 <= i < self.n_layers]
            if bad:
                issues.append(
                    f"fla_layers contains out-of-range indices for n_layers={self.n_layers}: {bad}"
                )

        if self.is_hybrid and self.is_moe:
            issues.append(
                "Hybrid + MoE is not supported by the generator yet — pick one"
            )

        return issues

    def get_architecture_summary(self) -> str:
        """Get a human-readable architecture summary."""
        parts = []

        # Sequence model type
        if self.is_mamba:
            parts.append(f"Sequence: {self.sequence_model.value}")
        elif self.is_hybrid:
            fla_count = len(self.fla_layers) if self.fla_layers else 0
            parts.append(f"Hybrid: {fla_count} FLA + {self.n_layers - fla_count} Attn layers")
        else:
            parts.append(f"Attention: {self.attention_type.name}")

        # MoE
        if self.is_moe:
            parts.append(f"MoE: {self.num_experts} experts, top-{self.experts_per_token}")

        # MLP
        parts.append(f"MLP: {self.mlp_type.name}")

        # Norm
        parts.append(f"Norm: {self.norm_type.name}")

        # Position
        parts.append(f"Position: {self.position_encoding.name}")

        return " | ".join(parts)
