"""
Race Selection Screen - Choose Your Race
Select from preset model architectures including Transformer, Mamba, MoE, and Hybrid.

"Skyrim belongs to the Nords... and so does efficient inference!"
"""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Footer, Button, TabbedContent, TabPane
from textual.containers import Horizontal, Vertical, Grid, ScrollableContainer
from textual.binding import Binding

from ..presets import PRESETS, list_categories
from ..widgets.character_portrait import CharacterPortrait, get_portrait


# ASCII art icons for each race
RACE_ICONS = {
    # Transformers (Men)
    "nord": r"""[#a0c4e8]
    ⚔️ ╔═══╗
      ║ N ║
      ╚═══╝[/]""",

    "imperial": r"""[#c9a959]
    👑 ╔═══╗
      ║ I ║
      ╚═══╝[/]""",

    "altmer": r"""[#e8d9a0]
    ✨ ╔═══╗
      ║ A ║
      ╚═══╝[/]""",

    "dragonborn": r"""[#ff6b35]
    🐉 ╔═══╗
      ║ D ║
      ╚═══╝[/]""",

    # Divine (LLaMA)
    "daedra": r"""[#8b0000]
    🔥 ╔═══╗
      ║ Δ ║
      ╚═══╝[/]""",

    "aedra": r"""[#f0e6d2]
    ⭐ ╔═══╗
      ║ Ω ║
      ╚═══╝[/]""",

    # Dwemer (Mamba)
    "dwemer": r"""[#b8860b]
    ⚙️ ╔═══╗
      ║ ⛭ ║
      ╚═══╝[/]""",

    "dwemer_centurion": r"""[#cd853f]
    🤖 ╔═══╗
      ║ C ║
      ╚═══╝[/]""",

    "dwemer_numidium": r"""[#daa520]
    🏛️ ╔═══╗
      ║ Ⓝ ║
      ╚═══╝[/]""",

    # Falmer (Hybrid)
    "falmer": r"""[#708090]
    🦇 ╔═══╗
      ║ F ║
      ╚═══╝[/]""",

    "falmer_warmonger": r"""[#4a4a4a]
    ⚔️ ╔═══╗
      ║ W ║
      ╚═══╝[/]""",

    # Argonian (Linear)
    "argonian": r"""[#228b22]
    🦎 ╔═══╗
      ║ 🜄 ║
      ╚═══╝[/]""",

    "argonian_shadowscale": r"""[#2f4f4f]
    🗡️ ╔═══╗
      ║ S ║
      ╚═══╝[/]""",

    # Khajiit (MoE)
    "khajiit": r"""[#deb887]
    🐱 ╔═══╗
      ║ K ║
      ╚═══╝[/]""",

    "khajiit_mane": r"""[#f4a460]
    👑 ╔═══╗
      ║ M ║
      ╚═══╝[/]""",

    # Bosmer (nGPT)
    "bosmer": r"""[#6b8e23]
    🌲 ╔═══╗
      ║ B ║
      ╚═══╝[/]""",

    # Custom
    "custom": r"""[#7a6e5a]
    🔧 ╔═══╗
      ║ ? ║
      ╚═══╝[/]""",
}


