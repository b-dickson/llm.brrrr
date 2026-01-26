"""
Summary Screen - Name Your Creation
Final review and code generation with OLMo-core integration.

"It is in the determination of one's destiny that the true nature of
architecture is revealed."
"""

from pathlib import Path

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Footer, Input, Button, TextArea
from textual.containers import Horizontal, Vertical, Center, ScrollableContainer
from textual.binding import Binding

from ..widgets.parchment import DragonBorder
from ..generator import generate_model_code, generate_full_package


SUMMARY_HEADER = r"""[bold #c9a959]
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║    ███▄    █  ▄▄▄       ███▄ ▄███▓▓█████     ▓██   ██▓ ▒█████   █    ██  ██▀███║
║    ██ ▀█   █ ▒████▄    ▓██▒▀█▀ ██▒▓█   ▀      ▒██  ██▒▒██▒  ██▒ ██  ▓██▒▓██ ▒ ██▒
║   ▓██  ▀█ ██▒▒██  ▀█▄  ▓██    ▓██░▒███         ▒██ ██░▒██░  ██▒▓██  ▒██░▓██ ░▄█ ▒
║   ▓██▒  ▐▌██▒░██▄▄▄▄██ ▒██    ▒██ ▒▓█  ▄       ░ ▐██▓░▒██   ██░▓▓█  ░██░▒██▀▀█▄  ║
║   ▒██░   ▓██░ ▓█   ▓██▒▒██▒   ░██▒░▒████▒      ░ ██▒▓░░ ████▓▒░▒▒█████▓ ░██▓ ▒██▒║
║                                                                               ║
║       ▄████▄   ██▀███  ▓█████ ▄▄▄     ▄▄▄█████▓ ██▓ ▒█████   ███▄    █        ║
║      ▒██▀ ▀█  ▓██ ▒ ██▒▓█   ▀▒████▄   ▓  ██▒ ▓▒▓██▒▒██▒  ██▒ ██ ▀█   █        ║
║      ▒▓█    ▄ ▓██ ░▄█ ▒▒███  ▒██  ▀█▄ ▒ ▓██░ ▒░▒██▒▒██░  ██▒▓██  ▀█ ██▒       ║
║      ▒▓▓▄ ▄██▒▒██▀▀█▄  ▒▓█  ▄░██▄▄▄▄██░ ▓██▓ ░ ░██░▒██   ██░▓██▒  ▐▌██▒       ║
║      ▒ ▓███▀ ░░██▓ ▒██▒░▒████▒▓█   ▓██▒ ▒██▒ ░ ░██░░ ████▓▒░▒██░   ▓██░       ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
[/]"""


