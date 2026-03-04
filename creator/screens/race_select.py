"""
Race Selection Screen - Choose Your Race
Select from preset model architectures including Transformer, Mamba, MoE,
GatedDeltaNet (native SequenceMixer), and Hybrid.

"Skyrim belongs to the Nords... and so does efficient inference!"
"""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Footer, Button, TabbedContent, TabPane
from textual.containers import Horizontal, Vertical, Grid, ScrollableContainer
from textual.binding import Binding

from ..presets import PRESETS, list_categories
from ..widgets.character_portrait import CharacterPortrait, get_portrait


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
        "description": "Alternating attention and GatedDeltaNet layers",
    },
    "Linear Attention": {
        "color": "#228b22",
        "icon": "🌊",
        "description": "GatedDeltaNet - native SequenceMixer, O(n) linear attention",
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


class RaceCard(Button):
    """A selectable race card showing model preset info."""

    DEFAULT_CSS = """
    RaceCard {
        width: 34;
        height: 9;
        background: #231b13;
        border: tall #5a4a32;
        padding: 0 1;
        margin: 1;
        content-align: center top;
    }

    RaceCard:hover {
        background: #2a1f14;
        border: tall #8b7355;
    }

    RaceCard:focus {
        background: #2a1f14;
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

        display_name = race_info["display_name"]
        model_name = race_info["model_name"]
        params = race_info["params"]
        category = race_info.get("category", "Custom")
        cat_info = CATEGORY_INFO.get(category, CATEGORY_INFO["Custom"])
        color = cat_info["color"]

        # Truncate long model names
        if len(model_name) > 20:
            model_name = model_name[:17] + "..."

        label = f"""[bold {color}]━━ {display_name.upper()} ━━[/]
[#8b7355]{model_name}[/]
[#d4c4a8]{params}[/]
[dim #5a4a32]{'─' * 22}[/]
[{color}]{cat_info['icon']} {category}[/]"""

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
        Binding("4", "tab_linear", "Linear", show=False),
        Binding("5", "tab_moe", "MoE", show=False),
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
        width: 34;
        height: 100%;
        background: #231b13;
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

    #race-lore-model {
        color: #8b7355;
        text-align: center;
        padding-bottom: 1;
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
        text-style: bold;
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
        background: #231b13;
        dock: top;
    }

    Tab {
        background: #231b13;
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

                # Linear Attention tab (Argonian) - Enhanced with Veezara
                with TabPane("🌊 GatedDeltaNet", id="tab-linear"):
                    with ScrollableContainer():
                        with Grid(id="race-grid", classes="race-grid-3"):
                            for race_key in ["argonian", "argonian_shadowscale", "argonian_veezara"]:
                                yield RaceCard(race_key, PRESETS[race_key])

                # Hybrid tab (Falmer)
                with TabPane("🔀 Hybrid", id="tab-hybrid"):
                    with ScrollableContainer():
                        with Grid(id="race-grid", classes="race-grid-2"):
                            for race_key in ["falmer", "falmer_warmonger"]:
                                yield RaceCard(race_key, PRESETS[race_key])

                # MoE tab (Khajiit)
                with TabPane("👥 MoE", id="tab-moe"):
                    with ScrollableContainer():
                        with Grid(id="race-grid", classes="race-grid-2"):
                            for race_key in ["khajiit", "khajiit_mane"]:
                                yield RaceCard(race_key, PRESETS[race_key])

                # Normalized + Custom tab
                with TabPane("⚖️ nGPT/Custom", id="tab-ngpt"):
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
                    yield Static("", id="race-lore-model")
                    yield Static("", id="race-lore-text")
                    yield Static("[#5a4a32]─── Racial Bonuses ───[/]", id="race-bonuses-label", markup=True)
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

        # Update title with category color
        title = self.query_one("#race-lore-title", Static)
        title.update(f"[bold {cat_info['color']}]{race_info['display_name']}[/]")

        # Update model name
        model = self.query_one("#race-lore-model", Static)
        model.update(f"[#8b7355]{race_info['model_name']} ({race_info['params']})[/]")

        # Update lore
        lore = self.query_one("#race-lore-text", Static)
        lore.update(race_info["lore"])

        # Update bonuses
        bonuses = self.query_one("#race-bonuses", Static)
        bonus_list = "\n".join(f"  [{cat_info['color']}]+[/] {b}" for b in race_info["bonuses"])
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
        tabs = self.query_one(TabbedContent)
        tabs.active = "tab-transformer"

    def action_tab_mamba(self) -> None:
        tabs = self.query_one(TabbedContent)
        tabs.active = "tab-mamba"

    def action_tab_hybrid(self) -> None:
        tabs = self.query_one(TabbedContent)
        tabs.active = "tab-hybrid"

    def action_tab_linear(self) -> None:
        tabs = self.query_one(TabbedContent)
        tabs.active = "tab-linear"

    def action_tab_moe(self) -> None:
        tabs = self.query_one(TabbedContent)
        tabs.active = "tab-moe"

    def _select_current_race(self) -> None:
        """Load the selected race and continue to attributes."""
        self.app.load_preset(self.selected_race)
        self.app.goto_attributes()
