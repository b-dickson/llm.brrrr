"""
Skyrim Theme — The Colors of Tamriel
=====================================

A weathered-parchment, gold-leaf, leather-bound aesthetic for the LLMRIM TUI.

The palette is intentionally restrained: deep leather backgrounds, two tones
of gold for accents and focus, bronze for secondary text, and a small set of
elemental colors (fire/frost/forest/arcane) for the standing-stone screen.

Inspired by aged manuscripts: layered tans, low-saturation backgrounds, sharp
gold accents only on what matters. Atmosphere first, decoration second.
"""

# ---------------------------------------------------------------------------
# Color tokens
# ---------------------------------------------------------------------------

COLORS = {
    # Backgrounds — deep leather, layered for depth.
    "leather_void":   "#0e0a06",  # the lowest layer, near-black
    "leather_deep":   "#15100a",  # screen background
    "leather":        "#1c160e",  # cards / panels
    "leather_light":  "#26200f",  # focus / hover
    "leather_glow":   "#322a17",  # active / pressed

    # Gold leaf — the only "loud" color in the palette.
    "gold":           "#c9a959",
    "gold_bright":    "#ffd266",
    "gold_pale":      "#e8d9a0",
    "gold_dark":      "#8a6f2c",

    # Bronze for secondary text & ornament.
    "bronze":         "#8b7355",
    "bronze_light":   "#a18762",
    "bronze_dark":    "#5a4a32",

    # Parchment text hierarchy.
    "ink_bright":     "#f4e8c8",  # primary
    "ink":            "#d4c4a8",  # body
    "ink_muted":      "#7a6e5a",  # tertiary
    "ink_faint":      "#4d3e2a",  # decorative

    # Borders.
    "border":         "#5a4a32",
    "border_warm":    "#6a5a42",
    "border_glow":    "#c9a959",

    # Elemental accents — used sparingly on the standing-stone screen.
    "fire":           "#ff6b35",
    "fire_dark":      "#a8421f",
    "frost":          "#a0c4e8",
    "frost_dark":     "#4a6e8e",
    "forest":         "#3e7a2c",
    "forest_dark":    "#244a18",
    "hist":           "#228b22",
    "arcane":         "#7b68ee",
    "blood":          "#7a1818",
}


# ---------------------------------------------------------------------------
# Stylesheet
# ---------------------------------------------------------------------------

