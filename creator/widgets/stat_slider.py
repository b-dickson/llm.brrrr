"""
StatSlider - Enhanced Skyrim-style stat slider widget with color gradients.
"""

from textual.widgets import Static
from textual.reactive import reactive
from textual.message import Message
from textual.binding import Binding


class StatSlider(Static, can_focus=True):
    """A Skyrim-style slider for numeric values with animated gold bar visualization."""

    BINDINGS = [
        Binding("left", "decrement", "Decrease", show=False),
        Binding("right", "increment", "Increase", show=False),
        Binding("h", "decrement", "Decrease", show=False),
        Binding("l", "increment", "Increase", show=False),
        Binding("shift+left", "decrement_big", "Decrease (big)", show=False),
        Binding("shift+right", "increment_big", "Increase (big)", show=False),
        Binding("H", "decrement_big", "Decrease (big)", show=False),
        Binding("L", "increment_big", "Increase (big)", show=False),
        Binding("home", "set_min", "Set to minimum", show=False),
        Binding("end", "set_max", "Set to maximum", show=False),
    ]

    DEFAULT_CSS = """
    StatSlider {
        height: 1;
        padding: 0 1;
    }

    StatSlider:focus {
        background: #3d2e1f;
    }

    StatSlider:focus .slider-bar {
        text-style: bold;
    }
    """

    value = reactive(0)

    class Changed(Message):
        """Emitted when the slider value changes."""

        def __init__(self, slider: "StatSlider", value: int) -> None:
            self.slider = slider
            self.value = value
            super().__init__()

    def __init__(
        self,
        label: str,
        min_val: int,
        max_val: int,
        initial: int,
        step: int = 1,
        big_step: int | None = None,
        suffix: str = "",
        show_pct: bool = False,
        color_gradient: bool = True,
        id: str | None = None,
        classes: str | None = None,
    ) -> None:
        super().__init__(id=id, classes=classes, markup=True)
        self.label = label
        self.min_val = min_val
        self.max_val = max_val
        self.step = step
        self.big_step = big_step or step * 10
        self.suffix = suffix
        self.show_pct = show_pct
        self.color_gradient = color_gradient
        self.value = max(min_val, min(initial, max_val))

    def render(self) -> str:
        """Render the slider with gradient gold bar visualization."""
        # Calculate bar fill percentage
        if self.max_val == self.min_val:
            pct = 1.0
        else:
            pct = (self.value - self.min_val) / (self.max_val - self.min_val)

        bar_width = 20
        filled = int(pct * bar_width)
        empty = bar_width - filled

        # Choose bar color based on fill level
        if self.color_gradient:
            if pct < 0.25:
                bar_color = "#6b8e23"  # Green (low)
                bar_char = "▓"
            elif pct < 0.5:
                bar_color = "#c9a959"  # Gold (medium-low)
                bar_char = "█"
            elif pct < 0.75:
                bar_color = "#daa520"  # Darker gold (medium-high)
                bar_char = "█"
            elif pct < 0.9:
                bar_color = "#ff6b35"  # Orange (high)
                bar_char = "█"
            else:
                bar_color = "#ff4500"  # Red-orange (very high)
                bar_char = "█"
        else:
            bar_color = "#c9a959"
            bar_char = "█"

        # Build the bar with gradient effect
        bar = f"[{bar_color}]{bar_char * filled}[/][#3d2e1f]{'░' * empty}[/]"

        # Format value string
        if self.show_pct:
            value_str = f"{int(pct * 100)}%"
        else:
            if self.value >= 1_000_000:
                value_str = f"{self.value / 1_000_000:.1f}M{self.suffix}"
            elif self.value >= 10_000:
                value_str = f"{self.value / 1_000:.0f}K{self.suffix}"
            elif self.value >= 1_000:
                value_str = f"{self.value / 1_000:.1f}K{self.suffix}"
            else:
                value_str = f"{self.value:,}{self.suffix}"

        # Highlight label when focused
        is_focused = self.has_focus
        label_color = "#c9a959" if is_focused else "#d4c4a8"
        value_color = "#e8d9a0" if is_focused else "#d4c4a8"

        # Arrow indicators when focused
        left_arrow = "[#5a4a32]◀[/] " if is_focused else "  "
        right_arrow = " [#5a4a32]▶[/]" if is_focused else "  "

        # Format with fixed widths for alignment
        return f"[{label_color}]{self.label:<20}[/] {left_arrow}{bar}{right_arrow} [{value_color}]{value_str:>8}[/]"

    def action_increment(self) -> None:
        """Increase the value by step."""
        new_val = min(self.value + self.step, self.max_val)
        if new_val != self.value:
            self.value = new_val
            self.post_message(self.Changed(self, self.value))

    def action_decrement(self) -> None:
        """Decrease the value by step."""
        new_val = max(self.value - self.step, self.min_val)
        if new_val != self.value:
            self.value = new_val
            self.post_message(self.Changed(self, self.value))

    def action_increment_big(self) -> None:
        """Increase the value by big step."""
        new_val = min(self.value + self.big_step, self.max_val)
        if new_val != self.value:
            self.value = new_val
            self.post_message(self.Changed(self, self.value))

    def action_decrement_big(self) -> None:
        """Decrease the value by big step."""
        new_val = max(self.value - self.big_step, self.min_val)
        if new_val != self.value:
            self.value = new_val
            self.post_message(self.Changed(self, self.value))

    def action_set_min(self) -> None:
        """Set to minimum value."""
        if self.value != self.min_val:
            self.value = self.min_val
            self.post_message(self.Changed(self, self.value))

    def action_set_max(self) -> None:
        """Set to maximum value."""
        if self.value != self.max_val:
            self.value = self.max_val
            self.post_message(self.Changed(self, self.value))

    def set_value(self, value: int) -> None:
        """Set the slider value directly."""
        new_val = max(self.min_val, min(value, self.max_val))
        if new_val != self.value:
            self.value = new_val
            self.refresh()

    def watch_value(self, value: int) -> None:
        """Update display when value changes."""
        self.refresh()


