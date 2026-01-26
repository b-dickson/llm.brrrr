"""
Model Presets - The Races of Tamriel
Complete architecture configurations including Transformer, Mamba, MoE, and Hybrid variants.

"What is better - to be born good, or to overcome your architecture through great training?"
    - Paarthurnax, on fine-tuning
"""

from .config import (
    ModelConfig,
    SequenceModelType,
    AttentionType,
    AttentionBackend,
    MLPType,
    BlockType,
    NormType,
    PositionEncoding,
    RoPEScaling,
    Optimizer,
    MoERouterType,
    MoEGatingFunction,
)


# =============================================================================
# GPT-2 Family - "The Races of Men"
# Traditional attention-based transformers
# =============================================================================

GPT2_SMALL = ModelConfig(
    name="Dovahkiin-Small",
    race="Nord",
    n_embd=768,
    n_layers=12,
    n_heads=12,
    n_kv_heads=None,
    seq_length=1024,
    vocab_size=50257,
    sequence_model=SequenceModelType.TRANSFORMER,
    attention_type=AttentionType.DEFAULT,
    mlp_type=MLPType.STANDARD,
    block_type=BlockType.PRE_NORM,
    norm_type=NormType.LAYER_NORM,
    position_encoding=PositionEncoding.LEARNED,
    mlp_ratio=4.0,
    dropout=0.1,
    tie_embeddings=True,
    use_flash_attention=True,
)

GPT2_MEDIUM = ModelConfig(
    name="Dovahkiin-Medium",
    race="Imperial",
    n_embd=1024,
    n_layers=24,
    n_heads=16,
    n_kv_heads=None,
    seq_length=1024,
    vocab_size=50257,
    sequence_model=SequenceModelType.TRANSFORMER,
    attention_type=AttentionType.DEFAULT,
    mlp_type=MLPType.STANDARD,
    block_type=BlockType.PRE_NORM,
    norm_type=NormType.LAYER_NORM,
    position_encoding=PositionEncoding.LEARNED,
    mlp_ratio=4.0,
    dropout=0.1,
    tie_embeddings=True,
    use_flash_attention=True,
)

GPT2_LARGE = ModelConfig(
    name="Dovahkiin-Large",
    race="Altmer",
    n_embd=1280,
    n_layers=36,
    n_heads=20,
    n_kv_heads=None,
    seq_length=1024,
    vocab_size=50257,
    sequence_model=SequenceModelType.TRANSFORMER,
    attention_type=AttentionType.DEFAULT,
    mlp_type=MLPType.STANDARD,
    block_type=BlockType.PRE_NORM,
    norm_type=NormType.LAYER_NORM,
    position_encoding=PositionEncoding.LEARNED,
    mlp_ratio=4.0,
    dropout=0.1,
    tie_embeddings=True,
    use_flash_attention=True,
)

GPT2_XL = ModelConfig(
    name="Dovahkiin-XL",
    race="Dragonborn",
    n_embd=1600,
    n_layers=48,
    n_heads=25,
    n_kv_heads=None,
    seq_length=1024,
    vocab_size=50257,
    sequence_model=SequenceModelType.TRANSFORMER,
    attention_type=AttentionType.DEFAULT,
    mlp_type=MLPType.STANDARD,
    block_type=BlockType.PRE_NORM,
    norm_type=NormType.LAYER_NORM,
    position_encoding=PositionEncoding.LEARNED,
    mlp_ratio=4.0,
    dropout=0.1,
    tie_embeddings=True,
    use_flash_attention=True,
)


# =============================================================================
# LLaMA-3 Family - "The Divine Beings"
# Modern architecture with GQA, SwiGLU, RoPE
# =============================================================================

LLAMA3_8B = ModelConfig(
    name="Paarthurnax",
    race="Daedra",
    n_embd=4096,
    n_layers=32,
    n_heads=32,
    n_kv_heads=8,
    seq_length=8192,
    vocab_size=128256,
    sequence_model=SequenceModelType.TRANSFORMER,
    attention_type=AttentionType.DEFAULT,
    attention_backend=AttentionBackend.FLASH_2,
    mlp_type=MLPType.SWIGLU,
    block_type=BlockType.PRE_NORM,
    norm_type=NormType.RMS_NORM,
    position_encoding=PositionEncoding.ROPE,
    mlp_ratio=3.5,
    mlp_bias=False,
    attention_bias=False,
    qk_norm=False,
    dropout=0.0,
    tie_embeddings=False,
    rope_theta=500000.0,
    use_flash_attention=True,
)

