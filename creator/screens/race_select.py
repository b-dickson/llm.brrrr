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
   ╔════════════════════════════════════════════════════════════════════════════╗
   ║                                                                            ║
   ║      ◆  C H O O S E    Y O U R    R A C E  ◆                               ║
   ║                                                                            ║
   ║      [#8b7355]The architecture of your soul determines your fate.[/#8b7355]                ║
   ║                                                                            ║
   ╚════════════════════════════════════════════════════════════════════════════╝[/]
[#7a6e5a]                       ━━━ Each race carries its own racial bonus ━━━[/]"""


class RaceCard(Button):
    """A selectable race card showing model preset info."""

    DEFAULT_CSS = """
    RaceCard {
        width: 32;
        height: 9;
        background: #1c160e;
        border: tall #5a4a32;
        padding: 0 1;
        margin: 0 1;
        content-align: center middle;
    }

    RaceCard:hover {
        background: #26200f;
        border: tall #8b7355;
    }

    RaceCard:focus {
        background: #322a17;
        border: double #c9a959;
        text-style: bold;
    }

    RaceCard.-selected {
        border: double #ffd266;
        background: #4a3a1a;
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

        # Truncate long model names so two-column cards never overflow.
        if len(model_name) > 22:
            model_name = model_name[:19] + "…"

        label = (
            f"[bold {color}]◆ {display_name.upper()} ◆[/]\n"
            f"[#8b7355]{model_name}[/]\n"
            f"[#f4e8c8 bold]{params}[/]\n"
            f"[#3d2e1f]{'─' * 24}[/]\n"
            f"[{color}]{cat_info['icon']}  {category}[/]"
        )

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
        Binding("6", "tab_ngpt", "nGPT", show=False),
    ]

    DEFAULT_CSS = """
    RaceSelectScreen {
        background: #15100a;
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
        background: #15100a;
    }

    TabPane {
        padding: 0;
    }

    ContentSwitcher {
        background: #15100a;
    }

    .race-grid {
        width: 100%;
        height: auto;
        align: center top;
        grid-gutter: 1 1;
        padding: 1 2;
    }

    .race-grid-3 {
        grid-size: 3;
    }

    .race-grid-2 {
        grid-size: 2;
    }

    #race-info-panel {
        width: 38;
        height: 100%;
        background: #1c160e;
        border-left: heavy #5a4a32;
        padding: 0;
    }

    #race-portrait-container {
        width: 100%;
        height: auto;
        padding: 1 0 0 0;
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
        height: 1fr;
        padding: 1 2;
        border-top: heavy #5a4a32;
    }

    #race-lore-title {
        color: #ffd266;
        text-style: bold;
        text-align: center;
        padding-bottom: 0;
    }

    #race-lore-model {
        color: #8b7355;
        text-align: center;
        padding-bottom: 1;
    }

    #race-lore-text {
        color: #a18762;
        text-style: italic;
        padding: 1 0;
    }

    #race-bonuses {
        color: #d4c4a8;
    }

    #race-bonuses-label {
        color: #c9a959;
        padding-top: 1;
        text-align: center;
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
        background: #1c160e;
        dock: top;
    }

    Tab {
        background: #1c160e;
        color: #8b7355;
        padding: 1 2;
    }

    Tab:hover {
        background: #322a17;
        color: #d4c4a8;
    }

    Tab.-active {
        background: #322a17;
        color: #ffd266;
        text-style: bold;
    }

    TabPane > ScrollableContainer {
        background: #15100a;
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
                        with Grid(classes="race-grid race-grid-3"):
                            for race_key in [
                                "nord", "imperial", "altmer",
                                "dragonborn", "daedra", "aedra",
                            ]:
                                yield RaceCard(race_key, PRESETS[race_key])

                # Mamba tab (Dwemer)
                with TabPane("⚙ Mamba/SSM", id="tab-mamba"):
                    with ScrollableContainer():
                        with Grid(classes="race-grid race-grid-3"):
                            for race_key in ["dwemer", "dwemer_centurion", "dwemer_numidium"]:
                                yield RaceCard(race_key, PRESETS[race_key])

                # Linear Attention tab (Argonian)
                with TabPane("🜄 GatedDeltaNet", id="tab-linear"):
                    with ScrollableContainer():
                        with Grid(classes="race-grid race-grid-3"):
                            for race_key in [
                                "argonian", "argonian_shadowscale", "argonian_veezara",
                            ]:
                                yield RaceCard(race_key, PRESETS[race_key])

                # Hybrid tab (Falmer)
                with TabPane("⚯ Hybrid", id="tab-hybrid"):
                    with ScrollableContainer():
                        with Grid(classes="race-grid race-grid-2"):
                            for race_key in ["falmer", "falmer_warmonger"]:
                                yield RaceCard(race_key, PRESETS[race_key])

                # MoE tab (Khajiit)
                with TabPane("⚜ MoE", id="tab-moe"):
                    with ScrollableContainer():
                        with Grid(classes="race-grid race-grid-2"):
                            for race_key in ["khajiit", "khajiit_mane"]:
                                yield RaceCard(race_key, PRESETS[race_key])

                # Normalized + Custom tab
                with TabPane("✦ nGPT / Custom", id="tab-ngpt"):
                    with ScrollableContainer():
                        with Grid(classes="race-grid race-grid-2"):
                            yield RaceCard("bosmer", PRESETS["bosmer"])
                            yield RaceCard("custom", PRESETS["custom"])

            # Right panel with portrait and lore
            with Vertical(id="race-info-panel"):
                with Vertical(id="race-portrait-container"):
                    yield Static(get_portrait("nord"), id="race-portrait", markup=True)
                with Vertical(id="race-lore-panel"):
                    yield Static("", id="race-lore-title")
                    yield Static("", id="race-lore-model")
                    yield Static("[#5a4a32]· · · · · · · · · · · · · · · ·[/]", classes="separator", markup=True)
                    yield Static("", id="race-lore-text")
                    yield Static("[#c9a959]◆ Racial Bonuses ◆[/]", id="race-bonuses-label", markup=True)
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

    def action_tab_ngpt(self) -> None:
        tabs = self.query_one(TabbedContent)
        tabs.active = "tab-ngpt"

    def _select_current_race(self) -> None:
        """Load the selected race and continue to attributes."""
        self.app.load_preset(self.selected_race)
        self.app.goto_attributes()