HEADER_ART = r"""[bold #c9a959]
╔══════════════════════════════════════════════════════════════════════════════╗
║  ▄████▄   ██░ ██  ▒█████   ▒█████    ██████ ▓█████    ▓██   ██▓ ▒█████       ║
║ ▒██▀ ▀█  ▓██░ ██▒▒██▒  ██▒▒██▒  ██▒▒██    ▒ ▓█   ▀     ▒██  ██▒▒██▒  ██▒     ║
║ ▒▓█    ▄ ▒██▀▀██░▒██░  ██▒▒██░  ██▒░ ▓██▄   ▒███        ▒██ ██░▒██░  ██▒     ║
║ ▒▓▓▄ ▄██▒░▓█ ░██ ▒██   ██░▒██   ██░  ▒   ██▒▒▓█  ▄      ░ ▐██▓░▒██   ██░     ║
║ ▒ ▓███▀ ░░▓█▒░██▓░ ████▓▒░░ ████▓▒░▒██████▒▒░▒████▒     ░ ██▒▓░░ ████▓▒░     ║
║ ░ ░▒ ▒  ░ ▒ ░░▒░▒░ ▒░▒░▒░ ░ ▒░▒░▒░ ▒ ▒▓▒ ▒ ░░░ ▒░ ░      ██▒▒▒ ░ ▒░▒░▒░      ║
║                        ██▀███   ▄▄▄       ▄████▄  ▓█████                      ║
║                       ▓██ ▒ ██▒▒████▄    ▒██▀ ▀█  ▓█   ▀                      ║
║                       ▓██ ░▄█ ▒▒██  ▀█▄  ▒▓█    ▄ ▒███                        ║
║                       ▒██▀▀█▄  ░██▄▄▄▄██ ▒▓▓▄ ▄██▒▒▓█  ▄                      ║
║                       ░██▓ ▒██▒ ▓█   ▓██▒▒ ▓███▀ ░░▒████▒                     ║
║                       ░ ▒▓ ░▒▓░ ▒▒   ▓▒█░░ ░▒ ▒  ░░░ ▒░ ░                     ║
╚══════════════════════════════════════════════════════════════════════════════╝
[/]"""


# Category colors and descriptions
CATEGORY_INFO = {
    "Transformer": {
        "color": "#c9a959",
        "icon": "⚡",
        "description": "Classic attention-based architectures",
    },
    "Mamba": {
        "color": "#b8860b",
        "icon": "⚙️",
        "description": "State space models with O(n) complexity",
    },
    "Hybrid": {
        "color": "#708090",
        "icon": "🔀",
        "description": "Alternating attention and linear layers",
    },
    "Linear Attention": {
        "color": "#228b22",
        "icon": "🌊",
        "description": "Efficient linear attention mechanisms",
    },
    "Mixture of Experts": {
        "color": "#deb887",
        "icon": "👥",
        "description": "Sparse expert routing for efficiency",
    },
    "Normalized": {
        "color": "#6b8e23",
        "icon": "⚖️",
        "description": "nGPT-style normalized architectures",
    },
    "Custom": {
        "color": "#7a6e5a",
        "icon": "🔧",
        "description": "Build your own architecture",
    },
}


class RaceCard(Button):
    """A selectable race card showing model preset info."""

    DEFAULT_CSS = """
    RaceCard {
        width: 34;
        height: 11;
        background: #2a1f14;
        border: tall #5a4a32;
        padding: 0 1;
        margin: 1;
        content-align: center top;
    }

    RaceCard:hover {
        background: #3d2e1f;
        border: tall #6a5a42;
    }

    RaceCard:focus {
        background: #3d2e1f;
        border: double #c9a959;
    }

    RaceCard.-selected {
        border: double #c9a959;
        background: #3d2e1f;
    }
    """

    def __init__(self, race_key: str, race_info: dict) -> None:
        self.race_key = race_key
        self.race_info = race_info

        # Build the card content with icon
        display_name = race_info["display_name"]
        model_name = race_info["model_name"]
        params = race_info["params"]
        icon = RACE_ICONS.get(race_key, "")

        # Truncate long model names
        if len(model_name) > 18:
            model_name = model_name[:15] + "..."

        label = f"""{icon}
[bold #c9a959]━ {display_name.upper()} ━[/]
[#8b7355]{model_name}[/]
[#d4c4a8]{params}[/]"""

        super().__init__(label, id=f"race-{race_key}")