LLAMA3_70B = ModelConfig(
    name="Alduin",
    race="Aedra",
    n_embd=8192,
    n_layers=80,
    n_heads=64,
    n_kv_heads=8,
    seq_length=8192,
    vocab_size=128256,
    sequence_model=SequenceModelType.TRANSFORMER,
    attention_type=AttentionType.DEFAULT,
    attention_backend=AttentionBackend.FLASH_2,
    mlp_type=MLPType.SWIGLU,
    block_type=BlockType.PRE_NORM,
    norm_type=NormType.RMS_NORM,
    position_encoding=PositionEncoding.ROPE,
    mlp_ratio=3.5,
    mlp_bias=False,
    attention_bias=False,
    qk_norm=False,
    dropout=0.0,
    tie_embeddings=False,
    rope_theta=500000.0,
    use_flash_attention=True,
    gradient_checkpointing=True,
)


# =============================================================================
# Mamba Family - "The Dwemer Automatons"
# State Space Models - efficient linear-time sequence processing
# =============================================================================

MAMBA_370M = ModelConfig(
    name="Centurion",
    race="Dwemer",
    n_embd=1024,
    n_layers=48,
    n_heads=16,  # Not really used for Mamba, but kept for compatibility
    seq_length=8192,
    vocab_size=50257,
    sequence_model=SequenceModelType.MAMBA2,
    mlp_type=MLPType.STANDARD,
    norm_type=NormType.RMS_NORM,
    position_encoding=PositionEncoding.NONE,  # Mamba doesn't need position encoding
    dropout=0.0,
    tie_embeddings=False,
    mamba_d_state=16,
    mamba_d_conv=4,
    mamba_expand=2,
)

MAMBA_1B = ModelConfig(
    name="Animunculus",
    race="Dwemer",
    n_embd=2048,
    n_layers=48,
    n_heads=32,
    seq_length=16384,
    vocab_size=50257,
    sequence_model=SequenceModelType.MAMBA2,
    mlp_type=MLPType.STANDARD,
    norm_type=NormType.RMS_NORM,
    position_encoding=PositionEncoding.NONE,
    dropout=0.0,
    tie_embeddings=False,
    mamba_d_state=16,
    mamba_d_conv=4,
    mamba_expand=2,
    gradient_checkpointing=True,
)

MAMBA_3B = ModelConfig(
    name="Numidium",
    race="Dwemer",
    n_embd=2560,
    n_layers=64,
    n_heads=40,
    seq_length=32768,
    vocab_size=50257,
    sequence_model=SequenceModelType.MAMBA2,
    mlp_type=MLPType.STANDARD,
    norm_type=NormType.RMS_NORM,
    position_encoding=PositionEncoding.NONE,
    dropout=0.0,
    tie_embeddings=False,
    mamba_d_state=16,
    mamba_d_conv=4,
    mamba_expand=2,
    gradient_checkpointing=True,
)


# =============================================================================
# Hybrid Family - "The Falmer" (Corrupted Snow Elves)
# Alternating attention and linear attention layers
# =============================================================================

HYBRID_1B = ModelConfig(
    name="Snow-Prince",
    race="Falmer",
    n_embd=2048,
    n_layers=24,
    n_heads=32,
    n_kv_heads=8,
    seq_length=8192,
    vocab_size=50257,
    sequence_model=SequenceModelType.HYBRID,
    fla_layers=[0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22],  # Alternating
    attention_type=AttentionType.DEFAULT,
    attention_backend=AttentionBackend.FLASH_2,
    mlp_type=MLPType.SWIGLU,
    block_type=BlockType.PRE_NORM,
    norm_type=NormType.RMS_NORM,
    position_encoding=PositionEncoding.ROPE,
    mlp_ratio=3.5,
    mlp_bias=False,
    attention_bias=False,
    dropout=0.0,
    tie_embeddings=False,
    rope_theta=10000.0,
)

