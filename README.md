# The Elder Models V: LLMRIM

**A Skyrim-themed LLM architecture creator that emits OLMo-core configs.**

*"Fus Ro Brrr… your training begins."*

## Overview

LLMRIM is a terminal user interface for designing transformer (and friends)
architectures. Eighteen presets are dressed up as "races" with lore, racial
bonuses, and ASCII portraits. Tweak the dimensions, walk between the standing
stones, name your creation, and the tool generates a complete OLMo-core
config + training script package.

The TUI is dependency-light: only `textual` is required at runtime — the
generated code targets **olmo-core ≥ 2.5.0** (the SequenceMixer API), but
that is an *opt-in* extra you only install if you actually want to train.

Supported architectures (all 18 presets):

- Standard transformers — GPT-2 (Nord/Imperial/Altmer/Dragonborn) and
  LLaMA-3 (Daedra 8B, Aedra 70B)
- **GatedDeltaNet** linear attention — native `SequenceMixerConfig`, no FLA
  wrapper. Constant-size recurrent state, O(n) compute (Argonian, Shadowscale,
  Veezara)
- **Hybrid** architectures — alternating softmax attention and GatedDeltaNet
  blocks via `block_pattern` (Falmer, Warmonger)
- **Mixture of Experts** — `MoEConfig` with linear router, top-k gating, load
  balancing loss, and optional shared dense MLP (Khajiit, Mane)
- **nGPT** normalized transformers — `NormalizedTransformer` with L2 norm,
  normalized feed-forward, and normalized LM head (Bosmer)
- A "Mamba/SSM" preset family (Dwemer/Centurion/Numidium) — these emit a
  GatedDeltaNet config under v2.5.0, since OLMo-core's only native linear
  recurrent mixer is GDN

## Quick start

```bash
# 1. Sync the dev environment (this is fast — ~10 dependencies, no torch).
uv sync

# 2. Launch the TUI.
uv run llmrim
# (or: uv run python -m creator)
```

That's it. Navigate with the arrow keys, press Enter to advance, Escape to go
back, and `g`/`f` on the summary screen to generate a config or full package.

Generated files land in `./models/<your-model-name>/`.

### Running the generated configs

The TUI itself does not need olmo-core. To actually *train* a model, install
the `olmo` extra (which pulls v2.5.0 from GitHub since PyPI is still on
2.4.0):

```bash
uv sync --extra olmo

# And, if you want flash attention or the GatedDeltaNet kernels:
uv sync --extra olmo --extra flash
```

Then drop into a generated package and launch:

```bash
cd models/dovahkiin_small
torchrun --nproc-per-node=8 dovahkiin_small_train.py
```

Edit `DATA_PATHS` and `GLOBAL_BATCH_SIZE` in the train script first.

## Races (18 Model Presets)

### Transformers (The Races of Men)
| Race | Model | Parameters | Lore |
|------|-------|------------|------|
| Nord | GPT-2 Small | ~124M | Hardy and efficient, resistant to overfitting |
| Imperial | GPT-2 Medium | ~350M | Balanced in all attributes |
| Altmer | GPT-2 Large | ~774M | Superior capacity, arduous training |
| Dragonborn | GPT-2 XL | ~1.5B | Emergent abilities at scale |

### Divine Beings (LLaMA-3)
| Race | Model | Parameters | Lore |
|------|-------|------------|------|
| Daedra | LLaMA-3 8B | ~8B | Otherworldly architecture with GQA |
| Aedra | LLaMA-3 70B | ~70B | Divine-tier compute, emergent reasoning |

### Dwemer Automatons (Mamba/SSM)
| Race | Model | Parameters | Lore |
|------|-------|------------|------|
| Dwemer | Mamba-2 370M | ~370M | Linear complexity, efficient |
| Centurion | Mamba-2 1B | ~1B | 16K context, stable training |
| Numidium | Mamba-2 3B | ~3B | 32K context, god-machine |

### Falmer (Hybrid — Attention + GatedDeltaNet)
| Race | Model | Parameters | Lore |
|------|-------|------------|------|
| Falmer | Hybrid 1B | ~1B | Alternating attention + GatedDeltaNet layers |
| Warmonger | Hybrid 3B | ~3B | Best of both architectures |

