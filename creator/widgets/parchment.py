"""
Parchment - Aged parchment-style container widget.
"""

from textual.containers import Container
from textual.widgets import Static


class Parchment(Container):
    """A styled container that looks like aged parchment with dragon borders."""

    DEFAULT_CSS = """
    Parchment {
        background: #2a1f14;
        border: tall #5a4a32;
        padding: 1 2;
        margin: 1;
    }

    Parchment:focus-within {
        border: tall #6a5a42;
    }

    Parchment > .parchment-title {
        color: #c9a959;
        text-style: bold;
        text-align: center;
        padding-bottom: 1;
        width: 100%;
    }
    """

    def __init__(
        self,
        *children,
        title: str = "",
        id: str | None = None,
        classes: str | None = None,
    ) -> None:
        super().__init__(*children, id=id, classes=classes)
        self._title = title

    def compose(self):
        """Compose the parchment with optional title."""
        if self._title:
            yield Static(self._title, classes="parchment-title")


class DragonBorder(Container):
    """A container with heavy dragon-style borders."""

    DEFAULT_CSS = """
    DragonBorder {
        background: #2a1f14;
        border: heavy #5a4a32;
        border-title-color: #c9a959;
        border-title-style: bold;
        padding: 1 2;
        margin: 1;
    }

    DragonBorder:focus-within {
        border: heavy #c9a959;
    }
    """

    def __init__(
        self,
        *children,
        title: str = "",
        id: str | None = None,
        classes: str | None = None,
    ) -> None:
        super().__init__(*children, id=id, classes=classes)
        if title:
            self.border_title = title