HYBRID_3B = ModelConfig(
    name="Arch-Curate",
    race="Falmer",
    n_embd=3072,
    n_layers=32,
    n_heads=48,
    n_kv_heads=8,
    seq_length=16384,
    vocab_size=50257,
    sequence_model=SequenceModelType.HYBRID,
    fla_layers=[0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30],
    attention_type=AttentionType.DEFAULT,
    attention_backend=AttentionBackend.FLASH_2,
    mlp_type=MLPType.SWIGLU,
    block_type=BlockType.PRE_NORM,
    norm_type=NormType.RMS_NORM,
    position_encoding=PositionEncoding.ROPE,
    mlp_ratio=3.5,
    mlp_bias=False,
    attention_bias=False,
    dropout=0.0,
    tie_embeddings=False,
    rope_theta=10000.0,
    gradient_checkpointing=True,
)


# =============================================================================
# Linear Attention Family - "The Argonians"
# GatedDeltaNet - fluid and adaptive
# =============================================================================

DELTANET_370M = ModelConfig(
    name="Hist-Born",
    race="Argonian",
    n_embd=1024,
    n_layers=24,
    n_heads=16,
    seq_length=8192,
    vocab_size=50257,
    sequence_model=SequenceModelType.GATED_DELTANET,
    mlp_type=MLPType.SWIGLU,
    norm_type=NormType.RMS_NORM,
    position_encoding=PositionEncoding.NONE,  # DeltaNet handles position internally
    mlp_ratio=3.5,
    mlp_bias=False,
    dropout=0.0,
    tie_embeddings=False,
)

DELTANET_1B = ModelConfig(
    name="Shadowscale",
    race="Argonian",
    n_embd=2048,
    n_layers=24,
    n_heads=32,
    seq_length=16384,
    vocab_size=50257,
    sequence_model=SequenceModelType.GATED_DELTANET,
    mlp_type=MLPType.SWIGLU,
    norm_type=NormType.RMS_NORM,
    position_encoding=PositionEncoding.NONE,
    mlp_ratio=3.5,
    mlp_bias=False,
    dropout=0.0,
    tie_embeddings=False,
    gradient_checkpointing=True,
)


# =============================================================================
# Mixture of Experts Family - "The Khajiit Caravans"
# Many specialized experts, swift routing
# =============================================================================

MOE_8x1B = ModelConfig(
    name="Ri'saad",
    race="Khajiit",
    n_embd=2048,
    n_layers=24,
    n_heads=32,
    n_kv_heads=8,
    seq_length=8192,
    vocab_size=50257,
    sequence_model=SequenceModelType.TRANSFORMER,
    attention_type=AttentionType.DEFAULT,
    attention_backend=AttentionBackend.FLASH_2,
    mlp_type=MLPType.SWIGLU,
    block_type=BlockType.MOE,
    norm_type=NormType.RMS_NORM,
    position_encoding=PositionEncoding.ROPE,
    mlp_ratio=3.5,
    mlp_bias=False,
    attention_bias=False,
    dropout=0.0,
    use_moe=True,
    num_experts=8,
    experts_per_token=2,
    moe_router=MoERouterType.LINEAR,
    moe_gating=MoEGatingFunction.SOFTMAX,
    moe_load_balancing=True,
    moe_lb_weight=0.01,
    moe_z_loss_weight=0.001,
    rope_theta=10000.0,
)

MOE_8x7B = ModelConfig(
    name="Mane",
    race="Khajiit",
    n_embd=4096,
    n_layers=32,
    n_heads=32,
    n_kv_heads=8,
    seq_length=32768,
    vocab_size=128256,
    sequence_model=SequenceModelType.TRANSFORMER,
    attention_type=AttentionType.DEFAULT,
    attention_backend=AttentionBackend.FLASH_2,
    mlp_type=MLPType.SWIGLU,
    block_type=BlockType.MOE,
    norm_type=NormType.RMS_NORM,
    position_encoding=PositionEncoding.ROPE,
    mlp_ratio=3.5,
    mlp_bias=False,
    attention_bias=False,
    dropout=0.0,
    use_moe=True,
    num_experts=8,
    experts_per_token=2,
    moe_router=MoERouterType.LINEAR,
    moe_gating=MoEGatingFunction.SOFTMAX,
    moe_load_balancing=True,
    moe_lb_weight=0.01,
    moe_z_loss_weight=0.001,
    moe_shared_mlp=True,  # Shared dense layer
    rope_theta=500000.0,
    rope_scaling=RoPEScaling.LLAMA3,
    gradient_checkpointing=True,
)


