"""
Standing Stones Screen - Advanced Configuration
Warrior (optimization), Mage (regularization), Thief (efficiency) options.

"Do you get to the Cloud District very often? Oh what am I saying, of course you
don't - you're still using O(n^2) attention."
"""

from math import log10

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Footer, Checkbox, RadioButton, RadioSet, Input, Label
from textual.containers import Horizontal, Vertical, ScrollableContainer, Container
from textual.binding import Binding

from ..widgets.stat_slider import StatSlider
from ..widgets.parchment import DragonBorder
from ..widgets.character_sheet import MiniSheet
from ..config import (
    Optimizer,
    AttentionBackend,
    RoPEScaling,
    MoEGatingFunction,
)


def _lr_exponent(learning_rate: float) -> int:
    """Convert a learning rate like ``3e-4`` into the slider's integer
    exponent (``4``). Falls back to ``4`` for non-positive rates."""
    if learning_rate <= 0:
        return 4
    return max(1, min(6, int(round(-log10(learning_rate)))))


STONES_HEADER = r"""[bold #c9a959]
   ╔════════════════════════════════════════════════════════════════════════════╗
   ║                                                                            ║
   ║         ✦  T H E    S T A N D I N G    S T O N E S  ✦                      ║
   ║                                                                            ║
   ║         [#8b7355]Walk between three monoliths and choose your blessing.[/#8b7355]            ║
   ║                                                                            ║
   ╚════════════════════════════════════════════════════════════════════════════╝[/]
[#ff6b35]   ◆ Warrior[/]   [#5a4a32]·[/]   [#a0c4e8]◆ Mage[/]   [#5a4a32]·[/]   [#3e7a2c]◆ Thief[/]"""


