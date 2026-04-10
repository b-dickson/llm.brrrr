"""
Character Sheet - A compact preview of the current model build.
"""

from textual.widgets import Static
from textual.containers import Vertical, Horizontal
from textual.app import ComposeResult

from ..config import ModelConfig, SequenceModelType, PositionEncoding


class StatBar(Static):
    """A colorful stat bar visualization."""

    DEFAULT_CSS = """
    StatBar {
        height: 1;
    }
    """

    def __init__(
        self,
        label: str,
        value: int,
        max_val: int,
        color: str = "#c9a959",
        id: str | None = None,
    ) -> None:
        super().__init__(id=id, markup=True)
        self.label = label
        self.value = value
        self.max_val = max_val
        self.color = color

    def render(self) -> str:
        """Render the stat bar in the gold-leaf palette."""
        pct = min(self.value / self.max_val, 1.0) if self.max_val > 0 else 0
        bar_width = 12
        filled = int(round(pct * bar_width))
        empty = bar_width - filled

        # Quiet gold gradient — same logic as StatSlider for visual coherence.
        if pct < 0.2:
            bar_color = "#8a6f2c"
        elif pct < 0.55:
            bar_color = "#c9a959"
        elif pct < 0.85:
            bar_color = "#e8d9a0"
        else:
            bar_color = "#ffd266"

        bar = f"[{bar_color}]{'█' * filled}[/][#26200f]{'░' * empty}[/]"

        if self.value >= 1_000_000_000:
            val_str = f"{self.value / 1_000_000_000:.1f}B"
        elif self.value >= 1_000_000:
            val_str = f"{self.value / 1_000_000:.0f}M"
        elif self.value >= 1_000:
            val_str = f"{self.value / 1_000:.0f}K"
        else:
            val_str = str(self.value)

        return f"[#8b7355]{self.label:<12}[/] {bar} [{self.color}]{val_str:>6}[/]"