class RaceSelectScreen(Screen):
    """Screen for selecting model race/preset."""

    BINDINGS = [
        Binding("enter", "select_race", "Select", show=True),
        Binding("escape", "back", "Back", show=True),
        Binding("c", "select_custom", "Custom", show=True),
        Binding("1", "tab_transformer", "Transformer", show=False),
        Binding("2", "tab_mamba", "Mamba", show=False),
        Binding("3", "tab_hybrid", "Hybrid", show=False),
        Binding("4", "tab_moe", "MoE", show=False),
    ]

    DEFAULT_CSS = """
    RaceSelectScreen {
        background: #1a1512;
        overflow: hidden;
    }

    #race-header {
        width: 100%;
        height: auto;
        text-align: center;
    }

    #race-main-content {
        width: 100%;
        height: 1fr;
    }

    #race-tabs {
        width: 1fr;
        height: 100%;
    }

    TabbedContent {
        background: #1a1512;
    }

    TabPane {
        padding: 0;
    }

    ContentSwitcher {
        background: #1a1512;
    }

    #race-grid {
        width: 100%;
        height: auto;
        align: center top;
        grid-size: 4;
        grid-gutter: 1;
        padding: 1 2;
    }

    .race-grid-3 {
        grid-size: 3;
    }

    .race-grid-2 {
        grid-size: 2;
    }

    #race-info-panel {
        width: 30;
        height: 100%;
        background: #2a1f14;
        border-left: heavy #5a4a32;
        padding: 0;
    }

    #race-portrait-container {
        width: 100%;
        height: auto;
        padding: 0;
        align: center top;
    }

    #race-portrait {
        width: auto;
        height: auto;
        text-align: center;
        padding: 0;
    }

    #race-lore-panel {
        width: 100%;
        height: auto;
        padding: 1;
        border-top: heavy #5a4a32;
    }

    #race-lore-title {
        color: #c9a959;
        text-style: bold;
        text-align: center;
    }

    #race-lore-text {
        color: #7a6e5a;
        text-style: italic;
        padding: 1 0;
    }

    #race-bonuses {
        color: #d4c4a8;
    }

    #race-bonuses-label {
        color: #8b7355;
        padding-top: 1;
    }

    .separator {
        color: #5a4a32;
        text-align: center;
        width: 100%;
    }

    .category-header {
        color: #c9a959;
        text-align: center;
        width: 100%;
        padding: 1 0;
        text-style: bold;
    }

    Tabs {
        background: #2a1f14;
        dock: top;
    }

    Tab {
        background: #2a1f14;
        color: #8b7355;
        padding: 1 2;
    }

    Tab:hover {
        background: #3d2e1f;
    }

    Tab.-active {
        background: #3d2e1f;
        color: #c9a959;
        text-style: bold;
    }

    TabPane > ScrollableContainer {
        background: #1a1512;
    }
    """

    def __init__(self) -> None:
        super().__init__()
        self.selected_race = "nord"

    def compose(self) -> ComposeResult:
        """Compose the race selection screen."""
        yield Static(HEADER_ART, id="race-header", markup=True)

        with Horizontal(id="race-main-content"):
            with TabbedContent(id="race-tabs"):
                # Transformer tab (Men, Elves, Divine)
                with TabPane("⚡ Transformer", id="tab-transformer"):
                    with ScrollableContainer():
                        with Grid(id="race-grid"):
                            for race_key in ["nord", "imperial", "altmer", "dragonborn", "daedra", "aedra"]:
                                yield RaceCard(race_key, PRESETS[race_key])

                # Mamba tab (Dwemer)
                with TabPane("⚙️ Mamba/SSM", id="tab-mamba"):
                    with ScrollableContainer():
                        with Grid(id="race-grid", classes="race-grid-3"):
                            for race_key in ["dwemer", "dwemer_centurion", "dwemer_numidium"]:
                                yield RaceCard(race_key, PRESETS[race_key])

                # Hybrid tab (Falmer)
                with TabPane("🔀 Hybrid", id="tab-hybrid"):
                    with ScrollableContainer():
                        with Grid(id="race-grid", classes="race-grid-2"):
                            for race_key in ["falmer", "falmer_warmonger"]:
                                yield RaceCard(race_key, PRESETS[race_key])

                # Linear Attention tab (Argonian)
                with TabPane("🌊 Linear", id="tab-linear"):
                    with ScrollableContainer():
                        with Grid(id="race-grid", classes="race-grid-2"):
                            for race_key in ["argonian", "argonian_shadowscale"]:
                                yield RaceCard(race_key, PRESETS[race_key])

                # MoE tab (Khajiit)
                with TabPane("👥 MoE", id="tab-moe"):
                    with ScrollableContainer():
                        with Grid(id="race-grid", classes="race-grid-2"):
                            for race_key in ["khajiit", "khajiit_mane"]:
                                yield RaceCard(race_key, PRESETS[race_key])

                # Normalized tab (Bosmer)
                with TabPane("⚖️ nGPT", id="tab-ngpt"):
                    with ScrollableContainer():
                        with Grid(id="race-grid", classes="race-grid-2"):
                            yield RaceCard("bosmer", PRESETS["bosmer"])
                            yield RaceCard("custom", PRESETS["custom"])

            # Right panel with portrait and lore
            with Vertical(id="race-info-panel"):
                with Vertical(id="race-portrait-container"):
                    yield Static(get_portrait("nord"), id="race-portrait", markup=True)
                with Vertical(id="race-lore-panel"):
                    yield Static("", id="race-lore-title")
                    yield Static("", id="race-lore-text")
                    yield Static("Racial Bonuses:", id="race-bonuses-label")
                    yield Static("", id="race-bonuses")

        yield Footer()

    def on_mount(self) -> None:
        """Focus the first race card on mount."""
        self.update_lore_display("nord")
        try:
            first_card = self.query_one("#race-nord", RaceCard)
            first_card.focus()
        except Exception:
            pass

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle race card selection."""
        if isinstance(event.button, RaceCard):
            self.selected_race = event.button.race_key
            self.update_lore_display(self.selected_race)
            self._select_current_race()

    def on_race_card_focus(self, event) -> None:
        """Update lore when a race card is focused."""
        pass  # Handled by watch

    def watch_focused(self, focused) -> None:
        """Watch for focus changes to update lore display."""
        if focused and isinstance(focused, RaceCard):
            self.selected_race = focused.race_key
            self.update_lore_display(self.selected_race)

    def on_descendant_focus(self, event) -> None:
        """Update lore when focus changes."""
        if hasattr(event, "widget") and isinstance(event.widget, RaceCard):
            self.selected_race = event.widget.race_key
            self.update_lore_display(self.selected_race)

    def update_lore_display(self, race_key: str) -> None:
        """Update the lore display and portrait for the selected race."""
        race_info = PRESETS.get(race_key, PRESETS["custom"])
        category = race_info.get("category", "Custom")
        cat_info = CATEGORY_INFO.get(category, CATEGORY_INFO["Custom"])

        # Update portrait
        portrait = self.query_one("#race-portrait", Static)
        portrait.update(get_portrait(race_key))

        # Update title
        title = self.query_one("#race-lore-title", Static)
        title.update(f"[{cat_info['color']}]{race_info['display_name']}[/]")

        # Update lore
        lore = self.query_one("#race-lore-text", Static)
        lore.update(race_info["lore"])

        # Update bonuses
        bonuses = self.query_one("#race-bonuses", Static)
        bonus_list = "\n".join(f"  [#6b8e23]+[/] {b}" for b in race_info["bonuses"])
        bonuses.update(bonus_list)

    def action_select_race(self) -> None:
        """Select the currently focused race."""
        self._select_current_race()

    def action_select_custom(self) -> None:
        """Quick select custom race."""
        self.selected_race = "custom"
        self._select_current_race()

    def action_back(self) -> None:
        """Go back to title screen."""
        self.app.pop_screen()

    def action_tab_transformer(self) -> None:
        """Switch to transformer tab."""
        tabs = self.query_one(TabbedContent)
        tabs.active = "tab-transformer"

    def action_tab_mamba(self) -> None:
        """Switch to mamba tab."""
        tabs = self.query_one(TabbedContent)
        tabs.active = "tab-mamba"

    def action_tab_hybrid(self) -> None:
        """Switch to hybrid tab."""
        tabs = self.query_one(TabbedContent)
        tabs.active = "tab-hybrid"

    def action_tab_moe(self) -> None:
        """Switch to MoE tab."""
        tabs = self.query_one(TabbedContent)
        tabs.active = "tab-moe"

    def _select_current_race(self) -> None:
        """Load the selected race and continue to attributes."""
        self.app.load_preset(self.selected_race)
        self.app.goto_attributes()