class StandingStonesScreen(Screen):
    """Screen for advanced configuration options (Standing Stones)."""

    BINDINGS = [
        Binding("enter", "continue", "Continue", show=True),
        Binding("tab", "focus_next", "Next", show=False),
        Binding("shift+tab", "focus_previous", "Previous", show=False),
        Binding("escape", "back", "Back", show=True),
    ]

    DEFAULT_CSS = """
    StandingStonesScreen {
        background: #1a1512;
        overflow-y: auto;
    }

    #stones-header {
        width: 100%;
        text-align: center;
    }

    #stones-scroll {
        width: 100%;
        height: 1fr;
    }

    #stones-container {
        width: 100%;
        height: auto;
        padding: 0 2;
    }

    .stone-panel {
        width: 1fr;
        height: auto;
        margin: 1;
    }

    .stone-warrior {
        border: heavy #ff6b35;
        border-title-color: #ff6b35;
    }

    .stone-mage {
        border: heavy #a0c4e8;
        border-title-color: #a0c4e8;
    }

    .stone-thief {
        border: heavy #3e7a2c;
        border-title-color: #3e7a2c;
    }

    .stone-serpent {
        border: heavy #8b4513;
        border-title-color: #8b4513;
    }

    .stone-description {
        color: #7a6e5a;
        text-style: italic;
        padding-bottom: 1;
    }

    .option-row {
        height: auto;
        padding: 0 1;
    }

    .option-label {
        color: #8b7355;
        width: 18;
    }

    .separator {
        color: #5a4a32;
        text-align: center;
        width: 100%;
    }

    Checkbox {
        padding: 0 1;
        height: 1;
    }

    RadioSet {
        background: transparent;
        border: none;
        height: auto;
    }

    RadioButton {
        background: transparent;
        padding: 0 1;
        height: 1;
    }

    Input {
        width: 16;
        height: 1;
    }

    .sub-section {
        padding: 1 0;
        border-top: solid #3a2a1a;
        margin-top: 1;
    }

    .sub-title {
        color: #8b7355;
        text-style: bold;
        padding-bottom: 1;
    }

    #mini-sheet-bar {
        width: 100%;
        dock: bottom;
        background: #2a1f14;
        border-top: heavy #5a4a32;
        padding: 0 2;
        height: 3;
    }
    """

    def compose(self) -> ComposeResult:
        """Compose the standing stones screen."""
        config = self.app.config

        yield Static(STONES_HEADER, id="stones-header", markup=True)

        with ScrollableContainer(id="stones-scroll"):
            with Horizontal(id="stones-container"):
                # Warrior Stone - Optimization
                with DragonBorder(title="THE WARRIOR STONE", classes="stone-panel stone-warrior"):
                    yield Static("[#ff6b35]Blessing of Combat - Training & Optimization[/]", classes="stone-description", markup=True)

                    with Horizontal(classes="option-row"):
                        yield Label("Optimizer:", classes="option-label")
                        with RadioSet(id="radio-optimizer"):
                            yield RadioButton("AdamW", value=config.optimizer == Optimizer.ADAMW, id="opt-adamw")
                            yield RadioButton("Muon", value=config.optimizer == Optimizer.MUON, id="opt-muon")

                    yield StatSlider(
                        "Learning Rate (1e-x)",
                        min_val=1,
                        max_val=6,
                        initial=_lr_exponent(config.learning_rate),
                        step=1,
                        id="slider-lr",
                    )

                    yield StatSlider(
                        "Weight Decay",
                        min_val=0,
                        max_val=100,
                        initial=int(config.weight_decay * 100),
                        step=1,
                        big_step=10,
                        id="slider-weight-decay",
                    )

                    # Attention Backend
                    with Vertical(classes="sub-section"):
                        yield Static("[#ff6b35]Attention Backend[/]", classes="sub-title", markup=True)
                        with Horizontal(classes="option-row"):
                            yield Label("Backend:", classes="option-label")
                            with RadioSet(id="radio-backend"):
                                yield RadioButton("Torch SDPA", value=config.attention_backend == AttentionBackend.TORCH, id="backend-torch")
                                yield RadioButton("Flash 2", value=config.attention_backend == AttentionBackend.FLASH_2, id="backend-flash2")
                                yield RadioButton("Flash 3", value=config.attention_backend == AttentionBackend.FLASH_3, id="backend-flash3")
                                yield RadioButton("Flash 4", value=config.attention_backend == AttentionBackend.FLASH_4, id="backend-flash4")
                                yield RadioButton("TE", value=config.attention_backend == AttentionBackend.TRANSFORMER_ENGINE, id="backend-te")

                # Mage Stone - Regularization
                with DragonBorder(title="THE MAGE STONE", classes="stone-panel stone-mage"):
                    yield Static("[#a0c4e8]Blessing of Magic - Regularization & Stability[/]", classes="stone-description", markup=True)

                    yield Checkbox("QK Normalization", config.qk_norm, id="check-qk-norm")

                    yield StatSlider(
                        "Dropout",
                        min_val=0,
                        max_val=50,
                        initial=int(config.dropout * 100),
                        step=1,
                        big_step=5,
                        suffix="%",
                        id="slider-dropout",
                    )

                    yield StatSlider(
                        "Attention Dropout",
                        min_val=0,
                        max_val=50,
                        initial=int(config.attention_dropout * 100),
                        step=1,
                        big_step=5,
                        suffix="%",
                        id="slider-attn-dropout",
                    )

                    yield StatSlider(
                        "Embed Dropout",
                        min_val=0,
                        max_val=50,
                        initial=int(config.embed_dropout * 100),
                        step=1,
                        big_step=5,
                        suffix="%",
                        id="slider-embed-dropout",
                    )

                    # RoPE Scaling
                    with Vertical(classes="sub-section"):
                        yield Static("[#a0c4e8]RoPE Scaling (Long Context)[/]", classes="sub-title", markup=True)
                        with Horizontal(classes="option-row"):
                            yield Label("Scaling:", classes="option-label")
                            with RadioSet(id="radio-rope-scaling"):
                                yield RadioButton("None", value=config.rope_scaling == RoPEScaling.NONE, id="rope-none")
                                yield RadioButton("ABF", value=config.rope_scaling == RoPEScaling.ABF, id="rope-abf")
                                yield RadioButton("PI", value=config.rope_scaling == RoPEScaling.PI, id="rope-pi")
                                yield RadioButton("LLaMA-3", value=config.rope_scaling == RoPEScaling.LLAMA3, id="rope-llama3")
                                yield RadioButton("YaRN", value=config.rope_scaling == RoPEScaling.YARN, id="rope-yarn")

                # Thief Stone - Efficiency
                with DragonBorder(title="THE THIEF STONE", classes="stone-panel stone-thief"):
                    yield Static("[#3e7a2c]Blessing of Shadow - Memory & Speed[/]", classes="stone-description", markup=True)

                    yield Checkbox("Tie Embeddings", config.tie_embeddings, id="check-tie-emb")
                    yield Checkbox("Flash Attention", config.use_flash_attention, id="check-flash-attn")
                    yield Checkbox("Gradient Checkpointing", config.gradient_checkpointing, id="check-grad-ckpt")
                    yield Checkbox("MLP Bias", config.mlp_bias, id="check-mlp-bias")
                    yield Checkbox("Attention Bias", config.attention_bias, id="check-attn-bias")

                    # MoE Options (if MoE is enabled)
                    if config.is_moe:
                        with Vertical(classes="sub-section"):
                            yield Static("[#3e7a2c]MoE Routing Options[/]", classes="sub-title", markup=True)
                            yield Checkbox("Load Balancing Loss", config.moe_load_balancing, id="check-moe-lb")
                            yield Checkbox("Shared Dense MLP", config.moe_shared_mlp, id="check-moe-shared")

                            with Horizontal(classes="option-row"):
                                yield Label("Gating:", classes="option-label")
                                with RadioSet(id="radio-moe-gating"):
                                    yield RadioButton("Softmax", value=config.moe_gating == MoEGatingFunction.SOFTMAX, id="gate-softmax")
                                    yield RadioButton("Sigmoid", value=config.moe_gating == MoEGatingFunction.SIGMOID, id="gate-sigmoid")

                            yield StatSlider(
                                "LB Loss Weight (x100)",
                                min_val=0,
                                max_val=10,
                                initial=int(config.moe_lb_weight * 100),
                                step=1,
                                id="slider-moe-lb",
                            )

        # Mini sheet bar at bottom
        with Container(id="mini-sheet-bar"):
            yield MiniSheet(config, id="mini-sheet")

        yield Footer()

    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        """Handle radio button changes."""
        config = self.app.config
        radio_id = event.radio_set.id
        pressed_id = event.pressed.id if event.pressed else None

        if radio_id == "radio-optimizer":
            if pressed_id == "opt-adamw":
                config.optimizer = Optimizer.ADAMW
            elif pressed_id == "opt-muon":
                config.optimizer = Optimizer.MUON

        elif radio_id == "radio-backend":
            if pressed_id == "backend-torch":
                config.attention_backend = AttentionBackend.TORCH
            elif pressed_id == "backend-flash2":
                config.attention_backend = AttentionBackend.FLASH_2
            elif pressed_id == "backend-flash3":
                config.attention_backend = AttentionBackend.FLASH_3
            elif pressed_id == "backend-flash4":
                config.attention_backend = AttentionBackend.FLASH_4
            elif pressed_id == "backend-te":
                config.attention_backend = AttentionBackend.TRANSFORMER_ENGINE

        elif radio_id == "radio-rope-scaling":
            if pressed_id == "rope-none":
                config.rope_scaling = RoPEScaling.NONE
            elif pressed_id == "rope-abf":
                config.rope_scaling = RoPEScaling.ABF
            elif pressed_id == "rope-pi":
                config.rope_scaling = RoPEScaling.PI
            elif pressed_id == "rope-llama3":
                config.rope_scaling = RoPEScaling.LLAMA3
            elif pressed_id == "rope-yarn":
                config.rope_scaling = RoPEScaling.YARN

        elif radio_id == "radio-moe-gating":
            if pressed_id == "gate-softmax":
                config.moe_gating = MoEGatingFunction.SOFTMAX
            elif pressed_id == "gate-sigmoid":
                config.moe_gating = MoEGatingFunction.SIGMOID

    def on_checkbox_changed(self, event: Checkbox.Changed) -> None:
        """Handle checkbox changes."""
        config = self.app.config
        checkbox_id = event.checkbox.id
        value = event.value

        if checkbox_id == "check-qk-norm":
            config.qk_norm = value
        elif checkbox_id == "check-tie-emb":
            config.tie_embeddings = value
        elif checkbox_id == "check-flash-attn":
            config.use_flash_attention = value
        elif checkbox_id == "check-grad-ckpt":
            config.gradient_checkpointing = value
        elif checkbox_id == "check-mlp-bias":
            config.mlp_bias = value
        elif checkbox_id == "check-attn-bias":
            config.attention_bias = value
        elif checkbox_id == "check-moe-lb":
            config.moe_load_balancing = value
        elif checkbox_id == "check-moe-shared":
            config.moe_shared_mlp = value

    def on_stat_slider_changed(self, event: StatSlider.Changed) -> None:
        """Handle slider changes."""
        config = self.app.config
        slider_id = event.slider.id
        value = event.value

        if slider_id == "slider-lr":
            config.learning_rate = 10 ** (-value)
        elif slider_id == "slider-weight-decay":
            config.weight_decay = value / 100.0
        elif slider_id == "slider-dropout":
            config.dropout = value / 100.0
        elif slider_id == "slider-attn-dropout":
            config.attention_dropout = value / 100.0
        elif slider_id == "slider-embed-dropout":
            config.embed_dropout = value / 100.0
        elif slider_id == "slider-moe-lb":
            config.moe_lb_weight = value / 100.0

    def action_continue(self) -> None:
        """Continue to summary screen."""
        self.app.goto_summary()

    def action_back(self) -> None:
        """Go back to attributes screen."""
        self.app.pop_screen()
