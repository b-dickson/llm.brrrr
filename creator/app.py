"""
LLMRIM - The Elder Models V
Main application class.
"""

from textual.app import App
from textual.binding import Binding

from .config import ModelConfig
from .presets import PRESETS, get_preset
from .theme import SKYRIM_CSS


class LLMRIMApp(App):
    """The Elder Models V: LLMRIM - Skyrim-style LLM Architecture Creator."""

    CSS = SKYRIM_CSS
    TITLE = "LLMRIM"
    SUB_TITLE = "The Elder Models V"

    BINDINGS = [
        Binding("q", "quit", "Quit", show=True),
        Binding("escape", "back", "Back", show=True),
        Binding("?", "help", "Help", show=False),
    ]

    def __init__(self):
        super().__init__()
        self.config = ModelConfig()
        self.selected_race = "custom"

    def on_mount(self) -> None:
        """Start with title screen."""
        from .screens.title_screen import TitleScreen
        self.push_screen(TitleScreen())

    def action_back(self) -> None:
        """Go back to previous screen."""
        if len(self.screen_stack) > 1:
            self.pop_screen()

    def action_help(self) -> None:
        """Show help."""
        self.notify(
            "Arrow keys to navigate, Enter to select, Escape to go back",
            title="Help",
        )

    # === Screen Navigation ===

    def goto_race_select(self) -> None:
        """Navigate to race selection screen."""
        from .screens.race_select import RaceSelectScreen
        self.push_screen(RaceSelectScreen())

    def goto_attributes(self) -> None:
        """Navigate to attributes customization screen."""
        from .screens.attributes import AttributesScreen
        self.push_screen(AttributesScreen())

    def goto_standing_stones(self) -> None:
        """Navigate to standing stones (advanced options) screen."""
        from .screens.standing_stones import StandingStonesScreen
        self.push_screen(StandingStonesScreen())

    def goto_summary(self) -> None:
        """Navigate to summary and generation screen."""
        from .screens.summary import SummaryScreen
        self.push_screen(SummaryScreen())

    # === Configuration Management ===

    def load_preset(self, race_name: str) -> None:
        """Load a preset configuration by race name."""
        self.selected_race = race_name.lower()
        self.config = get_preset(race_name)

    def get_race_info(self) -> dict:
        """Get info about the currently selected race."""
        return PRESETS.get(self.selected_race, PRESETS["custom"])


def main():
    """Run the LLMRIM application."""
    app = LLMRIMApp()
    app.run()


if __name__ == "__main__":
    main()