class SummaryScreen(Screen):
    """Screen for final review and code generation."""

    BINDINGS = [
        Binding("g", "generate", "Generate", show=True),
        Binding("f", "full_package", "Full Package", show=True),
        Binding("p", "preview", "Preview", show=True),
        Binding("escape", "back", "Back", show=True),
        Binding("q", "quit", "Quit", show=True),
    ]

    DEFAULT_CSS = """
    SummaryScreen {
        background: #1a1512;
        overflow-y: auto;
    }

    #summary-header {
        width: 100%;
        text-align: center;
    }

    #summary-scroll {
        width: 100%;
        height: 1fr;
    }

    #summary-main {
        width: 100%;
        height: auto;
        padding: 0 4;
    }

    #name-section {
        width: 100%;
        height: auto;
        padding: 1 2;
    }

    #name-label {
        color: #c9a959;
        padding-bottom: 1;
    }

    #name-input {
        width: 40;
        background: #2a1f14;
        border: tall #5a4a32;
    }

    #name-input:focus {
        border: tall #c9a959;
    }

    #summary-box {
        width: 100%;
        height: auto;
        margin: 1 0;
    }

    .summary-row {
        height: 1;
        padding: 0 1;
    }

    .summary-label {
        color: #8b7355;
        width: 24;
    }

    .summary-value {
        color: #d4c4a8;
    }

    .summary-highlight {
        color: #c9a959;
        text-style: bold;
    }

    #param-summary {
        color: #c9a959;
        text-style: bold;
        text-align: center;
        padding: 1;
    }

    #arch-summary {
        color: #7a6e5a;
        text-align: center;
        text-style: italic;
        padding-bottom: 1;
    }

    #action-buttons {
        width: 100%;
        height: auto;
        align: center middle;
        padding: 1;
    }

    #action-buttons Button {
        margin: 0 1;
    }

    #preview-area {
        width: 100%;
        height: 20;
        background: #1a1512;
        border: tall #5a4a32;
        margin: 1 0;
    }

    #dramatic-message {
        color: #7a6e5a;
        text-style: italic;
        text-align: center;
        padding: 1;
    }

    .separator {
        color: #5a4a32;
        text-align: center;
        width: 100%;
    }

    #generation-status {
        color: #3e7a2c;
        text-align: center;
        padding: 1;
    }

    .section-divider {
        color: #5a4a32;
        padding: 1 0;
    }
    """

    def compose(self) -> ComposeResult:
        """Compose the summary screen."""
        config = self.app.config
        race_info = self.app.get_race_info()

        yield Static(SUMMARY_HEADER, id="summary-header", markup=True)

        with ScrollableContainer(id="summary-scroll"):
            with Vertical(id="summary-main"):
                # Name input
                with Horizontal(id="name-section"):
                    yield Static("Model Name:", id="name-label")
                    yield Input(value=config.name, placeholder="Enter model name...", id="name-input")

                # Summary box
                with DragonBorder(title="FINAL BUILD", id="summary-box"):
                    with Horizontal(classes="summary-row"):
                        yield Static("Race:", classes="summary-label")
                        yield Static(f"[#c9a959]{race_info['display_name']}[/] ({race_info['model_name']})", classes="summary-value", markup=True)

                    with Horizontal(classes="summary-row"):
                        yield Static("Category:", classes="summary-label")
                        yield Static(race_info.get('category', 'Custom'), classes="summary-value")

                    yield Static("[#5a4a32]─── Architecture ───[/]", classes="section-divider", markup=True)

                    with Horizontal(classes="summary-row"):
                        yield Static("Sequence Model:", classes="summary-label")
                        seq_type = config.sequence_model.name
                        if config.is_mamba:
                            seq_type = f"[#b8860b]{seq_type}[/] (State Space)"
                        elif config.is_hybrid:
                            seq_type = f"[#708090]{seq_type}[/] (Attention + FLA)"
                        else:
                            seq_type = f"[#c9a959]{seq_type}[/]"
                        yield Static(seq_type, classes="summary-value", markup=True)

                    with Horizontal(classes="summary-row"):
                        yield Static("Attention:", classes="summary-label")
                        yield Static(f"{config.attention_type.name} ({config.n_heads}H / {config.kv_heads}KV)", classes="summary-value")

                    with Horizontal(classes="summary-row"):
                        yield Static("MLP:", classes="summary-label")
                        yield Static(f"{config.mlp_type.name} ({config.mlp_ratio}x expansion)", classes="summary-value")

                    with Horizontal(classes="summary-row"):
                        yield Static("Block:", classes="summary-label")
                        yield Static(config.block_type.name, classes="summary-value")

                    with Horizontal(classes="summary-row"):
                        yield Static("Normalization:", classes="summary-label")
                        yield Static(config.norm_type.name, classes="summary-value")

                    with Horizontal(classes="summary-row"):
                        yield Static("Position Encoding:", classes="summary-label")
                        yield Static(config.position_encoding.name, classes="summary-value")

                    # MoE section if applicable
                    if config.is_moe:
                        yield Static("[#5a4a32]─── Mixture of Experts ───[/]", classes="section-divider", markup=True)

                        with Horizontal(classes="summary-row"):
                            yield Static("Experts:", classes="summary-label")
                            yield Static(f"[#deb887]{config.num_experts}[/] experts, top-{config.experts_per_token}", classes="summary-value", markup=True)

                        with Horizontal(classes="summary-row"):
                            yield Static("Router:", classes="summary-label")
                            yield Static(f"{config.moe_router.name} ({config.moe_gating.name})", classes="summary-value")

                        with Horizontal(classes="summary-row"):
                            yield Static("Load Balancing:", classes="summary-label")
                            yield Static("Enabled" if config.moe_load_balancing else "Disabled", classes="summary-value")

                    # Mamba section if applicable
                    if config.is_mamba:
                        yield Static("[#5a4a32]─── Automaton Core ───[/]", classes="section-divider", markup=True)

                        with Horizontal(classes="summary-row"):
                            yield Static("State Dimension:", classes="summary-label")
                            yield Static(str(config.mamba_d_state), classes="summary-value")

                        with Horizontal(classes="summary-row"):
                            yield Static("Conv Kernel:", classes="summary-label")
                            yield Static(str(config.mamba_d_conv), classes="summary-value")

                        with Horizontal(classes="summary-row"):
                            yield Static("Expansion:", classes="summary-label")
                            yield Static(f"{config.mamba_expand}x", classes="summary-value")

                    yield Static("[#5a4a32]─── Dimensions ───[/]", classes="section-divider", markup=True)

                    with Horizontal(classes="summary-row"):
                        yield Static("Embedding:", classes="summary-label")
                        yield Static(f"{config.n_embd:,}d", classes="summary-value")

                    with Horizontal(classes="summary-row"):
                        yield Static("Layers:", classes="summary-label")
                        yield Static(str(config.n_layers), classes="summary-value")

                    with Horizontal(classes="summary-row"):
                        yield Static("Context Length:", classes="summary-label")
                        yield Static(f"{config.seq_length:,} tokens", classes="summary-value")

                    with Horizontal(classes="summary-row"):
                        yield Static("Vocabulary:", classes="summary-label")
                        yield Static(f"{config.vocab_size:,} tokens", classes="summary-value")

                    yield Static(f"[bold #c9a959]Parameters: {config.param_str()}[/] | Memory: {config.memory_str('bf16')} (bf16)", id="param-summary", markup=True)
                    yield Static(config.get_architecture_summary(), id="arch-summary")

                # Action buttons
                with Center(id="action-buttons"):
                    yield Button("[G] Generate Config", id="btn-generate", variant="primary")
                    yield Button("[F] Full Package", id="btn-full")
                    yield Button("[P] Preview", id="btn-preview")
                    yield Button("[Q] Quit", id="btn-quit")

                yield Static("", id="generation-status")
                yield Static('"Your creation awaits, Dragonborn. OLMo-core stands ready."', id="dramatic-message")

        yield Footer()

    def on_mount(self) -> None:
        """Focus the name input on mount."""
        name_input = self.query_one("#name-input", Input)
        name_input.focus()

    def on_input_changed(self, event: Input.Changed) -> None:
        """Update config name when input changes."""
        if event.input.id == "name-input":
            self.app.config.name = event.value

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "btn-generate":
            self.action_generate()
        elif event.button.id == "btn-full":
            self.action_full_package()
        elif event.button.id == "btn-preview":
            self.action_preview()
        elif event.button.id == "btn-quit":
            self.app.exit()

    def action_generate(self) -> None:
        """Generate and save the model config file."""
        config = self.app.config

        # Validate config
        issues = config.validate()
        if issues:
            self.notify("\n".join(issues), title="Configuration Issues", severity="error")
            return

        # Generate code
        code = generate_model_code(config)

        # Create output directory
        output_dir = Path("models")
        output_dir.mkdir(exist_ok=True)

        # Save file
        model_name = config.name.lower().replace(" ", "_").replace("-", "_")
        filename = f"{model_name}_config.py"
        output_path = output_dir / filename

        try:
            output_path.write_text(code)
            status = self.query_one("#generation-status", Static)
            status.update(f"[bold green]Success![/] Config saved to: {output_path}")
            self.notify(f"Config saved to {output_path}", title="Generation Complete", severity="information")

            # Update dramatic message
            dramatic = self.query_one("#dramatic-message", Static)
            dramatic.update('"It is done. Your OLMo-core config awaits, Dragonborn."')

        except Exception as e:
            self.notify(f"Error saving file: {e}", title="Error", severity="error")

    def action_full_package(self) -> None:
        """Generate full package with config, training script, and README."""
        config = self.app.config

        # Validate config
        issues = config.validate()
        if issues:
            self.notify("\n".join(issues), title="Configuration Issues", severity="error")
            return

        # Generate full package
        package = generate_full_package(config)

        # Create output directory
        model_name = config.name.lower().replace(" ", "_").replace("-", "_")
        output_dir = Path("models") / model_name
        output_dir.mkdir(parents=True, exist_ok=True)

        try:
            for filename, content in package.items():
                filepath = output_dir / filename
                filepath.write_text(content)

            status = self.query_one("#generation-status", Static)
            status.update(f"[bold green]Success![/] Full package saved to: {output_dir}/")
            self.notify(f"Package saved to {output_dir}/", title="Full Package Generated", severity="information")

            # Update dramatic message
            dramatic = self.query_one("#dramatic-message", Static)
            dramatic.update('"A complete arsenal. Config, training script, and documentation. Go forth and train!"')

        except Exception as e:
            self.notify(f"Error saving package: {e}", title="Error", severity="error")

    def action_preview(self) -> None:
        """Show a preview of the generated code."""
        config = self.app.config
        code = generate_model_code(config)

        # Show in a notification (truncated for readability)
        lines = code.split('\n')[:30]
        preview = '\n'.join(lines) + "\n\n... (truncated)"
        self.notify(preview, title=f"Preview: {config.name}", timeout=15)

    def action_back(self) -> None:
        """Go back to standing stones."""
        self.app.pop_screen()

    def action_quit(self) -> None:
        """Quit the application."""
        self.app.exit()