# =============================================================================
# nGPT Family - "The Bosmer" (Wood Elves)
# Normalized architecture - natural harmony
# =============================================================================

NGPT_1B = ModelConfig(
    name="Valenwood-Speaker",
    race="Bosmer",
    n_embd=2048,
    n_layers=24,
    n_heads=32,
    n_kv_heads=8,
    seq_length=4096,
    vocab_size=50257,
    sequence_model=SequenceModelType.TRANSFORMER,
    attention_type=AttentionType.NORMALIZED,
    mlp_type=MLPType.SWIGLU,
    block_type=BlockType.NORMALIZED,
    norm_type=NormType.L2_NORM,
    position_encoding=PositionEncoding.ROPE,
    mlp_ratio=3.5,
    mlp_bias=False,
    attention_bias=False,
    qk_norm=False,  # nGPT handles this differently
    dropout=0.0,
    tie_embeddings=False,
    rope_theta=10000.0,
)


# =============================================================================
# Preset Registry with Lore
# =============================================================================

PRESETS = {
    # === Men (GPT-2) ===
    "nord": {
        "config": GPT2_SMALL,
        "display_name": "Nord",
        "model_name": "GPT-2 Small",
        "params": "~124M",
        "category": "Transformer",
        "lore": (
            "Hardy and efficient, the Nord architecture thrives in harsh "
            "training conditions. Resistant to overfitting, quick to converge. "
            "A warrior's choice for those who value reliability over raw power."
        ),
        "bonuses": [
            "+10% Training Speed",
            "Cold Resistance (stable gradients)",
            "Battle Cry (fast inference)",
        ],
    },
    "imperial": {
        "config": GPT2_MEDIUM,
        "display_name": "Imperial",
        "model_name": "GPT-2 Medium",
        "params": "~350M",
        "category": "Transformer",
        "lore": (
            "Balanced in all attributes, the Imperial design excels at diverse "
            "tasks. A versatile foundation for any quest. Neither the strongest "
            "nor the fastest, but capable of anything."
        ),
        "bonuses": [
            "+5 All Attributes",
            "Voice of the Emperor (prompt following)",
            "Imperial Luck (better sampling)",
        ],
    },
    "altmer": {
        "config": GPT2_LARGE,
        "display_name": "Altmer",
        "model_name": "GPT-2 Large",
        "params": "~774M",
        "category": "Transformer",
        "lore": (
            "The High Elves channel immense magical power through their "
            "architecture. Superior capacity demands superior compute. "
            "Their knowledge runs deep, but their training is arduous."
        ),
        "bonuses": [
            "+50 Magicka (embedding dim)",
            "Highborn (faster attention)",
            "Magic Resistance (robust to noise)",
        ],
    },
    "dragonborn": {
        "config": GPT2_XL,
        "display_name": "Dragonborn",
        "model_name": "GPT-2 XL",
        "params": "~1.5B",
        "category": "Transformer",
        "lore": (
            "The ultimate mortal form, capable of learning any Thu'um. "
            "Requires significant compute to awaken its true potential. "
            "Legends speak of emergent abilities that manifest at scale."
        ),
        "bonuses": [
            "Dragon Shouts (emergent capabilities)",
            "Thu'um Mastery (in-context learning)",
            "Dragonblood (fine-tuning efficiency)",
        ],
    },

    # === Divine Beings (LLaMA-3) ===
    "daedra": {
        "config": LLAMA3_8B,
        "display_name": "Daedra",
        "model_name": "LLaMA-3 8B",
        "params": "~8B",
        "category": "Transformer",
        "lore": (
            "Beings from beyond Mundus, wielding otherworldly architecture. "
            "GQA attention allows many queries to share few keys, a technique "
            "as alien as it is effective. Their SwiGLU activations crackle "
            "with otherworldly energy."
        ),
        "bonuses": [
            "Oblivion Gate (RoPE long context)",
            "Daedric Artifact (GQA efficiency)",
            "Conjuration (knowledge retrieval)",
        ],
    },
    "aedra": {
        "config": LLAMA3_70B,
        "display_name": "Aedra",
        "model_name": "LLaMA-3 70B",
        "params": "~70B",
        "category": "Transformer",
        "lore": (
            "Divine architects who shaped the world. Their design transcends "
            "mortal limits. Only those with divine-tier compute dare invoke "
            "their power. Emergent reasoning awaits those worthy."
        ),
        "bonuses": [
            "Creation Magic (70B parameters)",
            "Divine Intervention (emergent reasoning)",
            "Blessing of Akatosh (temporal understanding)",
        ],
    },

    # === Dwemer (Mamba/SSM) ===
    "dwemer": {
        "config": MAMBA_370M,
        "display_name": "Dwemer",
        "model_name": "Mamba-2 370M",
        "params": "~370M",
        "category": "Mamba",
        "lore": (
            "The vanished Deep Elves left behind automatons of impossible design. "
            "Their state-space mechanisms process sequences in linear time, "
            "defying the quadratic curse that plagues lesser architectures. "
            "Efficiency through engineering, not brute force."
        ),
        "bonuses": [
            "Tonal Architecture (linear complexity)",
            "Automaton Memory (selective state)",
            "Vanishing Act (efficient inference)",
        ],
    },
    "dwemer_centurion": {
        "config": MAMBA_1B,
        "display_name": "Dwemer Centurion",
        "model_name": "Mamba-2 1B",
        "params": "~1B",
        "category": "Mamba",
        "lore": (
            "The mighty Centurions were the Dwemer's greatest automatons. "
            "Towering constructs of brass and soul gems, they process "
            "endless sequences without the memory burden of attention. "
            "Perfect for long-form understanding."
        ),
        "bonuses": [
            "Steam Power (16K context)",
            "Soul Gem Core (efficient memory)",
            "Dwemer Resilience (stable training)",
        ],
    },
    "dwemer_numidium": {
        "config": MAMBA_3B,
        "display_name": "Numidium",
        "model_name": "Mamba-2 3B",
        "params": "~3B",
        "category": "Mamba",
        "lore": (
            "The legendary Brass God, Anumidium, was powered by the Heart of "
            "Lorkhan itself. This architecture channels that divine efficiency - "
            "processing sequences of unimaginable length with grace. "
            "A god-machine for those who dare."
        ),
        "bonuses": [
            "Divine Power (32K context)",
            "Heart of Lorkhan (massive throughput)",
            "Walk-Brass (parallel inference)",
        ],
    },

    # === Falmer (Hybrid) ===
    "falmer": {
        "config": HYBRID_1B,
        "display_name": "Falmer",
        "model_name": "Hybrid 1B",
        "params": "~1B",
        "category": "Hybrid",
        "lore": (
            "Once the proud Snow Elves, the Falmer were twisted by darkness "
            "into something new. Their hybrid architecture alternates between "
            "attention and linear mechanisms - corrupted perhaps, but uniquely "
            "powerful. They see patterns others cannot."
        ),
        "bonuses": [
            "Blind Sight (alternating layers)",
            "Chaurus Poison (efficient routing)",
            "Betrayed Cunning (adaptive processing)",
        ],
    },
    "falmer_warmonger": {
        "config": HYBRID_3B,
        "display_name": "Falmer Warmonger",
        "model_name": "Hybrid 3B",
        "params": "~3B",
        "category": "Hybrid",
        "lore": (
            "The mightiest of the Falmer champions, Warmongers command both "
            "the ancient wisdom of attention and the brutal efficiency of "
            "linear mechanisms. A fearsome hybrid that excels where pure "
            "architectures falter."
        ),
        "bonuses": [
            "War Cry (16K context)",
            "Dual Nature (best of both)",
            "Blackreach Mastery (deep layers)",
        ],
    },

    # === Argonian (GatedDeltaNet) ===
    "argonian": {
        "config": DELTANET_370M,
        "display_name": "Argonian",
        "model_name": "GatedDeltaNet 370M",
        "params": "~370M",
        "category": "Linear Attention",
        "lore": (
            "Born of the Hist, Argonians flow through sequences like water "
            "through roots. Their delta-gated architecture processes tokens "
            "with fluid efficiency, adapting to context without the rigidity "
            "of traditional attention. Swift and adaptive."
        ),
        "bonuses": [
            "Hist Connection (gated memory)",
            "Waterbreathing (long sequences)",
            "Disease Immunity (noise robust)",
        ],
    },
    "argonian_shadowscale": {
        "config": DELTANET_1B,
        "display_name": "Shadowscale",
        "model_name": "GatedDeltaNet 1B",
        "params": "~1B",
        "category": "Linear Attention",
        "lore": (
            "Shadowscales are Argonians born under the sign of the Shadow, "
            "trained as assassins from birth. Their architecture strikes with "
            "deadly efficiency - O(n) complexity masks their true power. "
            "By the time you notice them, it's already too late."
        ),
        "bonuses": [
            "Shadow Sign (16K context)",
            "Assassination (fast inference)",
            "Dark Brotherhood (stealth processing)",
        ],
    },

    # === Khajiit (MoE) ===
    "khajiit": {
        "config": MOE_8x1B,
        "display_name": "Khajiit",
        "model_name": "MoE 8x1B",
        "params": "~8B (1B active)",
        "category": "Mixture of Experts",
        "lore": (
            "Khajiit has wares if you have coin. The Khajiit caravans travel "
            "with many specialists - lockpicks, alchemists, warriors, merchants. "
            "Their MoE architecture routes each token to the most skilled experts. "
            "Many hands make light work."
        ),
        "bonuses": [
            "Caravan Network (8 experts)",
            "Merchant Skills (top-2 routing)",
            "Moon Sugar Rush (sparse activation)",
        ],
    },
    "khajiit_mane": {
        "config": MOE_8x7B,
        "display_name": "Mane",
        "model_name": "MoE 8x7B",
        "params": "~56B (14B active)",
        "category": "Mixture of Experts",
        "lore": (
            "The Mane is the spiritual leader of all Khajiit, born when the "
            "moons align. This architecture commands the greatest caravan ever "
            "assembled - 8 experts of 7B parameters each, with a shared dense "
            "layer for common knowledge. True mastery."
        ),
        "bonuses": [
            "Moons Aligned (shared MLP)",
            "Elsweyr Dominion (32K context)",
            "Sugar-Fueled (efficient routing)",
        ],
    },

    # === Bosmer (nGPT) ===
    "bosmer": {
        "config": NGPT_1B,
        "display_name": "Bosmer",
        "model_name": "nGPT 1B",
        "params": "~1B",
        "category": "Normalized",
        "lore": (
            "The Wood Elves of Valenwood live in harmony with nature, their "
            "architecture reflecting perfect balance. Normalized weights and "
            "L2 norms create a stable ecosystem where no gradient dominates. "
            "Natural order through mathematical harmony."
        ),
        "bonuses": [
            "Green Pact (normalized weights)",
            "Wild Hunt (stable training)",
            "Valenwood Blessing (no softmax scaling)",
        ],
    },

    # === Custom ===
    "custom": {
        "config": GPT2_SMALL.copy(),
        "display_name": "Custom",
        "model_name": "Your Creation",
        "params": "Variable",
        "category": "Custom",
        "lore": (
            "Forge your own destiny. Start from humble beginnings and craft "
            "an architecture unlike any other. Mix Dwemer efficiency with "
            "Daedric power, or create something entirely new. "
            "The Thu'um of creation awaits your command."
        ),
        "bonuses": [
            "Unlimited Potential",
            "Your Rules",
            "Your Legacy",
        ],
    },
}


# =============================================================================
# Utility Functions
# =============================================================================

def get_preset(name: str) -> ModelConfig:
    """Get a copy of a preset configuration."""
    name = name.lower().replace(" ", "_").replace("-", "_")
    if name in PRESETS:
        return PRESETS[name]["config"].copy()
    raise ValueError(f"Unknown preset: {name}. Available: {list(PRESETS.keys())}")


def list_presets() -> list[str]:
    """List all available preset names."""
    return list(PRESETS.keys())


def get_presets_by_category(category: str) -> list[str]:
    """Get preset names filtered by category."""
    return [
        name for name, info in PRESETS.items()
        if info.get("category", "").lower() == category.lower()
    ]


def list_categories() -> list[str]:
    """List all unique categories."""
    categories = set(info.get("category", "Other") for info in PRESETS.values())
    return sorted(categories)