class CharacterSheet(Vertical):
    """A compact character sheet showing the current model build."""

    DEFAULT_CSS = """
    CharacterSheet {
        width: 36;
        height: auto;
        background: #1c160e;
        border: heavy #5a4a32;
        padding: 1;
    }

    CharacterSheet:focus-within {
        border: heavy #c9a959;
    }

    .sheet-header {
        color: #ffd266;
        text-style: bold;
        text-align: center;
        width: 100%;
        padding-bottom: 1;
    }

    .sheet-divider {
        color: #5a4a32;
        text-align: center;
        width: 100%;
    }

    .sheet-section {
        padding: 0;
    }

    .sheet-label {
        color: #8b7355;
        width: 14;
    }

    .sheet-value {
        color: #d4c4a8;
    }

    .sheet-value-highlight {
        color: #c9a959;
        text-style: bold;
    }

    .sheet-row {
        height: 1;
    }

    .param-count {
        color: #c9a959;
        text-style: bold;
        text-align: center;
        padding-top: 1;
    }

    .arch-type {
        text-align: center;
        padding-bottom: 1;
    }

    .arch-transformer {
        color: #c9a959;
    }

    .arch-mamba {
        color: #b8860b;
    }

    .arch-hybrid {
        color: #708090;
    }

    .arch-moe {
        color: #deb887;
    }
    """

    def __init__(
        self,
        config: ModelConfig | None = None,
        id: str | None = None,
        classes: str | None = None,
    ) -> None:
        super().__init__(id=id, classes=classes)
        self._config = config

    def compose(self) -> ComposeResult:
        """Compose the character sheet."""
        yield Static("╔══ CHARACTER SHEET ══╗", classes="sheet-header", markup=True)

        if self._config:
            yield from self._build_sheet()
        else:
            yield Static("[#7a6e5a]No configuration loaded[/]", markup=True)

    def _build_sheet(self) -> ComposeResult:
        """Build the sheet content from config."""
        config = self._config

        # Architecture type badge
        arch_class = "arch-transformer"
        arch_text = "⚡ TRANSFORMER"
        if config.sequence_model == SequenceModelType.GATED_DELTANET:
            arch_class = "arch-hybrid"
            arch_text = "🌊 GATED DELTANET"
        elif config.is_mamba:
            arch_class = "arch-mamba"
            arch_text = "⚙️ MAMBA/SSM"
        elif config.is_hybrid:
            arch_class = "arch-hybrid"
            arch_text = "🔀 HYBRID"
        elif config.is_moe:
            arch_class = "arch-moe"
            arch_text = "👥 MoE"

        yield Static(f"[bold]{arch_text}[/]", classes=f"arch-type {arch_class}", markup=True)
        yield Static("─" * 30, classes="sheet-divider")

        # Core stats as bars
        yield StatBar("Embedding", config.n_embd, 8192)
        yield StatBar("Layers", config.n_layers, 80)
        yield StatBar("Heads", config.n_heads, 64)
        yield StatBar("Context", config.seq_length, 131072)

        yield Static("─" * 30, classes="sheet-divider")

        # Architecture details
        with Horizontal(classes="sheet-row"):
            yield Static("Attention:", classes="sheet-label")
            yield Static(config.attention_type.name, classes="sheet-value")

        with Horizontal(classes="sheet-row"):
            yield Static("MLP:", classes="sheet-label")
            yield Static(config.mlp_type.name, classes="sheet-value")

        with Horizontal(classes="sheet-row"):
            yield Static("Norm:", classes="sheet-label")
            yield Static(config.norm_type.name, classes="sheet-value")

        with Horizontal(classes="sheet-row"):
            yield Static("Position:", classes="sheet-label")
            yield Static(config.position_encoding.name, classes="sheet-value")

        # MoE details if applicable
        if config.is_moe:
            yield Static("─" * 30, classes="sheet-divider")
            with Horizontal(classes="sheet-row"):
                yield Static("Experts:", classes="sheet-label")
                yield Static(f"{config.num_experts} (top-{config.experts_per_token})", classes="sheet-value")

        # GatedDeltaNet details if applicable
        if config.sequence_model == SequenceModelType.GATED_DELTANET:
            yield Static("─" * 30, classes="sheet-divider")
            with Horizontal(classes="sheet-row"):
                yield Static("Expand V:", classes="sheet-label")
                yield Static(f"{config.gdn_expand_v}x", classes="sheet-value")
            with Horizontal(classes="sheet-row"):
                yield Static("Conv Size:", classes="sheet-label")
                yield Static(str(config.gdn_conv_size), classes="sheet-value")
            with Horizontal(classes="sheet-row"):
                yield Static("Mixer:", classes="sheet-label")
                yield Static("[#228b22]Native[/]", classes="sheet-value", markup=True)

        # Mamba details if applicable
        elif config.is_mamba:
            yield Static("─" * 30, classes="sheet-divider")
            with Horizontal(classes="sheet-row"):
                yield Static("State Dim:", classes="sheet-label")
                yield Static(str(config.mamba_d_state), classes="sheet-value")

        yield Static("─" * 30, classes="sheet-divider")

        # Parameter count
        yield Static(f"[bold #c9a959]Parameters: {config.param_str()}[/]", classes="param-count", markup=True)
        yield Static(f"[#7a6e5a]Memory: {config.memory_str('bf16')} (bf16)[/]", classes="param-count", markup=True)

    def update_config(self, config: ModelConfig) -> None:
        """Update the sheet with a new config."""
        self._config = config
        self.refresh(recompose=True)


class MiniSheet(Static):
    """A minimal one-line character summary."""

    DEFAULT_CSS = """
    MiniSheet {
        height: 1;
        background: #2a1f14;
        padding: 0 1;
    }
    """

    def __init__(
        self,
        config: ModelConfig | None = None,
        id: str | None = None,
    ) -> None:
        super().__init__(id=id, markup=True)
        self._config = config

    def render(self) -> str:
        """Render the mini sheet."""
        if not self._config:
            return "[#7a6e5a]No config[/]"

        config = self._config

        # Architecture icon
        if config.sequence_model == SequenceModelType.GATED_DELTANET:
            arch = "[#228b22]🌊[/]"
        elif config.is_mamba:
            arch = "[#b8860b]⚙️[/]"
        elif config.is_hybrid:
            arch = "[#708090]🔀[/]"
        elif config.is_moe:
            arch = "[#deb887]👥[/]"
        else:
            arch = "[#c9a959]⚡[/]"

        return (
            f"{arch} "
            f"[#c9a959]{config.name}[/] "
            f"[#8b7355]|[/] "
            f"[#d4c4a8]{config.n_embd}d × {config.n_layers}L[/] "
            f"[#8b7355]|[/] "
            f"[bold #c9a959]{config.param_str()}[/]"
        )

    def update_config(self, config: ModelConfig) -> None:
        """Update with new config."""
        self._config = config
        self.refresh()
