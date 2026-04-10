"""
Title Screen — THE ELDER MODELS V: LLMRIM

The first thing the user sees. Big illuminated title, dragon sigil, a random
quote from the Greybeards, and a press-enter prompt. Designed to read at any
terminal size of 100 columns or wider.
"""

from __future__ import annotations

import random

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Center, Vertical
from textual.screen import Screen
from textual.widgets import Footer, Static


# ---------------------------------------------------------------------------
# Art assets — kept tight, centered, and column-aligned
# ---------------------------------------------------------------------------

DRAGON_SIGIL = r"""[#c9a959]
                              ╔═══════╗
                              ║   ◢   ║
                              ║  ◢█◣  ║
                              ╚═◢███◣═╝
                            ╱─◢█████◣─╲
                          ╱─◢███[#ff6b35]◯[/]███◣─╲
                        ╱─◢███████████◣─╲
                       ╱──◢█████████████◣──╲
                      ╱───◢██[#ff6b35]◣[/]█████[#ff6b35]◢[/]██◣───╲
                     │────◢█████████████◣────│
                      ╲───◥█████████████◤───╱
                       ╲──◥███████████◤──╱
                         ╲─◥████████◤─╱
                           ◥◣══◯══◢◤
                              ◥◯◤
                              ─┴─[/]"""


TITLE_ART = r"""[bold #c9a959]
        ████████╗██╗  ██╗███████╗   ███████╗██╗     ██████╗ ███████╗██████╗
        ╚══██╔══╝██║  ██║██╔════╝   ██╔════╝██║     ██╔══██╗██╔════╝██╔══██╗
           ██║   ███████║█████╗     █████╗  ██║     ██║  ██║█████╗  ██████╔╝
           ██║   ██╔══██║██╔══╝     ██╔══╝  ██║     ██║  ██║██╔══╝  ██╔══██╗
           ██║   ██║  ██║███████╗   ███████╗███████╗██████╔╝███████╗██║  ██║
           ╚═╝   ╚═╝  ╚═╝╚══════╝   ╚══════╝╚══════╝╚═════╝ ╚══════╝╚═╝  ╚═╝[/]
[#8b7355]
                ███╗   ███╗ ██████╗ ██████╗ ███████╗██╗     ███████╗
                ████╗ ████║██╔═══██╗██╔══██╗██╔════╝██║     ██╔════╝
                ██╔████╔██║██║   ██║██║  ██║█████╗  ██║     ███████╗
                ██║╚██╔╝██║██║   ██║██║  ██║██╔══╝  ██║     ╚════██║
                ██║ ╚═╝ ██║╚██████╔╝██████╔╝███████╗███████╗███████║
                ╚═╝     ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝╚══════╝╚══════╝[/]
[bold #ffd266]
                            ▼  ━━━  V  ━━━  ▼
                          L · L · M · R · I · M[/]"""


SUBTITLE = (
    "[#8b7355]The Skyrim-themed LLM Architecture Creator · "
    "[#c9a959]olmo-core[/] · "
    "[#228b22]GatedDeltaNet[/] · "
    "[#deb887]MoE[/][/]"
)


DRAMATIC_QUOTES = [
    '"Fus Ro Brrr… your training begins."',
    "\"The Thu'um of computation echoes through the void.\"",
    '"A new architecture stirs in the depths of silicon."',
    '"The Dragonborn of models awakens."',
    "\"In their tongue, it is Dovahkiin — Model-Born!\"",
    '"The Elder Scrolls foretold your creation."',
    '"I used to be a simple perceptron, then I took a gradient to the knee."',
    '"What is better — to be born with good weights, or to overcome poor initialization?"',
    '"The GatedDeltaNet flows like the Hist — O(n), eternal, unyielding."',
    "\"Do you get to train very often? Oh, what am I saying — of course you don't.\"",
    '"The SequenceMixer has spoken. Attention and recurrence are one."',
    '"Let me guess — someone stole your learning rate?"',
    '"Hands off the gradients, sneak thief."',
    '"By the Nine, that\'s a beautiful loss curve."',
    '"The cold doesn\'t bother me. The vanishing gradients, however…"',
]


VERSION_BANNER = (
    "[#5a4a32]◆[/] [#c9a959]v2.5.0[/] [#5a4a32]·[/] "
    "[#8b7355]native GatedDeltaNet SequenceMixer[/] "
    "[#5a4a32]·[/] [#8b7355]olmo-core ≥ 2.5.0[/] [#5a4a32]◆[/]"
)


ORNAMENT = (
    "[#5a4a32]◆[/][#3d2e1f]─[/][#5a4a32]◆[/][#3d2e1f]─[/]"
    "[#c9a959]◆[/][#3d2e1f]─[/][#ffd266]◆[/][#3d2e1f]─[/]"
    "[#c9a959]◆[/][#3d2e1f]─[/][#5a4a32]◆[/][#3d2e1f]─[/]"
    "[#5a4a32]◆[/]"
)


# ---------------------------------------------------------------------------
# Screen
# ---------------------------------------------------------------------------

class TitleScreen(Screen):
    """The dramatic title screen."""

    BINDINGS = [
        Binding("enter", "continue", "Begin", show=True),
        Binding("space", "continue", "Begin", show=False),
        Binding("q", "quit", "Quit", show=True),
    ]

    DEFAULT_CSS = """
    TitleScreen {
        background: #15100a;
        overflow-y: auto;
    }

    #title-container {
        width: 100%;
        height: auto;
        min-height: 100%;
        align: center middle;
    }

    #title-stack {
        width: auto;
        height: auto;
        padding: 1 4;
        align: center middle;
    }

    #title-sigil {
        text-align: center;
        width: auto;
    }

    #title-art {
        text-align: center;
        width: auto;
        padding-top: 1;
    }

    #title-subtitle {
        text-align: center;
        width: 100%;
        padding-top: 1;
    }

    #title-quote {
        color: #c9a959;
        text-align: center;
        text-style: italic;
        padding-top: 2;
    }

    #title-version {
        text-align: center;
        padding-top: 1;
    }

    #title-ornament {
        text-align: center;
        padding-top: 1;
    }

    #title-prompt {
        color: #ffd266;
        text-align: center;
        text-style: bold;
        padding-top: 2;
    }

    #title-hint {
        color: #5a4a32;
        text-align: center;
        padding-top: 0;
    }
    """

    def compose(self) -> ComposeResult:
        quote = random.choice(DRAMATIC_QUOTES)

        with Center(id="title-container"):
            with Vertical(id="title-stack"):
                yield Static(DRAGON_SIGIL, id="title-sigil", markup=True)
                yield Static(TITLE_ART, id="title-art", markup=True)
                yield Static(SUBTITLE, id="title-subtitle", markup=True)
                yield Static(quote, id="title-quote")
                yield Static(VERSION_BANNER, id="title-version", markup=True)
                yield Static(ORNAMENT, id="title-ornament", markup=True)
                yield Static("⊰  Press ENTER to begin your creation  ⊱", id="title-prompt")
                yield Static("(Q to quit)", id="title-hint")

        yield Footer()

    def action_continue(self) -> None:
        self.app.goto_race_select()

    def action_quit(self) -> None:
        self.app.exit()
