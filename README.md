# The Elder Models V: LLMRIM

**A Skyrim-esque LLM Architecture Creator with OLMo-core Integration**

*"Fus Ro Brrr... Your training begins."*

## Overview

LLMRIM is a terminal-based user interface for designing and generating LLM architectures. It features a complete Skyrim-themed character creation experience where model architectures are presented as "races" with unique abilities and bonuses.

Now integrated with **OLMo-core** for production-quality implementations including:
- Standard Transformer architectures (GPT-2, LLaMA-3 style)
- **Mamba/Mamba2** state space models
- **GatedDeltaNet** linear attention
- **Hybrid** architectures (attention + linear layers)
- **Mixture of Experts (MoE)** with sophisticated routing
- **nGPT** normalized transformers

## Installation

```bash
# Clone the repository
cd llm.brrrr

# Install dependencies
pip install textual olmo-core flash-attn fla

# Run the creator
python -m creator
```

## Races (Model Presets)

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

### Falmer (Hybrid)
| Race | Model | Parameters | Lore |
|------|-------|------------|------|
| Falmer | Hybrid 1B | ~1B | Alternating attention + FLA |
| Warmonger | Hybrid 3B | ~3B | Best of both architectures |

### Argonians (Linear Attention)
| Race | Model | Parameters | Lore |
|------|-------|------------|------|
| Argonian | GatedDeltaNet 370M | ~370M | Fluid, adaptive processing |
| Shadowscale | GatedDeltaNet 1B | ~1B | O(n) complexity assassin |

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

1. **Title Screen** - Dramatic intro with dragon ASCII art
2. **Race Selection** - Choose your model family (tabbed by category)
3. **Attributes** - Customize dimensions, heads, layers, MoE/Mamba settings
4. **Standing Stones** - Training options (Warrior/Mage/Thief blessings)
5. **Summary** - Review and generate OLMo-core compatible code

## Generated Output

LLMRIM generates complete OLMo-core configurations:

```python
# Example: Generated Daedra (LLaMA-3 8B) config
from olmo_core.nn.transformer import TransformerConfig
from olmo_core.nn.attention import AttentionConfig, AttentionBackend
from olmo_core.nn.feed_forward import FeedForwardConfig
from olmo_core.nn.rope import RoPEConfig, RoPEType

config = TransformerConfig(
    d_model=4096,
    n_layers=32,
    n_heads=32,
    n_kv_heads=8,
    vocab_size=128256,
    max_seq_len=8192,
    attention=AttentionConfig(
        backend=AttentionBackend.flash_2,
        qk_norm=False,
    ),
    feed_forward=FeedForwardConfig(
        activation='silu',  # SwiGLU
    ),
    rope=RoPEConfig(
        type=RoPEType.default,
        theta=500000.0,
    ),
)
```

## Full Package Generation

Generate a complete model package with:
- `*_config.py` - OLMo-core model configuration
- `*_train.py` - Training script with distributed support
- `README.md` - Model documentation

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

This project integrates with OLMo-core to provide:

### Attention
- [x] Default (MHA, GQA support)
- [x] Fused (Flash-optimized)
- [x] Normalized (nGPT-style)
- [x] QK normalization
- [x] QK clipping

### Backends
- [x] PyTorch SDPA
- [x] Flash Attention 2
- [x] Flash Attention 3 (H100+)
- [x] TransformerEngine

### Position Encoding
- [x] Learned
- [x] RoPE
- [x] Fused RoPE
- [x] No position (for Mamba)

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

### Linear Attention (FLA)
- [x] Mamba
- [x] Mamba2
- [x] GatedDeltaNet
- [x] Hybrid (attention + FLA)

### Optimizers
- [x] AdamW
- [x] Muon

## Theme

The entire UI uses a Skyrim-inspired color palette:
- **Gold** (#c9a959) - Primary accent
- **Bronze** (#8b7355) - Secondary text
- **Leather** (#1a1512) - Dark background
- **Fire** (#ff6b35) - Warrior Stone
- **Frost** (#a0c4e8) - Mage Stone
- **Shadow** (#3e7a2c) - Thief Stone

## Credits

Built with:
- [Textual](https://textual.textualize.io/) - TUI framework
- [OLMo-core](https://github.com/allenai/OLMo-core) - LLM training framework
- [flash-attention](https://github.com/Dao-AILab/flash-attention) - Efficient attention
- [fla](https://github.com/sustcsonglin/flash-linear-attention) - Linear attention

---

*"What is better - to be born good, or to overcome your architecture through great training?"*
    *- Paarthurnax, on fine-tuning*