### Argonians (GatedDeltaNet — Native SequenceMixer)
| Race | Model | Parameters | Lore |
|------|-------|------------|------|
| Argonian | GatedDeltaNet 370M | ~370M | Fluid, adaptive processing |
| Shadowscale | GatedDeltaNet 1B | ~1B | O(n) complexity assassin |
| Veezara | GatedDeltaNet 3B | ~3B | Native SequenceMixer, gated delta rule recurrence |

### Khajiit Caravans (MoE)
| Race | Model | Parameters | Lore |
|------|-------|------------|------|
| Khajiit | MoE 8x1B | ~8B (1B active) | 8 experts, top-2 routing |
| Mane | MoE 8x7B | ~56B (14B active) | Shared MLP, 32K context |

### Bosmer (nGPT)
| Race | Model | Parameters | Lore |
|------|-------|------------|------|
| Bosmer | nGPT 1B | ~1B | Normalized weights, stable |

## Screens

1. **Title Screen** — Dramatic intro with dragon ASCII art
2. **Race Selection** — Choose your model family (tabbed by category)
3. **Attributes** — Customize dimensions, heads, layers, GatedDeltaNet/Mamba settings
4. **Standing Stones** — Training options (Warrior/Mage/Thief blessings)
5. **Summary** — Review and generate OLMo-core compatible code

## Generated output

LLMRIM emits complete OLMo-core ≥ 2.5.0 configs using the SequenceMixer API.
A few representative slices (real, lifted from `creator/generator.py`):

### Standard transformer (Daedra / LLaMA-3 8B)

```python
from olmo_core.config import DType
from olmo_core.nn.attention import AttentionBackendName, AttentionConfig, AttentionType
from olmo_core.nn.feed_forward import FeedForwardConfig, FeedForwardType
from olmo_core.nn.layer_norm import LayerNormConfig, LayerNormType
from olmo_core.nn.lm_head import LMHeadConfig, LMHeadType
from olmo_core.nn.rope import RoPEConfig, RoPEType
from olmo_core.nn.transformer import (
    TransformerBlockConfig, TransformerBlockType, TransformerConfig, TransformerType,
)

layer_norm = LayerNormConfig(name=LayerNormType.rms, eps=1e-5, bias=False)

block = TransformerBlockConfig(
    name=TransformerBlockType.default,
    sequence_mixer=AttentionConfig(
        name=AttentionType.default,
        n_heads=32,
        n_kv_heads=8,
        bias=False,
        rope=RoPEConfig(name=RoPEType.default, theta=500000),
        backend=AttentionBackendName.flash_2,
    ),
    feed_forward=FeedForwardConfig(
        name=FeedForwardType.default,
        hidden_size=14336,
        bias=False,
    ),
    layer_norm=layer_norm,
)

config = TransformerConfig(
    name=TransformerType.default,
    d_model=4096, n_layers=32, vocab_size=128256,
    block=block,
    lm_head=LMHeadConfig(layer_norm=layer_norm, bias=False),
    dtype=DType.bfloat16, init_seed=42,
)
```

### GatedDeltaNet (Veezara / Argonian 3B)

```python
from olmo_core.nn.attention.recurrent import GatedDeltaNetConfig

block = TransformerBlockConfig(
    name=TransformerBlockType.default,
    sequence_mixer=GatedDeltaNetConfig(
        n_heads=48,
        expand_v=2.0,
        allow_neg_eigval=True,
        conv_size=4,
    ),
    feed_forward=FeedForwardConfig(
        name=FeedForwardType.default,
        hidden_size=10752,
        bias=False,
    ),
    layer_norm=layer_norm,
)
```

The recurrent state is constant-size (`n_v_heads × head_k_dim × head_v_dim`)
regardless of sequence length — long contexts cost no extra memory.

### Hybrid (Falmer / Snow-Prince 1B)

```python
attention_block = TransformerBlockConfig(
    name=TransformerBlockType.default,
    sequence_mixer=AttentionConfig(name=AttentionType.default, n_heads=32, n_kv_heads=8, ...),
    feed_forward=feed_forward,
    layer_norm=layer_norm,
)
gdn_block = TransformerBlockConfig(
    name=TransformerBlockType.default,
    sequence_mixer=GatedDeltaNetConfig(n_heads=32, ...),
    feed_forward=feed_forward,
    layer_norm=layer_norm,
)

config = TransformerConfig(
    d_model=2048, n_layers=24, vocab_size=50257,
    block={"attn": attention_block, "gdn": gdn_block},
    block_pattern=[
        "gdn", "attn", "gdn", "attn", "gdn", "attn",
        "gdn", "attn", "gdn", "attn", "gdn", "attn",
        "gdn", "attn", "gdn", "attn", "gdn", "attn",
        "gdn", "attn", "gdn", "attn", "gdn", "attn",
    ],
    ...
)
```

