"""
Attributes Screen - Customize Your Build
Core stat customization with sliders and architecture choices.
Now with native GatedDeltaNet SequenceMixer configuration.

"I used to be an adventurer like you, then I took a gradient to the knee."
"""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Footer, RadioButton, RadioSet, Label, Collapsible, Checkbox
from textual.containers import Horizontal, Vertical, Container, ScrollableContainer
from textual.binding import Binding

from ..widgets.stat_slider import StatSlider
from ..widgets.parchment import Parchment, DragonBorder
from ..widgets.character_sheet import CharacterSheet, MiniSheet
from ..widgets.character_portrait import get_mini_portrait
from ..config import (
    SequenceModelType,
    AttentionType,
    AttentionBackend,
    MLPType,
    BlockType,
    NormType,
    PositionEncoding,
)


ATTRIBUTES_HEADER = r"""[bold #c9a959]
    ╔═══════════════════════════════════════════════════════════════════╗
    ║   ▄▄▄     ▄▄▄█████▓▄▄▄█████▓ ██▀███   ██▓ ▄▄▄▄    █    ██ ▄▄▄█████▓║
    ║  ▒████▄   ▓  ██▒ ▓▒▓  ██▒ ▓▒▓██ ▒ ██▒▓██▒▓█████▄  ██  ▓██▒▓  ██▒ ▓▒║
    ║  ▒██  ▀█▄ ▒ ▓██░ ▒░▒ ▓██░ ▒░▓██ ░▄█ ▒▒██▒▒██▒ ▄██▓██  ▒██░▒ ▓██░ ▒░║
    ║  ░██▄▄▄▄██░ ▓██▓ ░ ░ ▓██▓ ░ ▒██▀▀█▄  ░██░▒██░█▀  ▓▓█  ░██░░ ▓██▓ ░ ║
    ║   ▓█   ▓██▒ ▒██▒ ░   ▒██▒ ░ ░██▓ ▒██▒░██░░▓█  ▀█▓▒▒█████▓   ▒██▒ ░ ║
    ║   ▒▒   ▓▒█░ ▒ ░░     ▒ ░░   ░ ▒▓ ░▒▓░░▓  ░▒▓███▀▒░▒▓▒ ▒ ▒   ▒ ░░   ║
    ╚═══════════════════════════════════════════════════════════════════╝
[/]
[#7a6e5a]                    ━━━ Forge Your Architecture ━━━[/]"""


