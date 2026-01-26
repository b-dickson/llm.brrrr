"""
Title Screen - THE ELDER MODELS V: LLMRIM
Dramatic intro screen with Skyrim-style presentation.
"""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Footer
from textual.containers import Center, Vertical
from textual.binding import Binding
import random


DRAGON_LOGO = r"""
                            [bold #c9a959]
                                   __                  __
                                  /  \                /  \
                               __/    \______________/    \__
                              /                              \
                        _____/    [#ff6b35]●[/]                    [#ff6b35]●[/]    \_____
                       /                                          \
                  ____/                   /\                       \____
                 /                       /  \                           \
            ____/                       /    \                           \____
           /          ___             /      \             ___                \
          /          /   \           /   /\   \           /   \                \
         |          /     \         /   /  \   \         /     \                |
          \        /       \_______/   /    \   \_______/       \              /
           \______/                   /      \                   \____________/
                  \                  /________\                  /
                   \________________/    ||    \________________/
                                        /  \
                                       /    \
                                      /______\
[/]"""

TITLE_ART = r"""[bold #c9a959]
 ▄▄▄█████▓ ██░ ██ ▓█████     ▓█████  ██▓    ▓█████▄ ▓█████  ██▀███
 ▓  ██▒ ▓▒▓██░ ██▒▓█   ▀     ▓█   ▀ ▓██▒    ▒██▀ ██▌▓█   ▀ ▓██ ▒ ██▒
 ▒ ▓██░ ▒░▒██▀▀██░▒███       ▒███   ▒██░    ░██   █▌▒███   ▓██ ░▄█ ▒
 ░ ▓██▓ ░ ░▓█ ░██ ▒▓█  ▄     ▒▓█  ▄ ▒██░    ░▓█▄   ▌▒▓█  ▄ ▒██▀▀█▄
   ▒██▒ ░ ░▓█▒░██▓░▒████▒    ░▒████▒░██████▒░▒████▓ ░▒████▒░██▓ ▒██▒
   ▒ ░░    ▒ ░░▒░▒░░ ▒░ ░    ░░ ▒░ ░░ ▒░▓  ░ ▒▒▓  ▒ ░░ ▒░ ░░ ▒▓ ░▒▓░
     ░     ▒ ░▒░ ░ ░ ░  ░     ░ ░  ░░ ░ ▒  ░ ░ ▒  ▒  ░ ░  ░  ░▒ ░ ▒░
   ░       ░  ░░ ░   ░          ░     ░ ░    ░ ░  ░    ░     ░░   ░
           ░  ░  ░   ░  ░       ░  ░    ░  ░   ░       ░  ░   ░
[/]
[bold #8b7355]
               ███╗   ███╗ ██████╗ ██████╗ ███████╗██╗     ███████╗
               ████╗ ████║██╔═══██╗██╔══██╗██╔════╝██║     ██╔════╝
               ██╔████╔██║██║   ██║██║  ██║█████╗  ██║     ███████╗
               ██║╚██╔╝██║██║   ██║██║  ██║██╔══╝  ██║     ╚════██║
               ██║ ╚═╝ ██║╚██████╔╝██████╔╝███████╗███████╗███████║
               ╚═╝     ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝╚══════╝╚══════╝
[/]
[bold #c9a959]
                              ▄▄       ▄▄
                              ██       ██
                              ▀█▄     ▄█▀
                                ▀▀█████▀▀
                                   ██
                                   ▀▀

                         ██╗     ██╗     ███╗   ███╗██████╗ ██╗███╗   ███╗
                         ██║     ██║     ████╗ ████║██╔══██╗██║████╗ ████║
                         ██║     ██║     ██╔████╔██║██████╔╝██║██╔████╔██║
                         ██║     ██║     ██║╚██╔╝██║██╔══██╗██║██║╚██╔╝██║
                         ███████╗███████╗██║ ╚═╝ ██║██║  ██║██║██║ ╚═╝ ██║
                         ╚══════╝╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚═╝     ╚═╝
[/]"""


DRAMATIC_QUOTES = [
    '"Fus Ro Brrr... Your training begins."',
    '"The Thu\'um of computation echoes through the void."',
    '"A new architecture stirs in the depths of silicon."',
    '"The Dragonborn of models awakens."',
    '"In their tongue, it is Dovahkiin... Model-Born!"',
    '"The Elder Scrolls foretold your creation."',
    '"I used to be a simple perceptron, then I took a gradient to the knee."',
    '"What is better? To be born with good weights, or to overcome poor initialization?"',
    '"The ancient Nords used the Thu\'um to shout at their GPUs."',
    '"Do you get to train very often? Oh, what am I saying, of course you don\'t."',
]


class TitleScreen(Screen):
    """The dramatic title screen for LLMRIM."""

    BINDINGS = [
        Binding("enter", "continue", "Continue", show=True),
        Binding("space", "continue", "Continue", show=False),
        Binding("q", "quit", "Quit", show=True),
    ]

    DEFAULT_CSS = """
    TitleScreen {
        background: #1a1512;
        overflow-y: auto;
    }

    #title-container {
        width: 100%;
        height: auto;
        min-height: 100%;
        align: center middle;
    }

    #title-box {
        width: auto;
        height: auto;
        padding: 1 2;
        align: center middle;
    }

    #dragon-logo {
        text-align: center;
        width: auto;
        padding-bottom: 1;
    }

    #title-art {
        text-align: center;
        width: auto;
    }

    #title-quote {
        color: #7a6e5a;
        text-align: center;
        text-style: italic;
        padding-top: 2;
    }

    #title-prompt {
        color: #5a4a32;
        text-align: center;
        padding-top: 2;
    }

    .dragon-line {
        color: #5a4a32;
        text-align: center;
    }

    .spacer {
        height: 1;
    }
    """

    def compose(self) -> ComposeResult:
        """Compose the title screen."""
        quote = random.choice(DRAMATIC_QUOTES)

        with Center(id="title-container"):
            with Vertical(id="title-box"):
                yield Static(DRAGON_LOGO, id="dragon-logo", markup=True)
                yield Static(TITLE_ART, id="title-art", markup=True)
                yield Static(quote, id="title-quote")
                yield Static("[ Press ENTER to begin your creation ]", id="title-prompt")

        yield Footer()

    def action_continue(self) -> None:
        """Continue to race selection."""
        self.app.goto_race_select()

    def action_quit(self) -> None:
        """Quit the application."""
        self.app.exit()
