# The Elder Models V: LLMRIM

**A Skyrim-esque LLM Architecture Creator with OLMo-core Integration**

*"Fus Ro Brrr... Your training begins."*

## Overview

LLMRIM is a terminal-based user interface for designing and generating LLM architectures. It features a complete Skyrim-themed character creation experience where model architectures are presented as "races" with unique abilities and bonuses.

Built on the **OLMo-core v2.4.0+ SequenceMixer API** for production-quality implementations including:
- Standard Transformer architectures (GPT-2, LLaMA-3 style)
- **GatedDeltaNet** linear attention (native SequenceMixer — no FLA wrapper needed)
- **Mamba/Mamba2** state space models (via FLA)
- **Hybrid** architectures (Attention + GatedDeltaNet per-layer mixing)
- **Mixture of Experts (MoE)** with sophisticated routing
- **nGPT** normalized transformers

## Installation

```bash
# Clone the repository
cd llm.brrrr

# Install dependencies
uv pip install textual olmo-core flash-attn fla

# Run the creator
python -m creator
```

Requires **olmo-core >= 2.4.0** for native SequenceMixer support.

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

## Generated Output

LLMRIM generates complete OLMo-core configurations using the **SequenceMixer API**:

```python
# Example: Generated Daedra (LLaMA-3 8B) config
from olmo_core.nn.transformer import TransformerConfig, TransformerBlockConfig
from olmo_core.nn.attention import AttentionConfig, AttentionBackend
from olmo_core.nn.feed_forward import FeedForwardConfig
from olmo_core.nn.layer_norm import RMSNormConfig
from olmo_core.nn.rope import RoPEConfig, RoPEType

config = TransformerConfig(
    d_model=4096,
    n_layers=32,
    vocab_size=128256,
    max_seq_len=8192,
    block=TransformerBlockConfig(
        sequence_mixer=AttentionConfig(
            n_heads=32,
            n_kv_heads=8,
            head_dim=128,
            backend=AttentionBackend.flash_2,
        ),
        feed_forward=FeedForwardConfig(
            hidden_size=14336,
            activation="silu",
        ),
        layer_norm=RMSNormConfig(),
    ),
    rope=RoPEConfig(
        type=RoPEType.default,
        theta=500000.0,
    ),
)
```

GatedDeltaNet models generate native SequenceMixer configs:

```python
# Example: Generated Veezara (GatedDeltaNet 3B) config
from olmo_core.nn.transformer import TransformerConfig, TransformerBlockConfig
from olmo_core.nn.gated_deltanet import GatedDeltaNetConfig
from olmo_core.nn.feed_forward import FeedForwardConfig
from olmo_core.nn.layer_norm import RMSNormConfig

config = TransformerConfig(
    d_model=3072,
    n_layers=32,
    vocab_size=50257,
    max_seq_len=32768,
    block=TransformerBlockConfig(
        sequence_mixer=GatedDeltaNetConfig(
            n_heads=48,
            expand_v=2.0,
            allow_neg_eigval=True,
            conv_size=4,
        ),
        feed_forward=FeedForwardConfig(
            hidden_size=10752,
            activation="silu",
        ),
        layer_norm=RMSNormConfig(),
    ),
)
```

Hybrid architectures use `block_overrides` to assign different SequenceMixers per layer:

```python
# Hybrid: alternating Attention + GatedDeltaNet layers
config = TransformerConfig(
    d_model=2048,
    n_layers=24,
    block=TransformerBlockConfig(
        sequence_mixer=AttentionConfig(...),  # default block
    ),
    block_overrides={
        # Even layers get GatedDeltaNet
        i: TransformerBlockConfig(
            sequence_mixer=GatedDeltaNetConfig(...)
        )
        for i in range(0, 24, 2)
    },
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

## OLMo-core Features

This project integrates with OLMo-core v2.4.0+ to provide:

### Sequence Mixers
- [x] Attention (MHA, GQA support)
- [x] Fused Attention (Flash-optimized)
- [x] Normalized Attention (nGPT-style)
- [x] **GatedDeltaNet** (native SequenceMixer — O(n) linear attention)
- [x] QK normalization / QK clipping

### Attention Backends
- [x] PyTorch SDPA
- [x] Flash Attention 2
- [x] Flash Attention 3 (H100+)
- [x] Flash Attention 4 (CUTE)
- [x] TransformerEngine

### Position Encoding
- [x] Learned
- [x] RoPE
- [x] Fused RoPE
- [x] No position (for Mamba / GatedDeltaNet)

### RoPE Scaling
- [x] ABF (Absolute Base Frequency)
- [x] PI (Position Interpolation)
- [x] LLaMA-3 stepwise
- [x] YaRN

### Blocks
- [x] Pre-norm (LLaMA-style)
- [x] Reordered norm
- [x] Peri-norm
- [x] Normalized (nGPT)
- [x] MoE variants

### Normalization
- [x] LayerNorm
- [x] RMSNorm
- [x] Fused RMSNorm
- [x] L2Norm (nGPT)

### MLP
- [x] Standard (GELU)
- [x] SwiGLU

### Mixture of Experts
- [x] Linear router
- [x] Softmax/Sigmoid gating
- [x] Load balancing loss
- [x] Z-loss
- [x] Shared dense MLP

### Linear Attention
- [x] **GatedDeltaNet** — native `SequenceMixerConfig` (no FLA wrapper)
- [x] Mamba (via FLA)
- [x] Mamba2 (via FLA)
- [x] Hybrid (Attention + GatedDeltaNet per-layer via `block_overrides`)

### Optimizers
- [x] AdamW
- [x] Muon

## Theme

The entire UI uses a Skyrim-inspired color palette:
- **Gold** (#c9a959) — Primary accent
- **Bronze** (#8b7355) — Secondary text
- **Leather** (#1a1512) — Dark background
- **Fire** (#ff6b35) — Warrior Stone
- **Frost** (#a0c4e8) — Mage Stone
- **Shadow** (#3e7a2c) — Thief Stone
- **Hist Green** (#228b22) — GatedDeltaNet / Argonian accents

## Credits

Built with:
- [Textual](https://textual.textualize.io/) — TUI framework
- [OLMo-core](https://github.com/allenai/OLMo-core) — LLM training framework (v2.4.0+ SequenceMixer API)
- [flash-attention](https://github.com/Dao-AILab/flash-attention) — Efficient attention
- [fla](https://github.com/sustcsonglin/flash-linear-attention) — Linear attention (Mamba/Mamba2 wrapper)

---

*"What is better — to be born good, or to overcome your architecture through great training?"*
    *— Paarthurnax, on fine-tuning*