class AttributesScreen(Screen):
    """Screen for customizing model attributes."""

    BINDINGS = [
        Binding("enter", "continue", "Continue", show=True),
        Binding("tab", "focus_next", "Next", show=False),
        Binding("shift+tab", "focus_previous", "Previous", show=False),
        Binding("escape", "back", "Back", show=True),
        Binding("r", "reset", "Reset to Preset", show=True),
    ]

    DEFAULT_CSS = """
    AttributesScreen {
        background: #1a1512;
        overflow-y: auto;
    }

    #attr-header {
        width: 100%;
        text-align: center;
    }

    #attr-subtitle {
        color: #7a6e5a;
        text-align: center;
        width: 100%;
        padding-bottom: 1;
    }

    #attr-content-wrapper {
        width: 100%;
        height: 1fr;
    }

    #attr-scroll {
        width: 1fr;
        height: 100%;
    }

    #attr-main {
        width: 100%;
        height: auto;
        padding: 0 2;
    }

    #stats-column {
        width: 1fr;
        height: auto;
    }

    #arch-column {
        width: 1fr;
        height: auto;
    }

    #char-sheet-sidebar {
        width: auto;
        height: 100%;
        background: #1a1512;
        padding: 1 0;
    }

    .section-title {
        color: #c9a959;
        text-style: bold;
        padding: 1 0;
    }

    #param-display {
        width: 100%;
        background: #231b13;
        border: tall #5a4a32;
        padding: 1 2;
        margin: 1 2;
        text-align: center;
    }

    #param-count {
        color: #c9a959;
        text-style: bold;
    }

    #param-memory {
        color: #8b7355;
    }

    #arch-summary {
        color: #7a6e5a;
        text-style: italic;
        padding-top: 1;
    }

    .separator {
        color: #5a4a32;
        text-align: center;
        width: 100%;
    }

    RadioSet {
        background: transparent;
        border: none;
        padding: 0;
        height: auto;
    }

    RadioButton {
        background: transparent;
        padding: 0 1;
    }

    .arch-group {
        padding: 0 1;
        height: auto;
    }

    .arch-label {
        color: #8b7355;
        padding-right: 1;
        width: 14;
    }

    Collapsible {
        background: #231b13;
        border: tall #5a4a32;
        padding: 0;
        margin: 1;
    }

    CollapsibleTitle {
        color: #c9a959;
        background: #231b13;
        padding: 0 1;
    }

    CollapsibleTitle:hover {
        background: #3d2e1f;
    }

    CollapsibleTitle:focus {
        background: #3d2e1f;
    }

    .moe-section {
        padding: 1;
    }

    .mamba-section {
        padding: 1;
    }

    .gdn-section {
        padding: 1;
    }

    #mini-sheet-bar {
        width: 100%;
        dock: bottom;
        background: #231b13;
        border-top: heavy #5a4a32;
        padding: 0 2;
        height: 3;
    }

    #mini-sheet-content {
        height: 1;
        padding: 1 0;
    }
    """

    def compose(self) -> ComposeResult:
        """Compose the attributes screen."""
        config = self.app.config
        race_info = self.app.get_race_info()

        yield Static(ATTRIBUTES_HEADER, id="attr-header", markup=True)
        yield Static(
            f"[#8b7355]Race: {race_info['display_name']} ({race_info['model_name']})[/]",
            id="attr-subtitle", markup=True,
        )

        with Horizontal(id="attr-content-wrapper"):
            with ScrollableContainer(id="attr-scroll"):
                with Horizontal(id="attr-main"):
                    # Left column: Core stats
                    with Vertical(id="stats-column"):
                        with DragonBorder(title="Core Attributes"):
                            yield StatSlider(
                                "Embedding Dimension",
                                min_val=64, max_val=16384,
                                initial=config.n_embd, step=64, big_step=256,
                                id="slider-n_embd",
                            )
                            yield StatSlider(
                                "Hidden Layers",
                                min_val=1, max_val=128,
                                initial=config.n_layers, step=1, big_step=4,
                                id="slider-n_layers",
                            )
                            yield StatSlider(
                                "Attention Heads",
                                min_val=1, max_val=128,
                                initial=config.n_heads, step=1, big_step=4,
                                id="slider-n_heads",
                            )
                            yield StatSlider(
                                "KV Heads (GQA)",
                                min_val=1, max_val=128,
                                initial=config.n_kv_heads or config.n_heads,
                                step=1, big_step=4,
                                id="slider-n_kv_heads",
                            )
                            yield StatSlider(
                                "Context Length",
                                min_val=128, max_val=131072,
                                initial=config.seq_length, step=128, big_step=1024,
                                id="slider-seq_length",
                            )
                            yield StatSlider(
                                "Vocabulary Size",
                                min_val=1000, max_val=256000,
                                initial=config.vocab_size, step=1000, big_step=10000,
                                id="slider-vocab_size",
                            )

                        # MoE settings (collapsible)
                        with Collapsible(title="⚔️ Guild of Experts (MoE)", collapsed=not config.is_moe):
                            with Vertical(classes="moe-section"):
                                yield StatSlider(
                                    "Number of Experts",
                                    min_val=2, max_val=64,
                                    initial=config.num_experts, step=1, big_step=4,
                                    id="slider-num_experts",
                                )
                                yield StatSlider(
                                    "Experts per Token",
                                    min_val=1, max_val=8,
                                    initial=config.experts_per_token, step=1,
                                    id="slider-experts_per_token",
                                )

                        # Mamba settings (collapsible)
                        is_mamba_type = config.sequence_model in (
                            SequenceModelType.MAMBA, SequenceModelType.MAMBA2
                        )
                        with Collapsible(title="⚙️ Automaton Core (Mamba)", collapsed=not is_mamba_type):
                            with Vertical(classes="mamba-section"):
                                yield StatSlider(
                                    "State Dimension",
                                    min_val=8, max_val=64,
                                    initial=config.mamba_d_state, step=8,
                                    id="slider-mamba_d_state",
                                )
                                yield StatSlider(
                                    "Conv Kernel Size",
                                    min_val=2, max_val=8,
                                    initial=config.mamba_d_conv, step=1,
                                    id="slider-mamba_d_conv",
                                )
                                yield StatSlider(
                                    "Expansion Factor",
                                    min_val=1, max_val=4,
                                    initial=config.mamba_expand, step=1,
                                    id="slider-mamba_expand",
                                )

                        # GatedDeltaNet settings (collapsible) - NEW
                        is_gdn = config.sequence_model in (
                            SequenceModelType.GATED_DELTANET, SequenceModelType.HYBRID
                        )
                        with Collapsible(title="🌊 Hist Connection (GatedDeltaNet)", collapsed=not is_gdn):
                            with Vertical(classes="gdn-section"):
                                yield Static(
                                    "[#228b22]Native SequenceMixer - olmo-core v2.4.0+[/]",
                                    markup=True,
                                )
                                yield StatSlider(
                                    "Value Expansion",
                                    min_val=1, max_val=4,
                                    initial=int(config.gdn_expand_v),
                                    step=1,
                                    id="slider-gdn_expand_v",
                                )
                                yield StatSlider(
                                    "Conv Size",
                                    min_val=2, max_val=8,
                                    initial=config.gdn_conv_size, step=1,
                                    id="slider-gdn_conv_size",
                                )
                                yield Checkbox(
                                    "Allow Negative Eigenvalues",
                                    config.gdn_allow_neg_eigval,
                                    id="check-gdn-neg-eigval",
                                )

                    # Right column: Architecture choices
                    with Vertical(id="arch-column"):
                        with DragonBorder(title="Soul Type"):
                            with Horizontal(classes="arch-group"):
                                yield Label("Architecture:", classes="arch-label")
                                with RadioSet(id="radio-sequence"):
                                    yield RadioButton("Transformer", value=config.sequence_model == SequenceModelType.TRANSFORMER, id="seq-transformer")
                                    yield RadioButton("Mamba", value=config.sequence_model == SequenceModelType.MAMBA, id="seq-mamba")
                                    yield RadioButton("Mamba2", value=config.sequence_model == SequenceModelType.MAMBA2, id="seq-mamba2")
                                    yield RadioButton("GatedDeltaNet", value=config.sequence_model == SequenceModelType.GATED_DELTANET, id="seq-deltanet")
                                    yield RadioButton("Hybrid", value=config.sequence_model == SequenceModelType.HYBRID, id="seq-hybrid")

                        with DragonBorder(title="Combat Style"):
                            with Horizontal(classes="arch-group"):
                                yield Label("Attention:", classes="arch-label")
                                with RadioSet(id="radio-attention"):
                                    yield RadioButton("Default", value=config.attention_type == AttentionType.DEFAULT, id="attn-default")
                                    yield RadioButton("Fused", value=config.attention_type == AttentionType.FUSED, id="attn-fused")
                                    yield RadioButton("Normalized", value=config.attention_type == AttentionType.NORMALIZED, id="attn-normalized")

                            with Horizontal(classes="arch-group"):
                                yield Label("MLP:", classes="arch-label")
                                with RadioSet(id="radio-mlp"):
                                    yield RadioButton("Standard", value=config.mlp_type == MLPType.STANDARD, id="mlp-standard")
                                    yield RadioButton("SwiGLU", value=config.mlp_type == MLPType.SWIGLU, id="mlp-swiglu")

                            with Horizontal(classes="arch-group"):
                                yield Label("Block:", classes="arch-label")
                                with RadioSet(id="radio-block"):
                                    yield RadioButton("Pre-Norm", value=config.block_type == BlockType.PRE_NORM, id="block-pre")
                                    yield RadioButton("Reordered", value=config.block_type == BlockType.REORDERED, id="block-reordered")
                                    yield RadioButton("nGPT", value=config.block_type == BlockType.NORMALIZED, id="block-ngpt")
                                    yield RadioButton("MoE", value=config.block_type == BlockType.MOE, id="block-moe")

                            with Horizontal(classes="arch-group"):
                                yield Label("Norm:", classes="arch-label")
                                with RadioSet(id="radio-norm"):
                                    yield RadioButton("LayerNorm", value=config.norm_type == NormType.LAYER_NORM, id="norm-ln")
                                    yield RadioButton("RMSNorm", value=config.norm_type == NormType.RMS_NORM, id="norm-rms")
                                    yield RadioButton("FusedRMS", value=config.norm_type == NormType.FUSED_RMS_NORM, id="norm-fused")
                                    yield RadioButton("L2Norm", value=config.norm_type == NormType.L2_NORM, id="norm-l2")

                            with Horizontal(classes="arch-group"):
                                yield Label("Position:", classes="arch-label")
                                with RadioSet(id="radio-position"):
                                    yield RadioButton("Learned", value=config.position_encoding == PositionEncoding.LEARNED, id="pos-learned")
                                    yield RadioButton("RoPE", value=config.position_encoding == PositionEncoding.ROPE, id="pos-rope")
                                    yield RadioButton("Fused RoPE", value=config.position_encoding == PositionEncoding.FUSED_ROPE, id="pos-fused")
                                    yield RadioButton("None", value=config.position_encoding == PositionEncoding.NONE, id="pos-none")

            # Character sheet sidebar
            with Vertical(id="char-sheet-sidebar"):
                yield CharacterSheet(config, id="char-sheet")

        # Mini sheet bar at bottom
        with Container(id="mini-sheet-bar"):
            yield MiniSheet(config, id="mini-sheet")

        yield Footer()

    def on_mount(self) -> None:
        """Focus the first slider on mount."""
        slider = self.query_one("#slider-n_embd", StatSlider)
        slider.focus()

    def on_stat_slider_changed(self, event: StatSlider.Changed) -> None:
        """Handle slider value changes."""
        slider_id = event.slider.id
        value = event.value
        config = self.app.config

        if slider_id == "slider-n_embd":
            config.n_embd = value
        elif slider_id == "slider-n_layers":
            config.n_layers = value
        elif slider_id == "slider-n_heads":
            config.n_heads = value
        elif slider_id == "slider-n_kv_heads":
            config.n_kv_heads = value
        elif slider_id == "slider-seq_length":
            config.seq_length = value
        elif slider_id == "slider-vocab_size":
            config.vocab_size = value
        elif slider_id == "slider-num_experts":
            config.num_experts = value
        elif slider_id == "slider-experts_per_token":
            config.experts_per_token = value
        elif slider_id == "slider-mamba_d_state":
            config.mamba_d_state = value
        elif slider_id == "slider-mamba_d_conv":
            config.mamba_d_conv = value
        elif slider_id == "slider-mamba_expand":
            config.mamba_expand = value
        elif slider_id == "slider-gdn_expand_v":
            config.gdn_expand_v = float(value)
        elif slider_id == "slider-gdn_conv_size":
            config.gdn_conv_size = value

        self._update_param_display()

    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        """Handle radio button changes."""
        radio_id = event.radio_set.id
        pressed_id = event.pressed.id if event.pressed else None
        config = self.app.config

        if radio_id == "radio-sequence":
            if pressed_id == "seq-transformer":
                config.sequence_model = SequenceModelType.TRANSFORMER
            elif pressed_id == "seq-mamba":
                config.sequence_model = SequenceModelType.MAMBA
            elif pressed_id == "seq-mamba2":
                config.sequence_model = SequenceModelType.MAMBA2
            elif pressed_id == "seq-deltanet":
                config.sequence_model = SequenceModelType.GATED_DELTANET
            elif pressed_id == "seq-hybrid":
                config.sequence_model = SequenceModelType.HYBRID

        elif radio_id == "radio-attention":
            if pressed_id == "attn-default":
                config.attention_type = AttentionType.DEFAULT
            elif pressed_id == "attn-fused":
                config.attention_type = AttentionType.FUSED
            elif pressed_id == "attn-normalized":
                config.attention_type = AttentionType.NORMALIZED

        elif radio_id == "radio-mlp":
            if pressed_id == "mlp-standard":
                config.mlp_type = MLPType.STANDARD
                config.mlp_ratio = 4.0
            elif pressed_id == "mlp-swiglu":
                config.mlp_type = MLPType.SWIGLU
                config.mlp_ratio = 3.5

        elif radio_id == "radio-block":
            if pressed_id == "block-pre":
                config.block_type = BlockType.PRE_NORM
                config.use_moe = False
            elif pressed_id == "block-reordered":
                config.block_type = BlockType.REORDERED
                config.use_moe = False
            elif pressed_id == "block-ngpt":
                config.block_type = BlockType.NORMALIZED
                config.use_moe = False
            elif pressed_id == "block-moe":
                config.block_type = BlockType.MOE
                config.use_moe = True

        elif radio_id == "radio-norm":
            if pressed_id == "norm-ln":
                config.norm_type = NormType.LAYER_NORM
            elif pressed_id == "norm-rms":
                config.norm_type = NormType.RMS_NORM
            elif pressed_id == "norm-fused":
                config.norm_type = NormType.FUSED_RMS_NORM
            elif pressed_id == "norm-l2":
                config.norm_type = NormType.L2_NORM

        elif radio_id == "radio-position":
            if pressed_id == "pos-learned":
                config.position_encoding = PositionEncoding.LEARNED
            elif pressed_id == "pos-rope":
                config.position_encoding = PositionEncoding.ROPE
            elif pressed_id == "pos-fused":
                config.position_encoding = PositionEncoding.FUSED_ROPE
            elif pressed_id == "pos-none":
                config.position_encoding = PositionEncoding.NONE

        self._update_param_display()

    def on_checkbox_changed(self, event) -> None:
        """Handle checkbox changes."""
        config = self.app.config
        checkbox_id = event.checkbox.id
        value = event.value

        if checkbox_id == "check-gdn-neg-eigval":
            config.gdn_allow_neg_eigval = value

    def _update_param_display(self) -> None:
        """Update the parameter count display and character sheet."""
        config = self.app.config

        try:
            char_sheet = self.query_one("#char-sheet", CharacterSheet)
            char_sheet.update_config(config)
        except Exception:
            pass

        try:
            mini_sheet = self.query_one("#mini-sheet", MiniSheet)
            mini_sheet.update_config(config)
        except Exception:
            pass

    def action_continue(self) -> None:
        """Continue to standing stones screen."""
        issues = self.app.config.validate()
        if issues:
            self.notify("\n".join(issues), title="Configuration Issues", severity="warning")
            return
        self.app.goto_standing_stones()

    def action_back(self) -> None:
        """Go back to race selection."""
        self.app.pop_screen()

    def action_reset(self) -> None:
        """Reset to preset values."""
        self.app.load_preset(self.app.selected_race)
        self.app.pop_screen()
        self.app.goto_attributes()