`block_pattern` is a clean way to interleave block kinds — much simpler than
the old `block_overrides` dict.

### Mixture of Experts (Khajiit / Ri'saad 8x1B)

```python
from olmo_core.nn.moe import MoEConfig, MoERouterConfig, MoERouterGatingFunction

block = TransformerBlockConfig(
    name=TransformerBlockType.moe,
    sequence_mixer=AttentionConfig(...),
    feed_forward_moe=MoEConfig(
        num_experts=8,
        hidden_size=7168,
        router=MoERouterConfig(
            top_k=2,
            gating_function=MoERouterGatingFunction.softmax,
        ),
        lb_loss_weight=0.01,
        z_loss_weight=0.001,
    ),
    layer_norm=layer_norm,
)
```

## Full Package Generation

Generate a complete model package with:
- `*_config.py` — OLMo-core model configuration
- `*_train.py` — Training script with distributed support
- `README.md` — Model documentation

## Keybindings

| Key | Action |
|-----|--------|
| Arrow Keys | Navigate |
| Enter | Select/Confirm |
| Tab | Next field |
| Escape | Back |
| G | Generate config |
| F | Full package |
| P | Preview code |
| Q | Quit |

## OLMo-core features covered

The generator targets OLMo-core ≥ 2.5.0. It can produce configs that use:

| Area | Options |
|---|---|
| Sequence mixers | `Attention` (MHA / GQA), `FusedAttention`, `NormalizedAttention`, `GatedDeltaNet` |
| Attention backends | `torch` (SDPA), `flash_2`, `flash_3`, `flash_4`, `te` (TransformerEngine) |
| Position encoding | learned, RoPE, fused RoPE, no-pos (for GDN) |
| RoPE scaling | ABF, PI, LLaMA-3 stepwise, YaRN |
| Block types | default, reordered-norm, peri-norm, normalized (nGPT), MoE variants |
| Normalization | LayerNorm, RMSNorm, FusedRMSNorm, L2Norm |
| MLP | SwiGLU (default), GELU (via standard MLP) |
| MoE | linear router, softmax/sigmoid gating, load-balancing & z-loss, shared dense MLP |
| Hybrid | per-layer mixing via `block_pattern` (Attention ⨯ GatedDeltaNet) |
| Optimizers | AdamW, Muon (the `Muon` reference impl ships in the repo root) |

## Theme

A weathered-parchment palette: leather backgrounds, gold leaf accents, and a
single shot of bronze for secondary text. The standing-stone screen adds three
restrained elemental hues (fire / frost / forest) only on the stone borders.

| Token | Hex | Used for |
|---|---|---|
| `gold`         | `#c9a959` | primary accent |
| `gold_bright`  | `#ffd266` | focus, hover, active |
| `bronze`       | `#8b7355` | secondary text, ornament |
| `leather_deep` | `#15100a` | screen background |
| `leather`      | `#1c160e` | cards, panels |
| `ink`          | `#d4c4a8` | body text |
| `fire`         | `#ff6b35` | Warrior Stone |
| `frost`        | `#a0c4e8` | Mage Stone |
| `forest`       | `#3e7a2c` | Thief Stone |
| `hist`         | `#228b22` | GatedDeltaNet accents |

## Credits

Built with:

- [Textual](https://textual.textualize.io/) — the TUI framework that makes any
  of this readable.
- [OLMo-core](https://github.com/allenai/OLMo-core) — the actual LLM training
  framework whose API we generate against.
- [flash-attention](https://github.com/Dao-AILab/flash-attention) and
  [flash-linear-attention](https://github.com/fla-org/flash-linear-attention) —
  optional fast kernels referenced from generated training scripts.

---

*"What is better — to be born good, or to overcome your architecture through great training?"*
    *— Paarthurnax, on fine-tuning*