class CompactStatSlider(Static, can_focus=True):
    """A more compact stat slider for dense layouts."""

    BINDINGS = [
        Binding("left", "decrement", show=False),
        Binding("right", "increment", show=False),
        Binding("shift+left", "decrement_big", show=False),
        Binding("shift+right", "increment_big", show=False),
    ]

    DEFAULT_CSS = """
    CompactStatSlider {
        height: 1;
        padding: 0;
    }

    CompactStatSlider:focus {
        background: #3d2e1f;
    }
    """

    value = reactive(0)

    class Changed(Message):
        def __init__(self, slider: "CompactStatSlider", value: int) -> None:
            self.slider = slider
            self.value = value
            super().__init__()

    def __init__(
        self,
        label: str,
        min_val: int,
        max_val: int,
        initial: int,
        step: int = 1,
        id: str | None = None,
    ) -> None:
        super().__init__(id=id, markup=True)
        self.label = label
        self.min_val = min_val
        self.max_val = max_val
        self.step = step
        self.value = max(min_val, min(initial, max_val))

    def render(self) -> str:
        pct = (self.value - self.min_val) / (self.max_val - self.min_val) if self.max_val > self.min_val else 0
        bar_width = 8
        filled = int(pct * bar_width)

        bar = f"[#c9a959]{'█' * filled}[/][#3d2e1f]{'░' * (bar_width - filled)}[/]"
        color = "#c9a959" if self.has_focus else "#8b7355"

        return f"[{color}]{self.label}[/] [{bar}] [#d4c4a8]{self.value}[/]"

    def action_increment(self) -> None:
        new_val = min(self.value + self.step, self.max_val)
        if new_val != self.value:
            self.value = new_val
            self.post_message(self.Changed(self, self.value))

    def action_decrement(self) -> None:
        new_val = max(self.value - self.step, self.min_val)
        if new_val != self.value:
            self.value = new_val
            self.post_message(self.Changed(self, self.value))

    def action_increment_big(self) -> None:
        new_val = min(self.value + self.step * 10, self.max_val)
        if new_val != self.value:
            self.value = new_val
            self.post_message(self.Changed(self, self.value))

    def action_decrement_big(self) -> None:
        new_val = max(self.value - self.step * 10, self.min_val)
        if new_val != self.value:
            self.value = new_val
            self.post_message(self.Changed(self, self.value))