SKYRIM_CSS = """
/* ==========================================================================
   THE ELDER MODELS V: LLMRIM
   Aged parchment, gold leaf, leather binding.
   ========================================================================== */

/* === Globals =============================================================  */
Screen {
    background: #15100a;
    color: #d4c4a8;
}

/* === Typography ==========================================================  */
.title {
    text-style: bold;
    color: #c9a959;
    text-align: center;
}

.subtitle {
    color: #8b7355;
    text-style: italic;
    text-align: center;
}

.dramatic {
    color: #ffd266;
    text-style: bold italic;
    text-align: center;
}

.lore-text {
    color: #7a6e5a;
    text-style: italic;
}

/* === Containers ==========================================================  */
.parchment {
    background: #1c160e;
    border: tall #5a4a32;
    padding: 1 2;
}

.dragon-border {
    border: heavy #5a4a32;
    border-title-color: #c9a959;
    border-title-style: bold;
    background: #1c160e;
    padding: 1 2;
}

.dragon-border:focus-within {
    border: heavy #c9a959;
}

Container,
Horizontal,
Vertical {
    background: transparent;
}

Static {
    background: transparent;
    color: #d4c4a8;
}

/* === Buttons =============================================================  */
Button {
    background: #1c160e;
    color: #d4c4a8;
    border: tall #5a4a32;
    padding: 0 2;
}

Button:hover {
    background: #26200f;
    color: #e8d9a0;
    border: tall #6a5a42;
}

Button:focus {
    background: #322a17;
    color: #ffd266;
    border: tall #c9a959;
    text-style: bold;
}

Button.-primary {
    background: #322a17;
    color: #ffd266;
    border: tall #c9a959;
    text-style: bold;
}

Button.-primary:hover {
    background: #4a3a1a;
    color: #ffd266;
    border: tall #ffd266;
}

/* === Inputs ==============================================================  */
Input {
    background: #1c160e;
    color: #f4e8c8;
    border: tall #5a4a32;
    padding: 0 1;
}

Input:focus {
    border: tall #c9a959;
    background: #26200f;
    color: #ffd266;
}

/* === Labels ==============================================================  */
Label {
    color: #d4c4a8;
}

.label-gold {
    color: #c9a959;
    text-style: bold;
}

.label-muted {
    color: #7a6e5a;
}

.label-bright {
    color: #f4e8c8;
}

/* === Selection / Option lists ============================================  */
SelectionList,
OptionList {
    background: #1c160e;
    border: tall #5a4a32;
    padding: 0 1;
}

SelectionList:focus,
OptionList:focus {
    border: tall #c9a959;
}

SelectionList > .selection-list--option-highlighted,
OptionList > .option-list--option-highlighted {
    background: #322a17;
    color: #ffd266;
    text-style: bold;
}

SelectionList > .selection-list--option-selected {
    color: #c9a959;
}

/* === Radio / Checkbox ====================================================  */
RadioButton,
Checkbox {
    background: transparent;
    color: #d4c4a8;
    padding: 0 1;
}

RadioButton:focus,
Checkbox:focus {
    color: #ffd266;
}

RadioButton.-on,
Checkbox.-on {
    color: #c9a959;
    text-style: bold;
}

RadioSet {
    background: transparent;
    border: none;
    padding: 0;
    height: auto;
}

/* === Tabs ================================================================  */
TabbedContent {
    background: #15100a;
}

TabPane {
    background: #15100a;
    padding: 1;
}

Tabs {
    background: #1c160e;
}

Tab {
    background: #1c160e;
    color: #7a6e5a;
    padding: 1 3;
}

Tab:hover {
    background: #26200f;
    color: #d4c4a8;
}

Tab.-active {
    background: #322a17;
    color: #ffd266;
    text-style: bold;
}

/* === Scrollbars ==========================================================  */
Scrollbar {
    background: #1c160e;
}

Scrollbar > .scrollbar--bar {
    background: #5a4a32;
}

Scrollbar > .scrollbar--bar:hover {
    background: #c9a959;
}

/* === Data tables =========================================================  */
DataTable {
    background: #1c160e;
    border: tall #5a4a32;
}

DataTable > .datatable--header {
    background: #322a17;
    color: #c9a959;
    text-style: bold;
}

DataTable > .datatable--cursor {
    background: #4a3a1a;
    color: #ffd266;
}

/* === Header / Footer ====================================================  */
Header {
    background: #1c160e;
    color: #c9a959;
}

Footer {
    background: #1c160e;
    color: #7a6e5a;
}

Footer > .footer--key {
    color: #ffd266;
    background: #322a17;
    text-style: bold;
}

Footer > .footer--description {
    color: #d4c4a8;
}

Footer > .footer--highlight {
    background: #4a3a1a;
    color: #ffd266;
}

/* === Collapsible =========================================================  */
Collapsible {
    background: #1c160e;
    border: tall #5a4a32;
    padding: 0;
    margin: 1;
}

Collapsible:focus-within {
    border: tall #c9a959;
}

CollapsibleTitle {
    color: #c9a959;
    background: #1c160e;
    padding: 0 1;
}

CollapsibleTitle:hover {
    background: #322a17;
    color: #ffd266;
}

CollapsibleTitle:focus {
    background: #322a17;
    color: #ffd266;
    text-style: bold;
}

/* === Misc ================================================================  */
RichLog,
TextArea {
    background: #1c160e;
    border: tall #5a4a32;
    color: #d4c4a8;
    padding: 1;
}

RichLog:focus,
TextArea:focus {
    border: tall #c9a959;
}

ProgressBar > .bar--bar {
    color: #c9a959;
    background: #322a17;
}

ProgressBar > .bar--complete {
    color: #ffd266;
}

/* === Notifications =======================================================  */
Toast {
    background: #1c160e;
    border: heavy #c9a959;
    color: #f4e8c8;
}

Toast.-information {
    border: heavy #c9a959;
}

Toast.-warning {
    border: heavy #ff6b35;
}

Toast.-error {
    border: heavy #7a1818;
}
"""


# ---------------------------------------------------------------------------
# Ornamental separators (used by various screens)
# ---------------------------------------------------------------------------

ORNAMENT_HEAVY   = "═══════════════════════════════════════════════════════════"
ORNAMENT_LIGHT   = "───────────────────────────────────────────────────────────"
ORNAMENT_DOTTED  = "· · · · · · · · · · · · · · · · · · · · · · · · · · · · · ·"
ORNAMENT_DIAMOND = "◆ ─ ◆ ─ ◆ ─ ◆ ─ ◆ ─ ◆ ─ ◆ ─ ◆ ─ ◆ ─ ◆ ─ ◆ ─ ◆ ─ ◆"
ORNAMENT_RUNIC   = "᛫ ᛫ ᛫ ᛬ ᛫ ᛫ ᛫ ᛬ ᛫ ᛫ ᛫ ᛬ ᛫ ᛫ ᛫ ᛬ ᛫ ᛫ ᛫ ᛬ ᛫ ᛫ ᛫"
ORNAMENT_SCROLL  = "⊰═══━━━─◆─━━━═══⊱"
ORNAMENT_DRAGON  = "▼━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━▼"

DRAGON_SEPARATOR = ORNAMENT_HEAVY
"""Backwards-compat alias for older imports."""
