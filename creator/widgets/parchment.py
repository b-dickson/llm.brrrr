"""
DragonBorder — heavy bordered container with a gold title bar.

Used by every screen as the standard panel-with-title container. The old
``Parchment`` class lived here too but it had a broken ``compose()`` that
silently dropped its children, so it was deleted. If you want a panel, use
``DragonBorder``.
"""

from __future__ import annotations

from textual.containers import Container


class DragonBorder(Container):
    """A container with heavy dragon-style borders and a gold title."""

    DEFAULT_CSS = """
    DragonBorder {
        background: #1c160e;
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
