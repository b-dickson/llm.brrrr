"""
Skyrim Theme - The Colors of Tamriel
CSS theme for the LLMRIM TUI.

Enhanced with deeper atmosphere, richer gradients, and ornate decorative elements.
"""

# Color palette - Deeper, richer, more atmospheric
COLORS = {
    # Core palette
    "gold": "#c9a959",
    "gold_dark": "#a88932",
    "gold_light": "#e8d9a0",
    "gold_bright": "#ffd700",
    # Parchment/leather tones
    "bronze": "#8b7355",
    "leather": "#1a1512",
    "leather_mid": "#231b13",
    "leather_light": "#2a1f14",
    "parchment": "#3d2e1f",
    "parchment_light": "#4d3e2f",
    # Text hierarchy
    "text": "#d4c4a8",
    "text_muted": "#7a6e5a",
    "text_bright": "#f0e6d2",
    "text_dim": "#5a4a32",
    # Borders
    "border": "#5a4a32",
    "border_light": "#6a5a42",
    "border_glow": "#8b7355",
    # Accents
    "danger": "#8b0000",
    "danger_light": "#a52a2a",
    "success": "#2e5a1c",
    "success_light": "#3e7a2c",
    "frost": "#a0c4e8",
    "fire": "#ff6b35",
    "shadow": "#2f4f4f",
    "arcane": "#7b68ee",
    "hist_green": "#228b22",
}

SKYRIM_CSS = """
/* ==========================================================================
   THE ELDER MODELS V: LLMRIM - Enhanced Skyrim Theme
   Deeper atmosphere, richer gradients, ornate decorative elements
   ========================================================================== */

/* === Global Styles === */
Screen {
    background: #1a1512;
}

/* === Title Styling === */
.title {
    text-style: bold;
    color: #c9a959;
    text-align: center;
}

.subtitle {
    color: #8b7355;
    text-align: center;
}

/* === Parchment Container === */
.parchment {
    background: #2a1f14;
    border: tall #5a4a32;
    padding: 1 2;
}

.parchment-title {
    color: #c9a959;
    text-style: bold;
    text-align: center;
    padding-bottom: 1;
}

/* === Dragon Border === */
.dragon-border {
    border: heavy #5a4a32;
    border-title-color: #c9a959;
    border-title-style: bold;
    background: #231b13;
    padding: 1 2;
}

/* === Stat Bars === */
.stat-bar {
    color: #c9a959;
    background: #3d2e1f;
}

.stat-label {
    color: #d4c4a8;
    width: 20;
}

.stat-value {
    color: #e8d9a0;
    text-style: bold;
    width: 8;
    text-align: right;
}

/* === Buttons === */
Button {
    background: #3d2e1f;
    color: #d4c4a8;
    border: tall #5a4a32;
}

Button:hover {
    background: #4d3e2f;
    color: #e8d9a0;
    border: tall #8b7355;
}

Button:focus {
    background: #4d3e2f;
    color: #c9a959;
    border: tall #c9a959;
}

Button.-primary {
    background: #5a4a32;
    color: #c9a959;
    border: tall #c9a959;
    text-style: bold;
}

Button.-primary:hover {
    background: #6a5a42;
    color: #ffd700;
    border: tall #ffd700;
}

/* === Input Fields === */
Input {
    background: #231b13;
    color: #d4c4a8;
    border: tall #5a4a32;
}

Input:focus {
    border: tall #c9a959;
    background: #2a1f14;
}

/* === Labels === */
Label {
    color: #d4c4a8;
}

.label-gold {
    color: #c9a959;
}

.label-muted {
    color: #7a6e5a;
}

.label-bright {
    color: #f0e6d2;
}

/* === Selection List === */
SelectionList {
    background: #231b13;
    border: tall #5a4a32;
}

SelectionList > .selection-list--option {
    padding: 0 2;
}

SelectionList > .selection-list--option-highlighted {
    background: #3d2e1f;
    color: #c9a959;
}

SelectionList > .selection-list--option-selected {
    color: #c9a959;
}

/* === Option List === */
OptionList {
    background: #231b13;
    border: tall #5a4a32;
}

OptionList > .option-list--option-highlighted {
    background: #3d2e1f;
    color: #c9a959;
}

/* === Radio Buttons & Checkboxes === */
RadioButton {
    background: transparent;
    color: #d4c4a8;
}

RadioButton:focus {
    color: #c9a959;
}

RadioButton.-on {
    color: #c9a959;
    text-style: bold;
}

Checkbox {
    background: transparent;
    color: #d4c4a8;
}

Checkbox:focus {
    color: #c9a959;
}

Checkbox.-on {
    color: #c9a959;
    text-style: bold;
}

/* === Progress Bars === */
ProgressBar {
    color: #c9a959;
    background: #3d2e1f;
}

ProgressBar > .bar--bar {
    color: #c9a959;
    background: #3d2e1f;
}

ProgressBar > .bar--complete {
    color: #c9a959;
}

/* === Tabs === */
TabbedContent {
    background: #1a1512;
}

Tabs {
    background: #231b13;
}

Tab {
    background: #231b13;
    color: #7a6e5a;
    padding: 1 3;
}

Tab:hover {
    background: #3d2e1f;
    color: #d4c4a8;
}

Tab.-active {
    background: #3d2e1f;
    color: #c9a959;
    text-style: bold;
}

TabPane {
    background: #1a1512;
    padding: 1;
}

/* === Scrollbars === */
Scrollbar {
    background: #231b13;
}

Scrollbar > .scrollbar--bar {
    background: #5a4a32;
}

Scrollbar > .scrollbar--bar:hover {
    background: #8b7355;
}

/* === Data Tables === */
DataTable {
    background: #231b13;
    border: tall #5a4a32;
}

DataTable > .datatable--header {
    background: #3d2e1f;
    color: #c9a959;
    text-style: bold;
}

DataTable > .datatable--cursor {
    background: #4d3e2f;
    color: #e8d9a0;
}

/* === Footer === */
Footer {
    background: #231b13;
    color: #7a6e5a;
}

Footer > .footer--key {
    color: #c9a959;
    background: #3d2e1f;
}

Footer > .footer--description {
    color: #d4c4a8;
}

/* === Header === */
Header {
    background: #231b13;
    color: #c9a959;
}

/* === Containers === */
Container {
    background: transparent;
}

Horizontal {
    background: transparent;
}

Vertical {
    background: transparent;
}

/* === Static Text === */
Static {
    background: transparent;
    color: #d4c4a8;
}

/* === Rich Text === */
RichLog {
    background: #231b13;
    border: tall #5a4a32;
    padding: 1;
}

/* === Race Card === */
.race-card {
    background: #231b13;
    border: tall #5a4a32;
    padding: 1 2;
    margin: 1;
    width: 40;
    height: 12;
}

.race-card:hover {
    border: tall #8b7355;
    background: #2a1f14;
}

.race-card:focus {
    border: double #c9a959;
    background: #2a1f14;
}

.race-card-selected {
    border: double #c9a959;
    background: #3d2e1f;
}

.race-name {
    color: #c9a959;
    text-style: bold;
    text-align: center;
}

.race-model {
    color: #8b7355;
    text-align: center;
}

.race-params {
    color: #d4c4a8;
    text-align: center;
}

.race-lore {
    color: #7a6e5a;
    padding-top: 1;
}

/* === Standing Stones === */
.stone-panel {
    background: #231b13;
    border: heavy #5a4a32;
    padding: 1 2;
    margin: 1;
}

.stone-panel:focus {
    border: heavy #c9a959;
}

.stone-title {
    color: #c9a959;
    text-style: bold;
    text-align: center;
}

.stone-warrior {
    border-title-color: #ff6b35;
}

.stone-mage {
    border-title-color: #a0c4e8;
}

.stone-thief {
    border-title-color: #3e7a2c;
}

/* === Summary Screen === */
.summary-box {
    background: #231b13;
    border: double #c9a959;
    padding: 1 2;
}

.summary-label {
    color: #8b7355;
    width: 20;
}

.summary-value {
    color: #d4c4a8;
    text-style: bold;
}

/* === Parameter Display === */
.param-count {
    color: #c9a959;
    text-style: bold;
    text-align: center;
}

.param-warning {
    color: #a52a2a;
}

.param-ok {
    color: #3e7a2c;
}

/* === Lore Text === */
.lore-text {
    color: #7a6e5a;
    text-style: italic;
}

/* === Dramatic Messages === */
.dramatic {
    color: #c9a959;
    text-style: bold italic;
    text-align: center;
}

/* === Title Screen Specific === */
#title-logo {
    color: #c9a959;
    text-align: center;
}

#title-subtitle {
    color: #8b7355;
    text-align: center;
    text-style: italic;
}

#title-prompt {
    color: #7a6e5a;
    text-align: center;
}

/* === Slider Widget === */
.slider-container {
    height: 3;
}

.slider-label {
    width: 24;
    color: #d4c4a8;
}

.slider-bar {
    color: #c9a959;
}

.slider-value {
    width: 10;
    text-align: right;
    color: #e8d9a0;
    text-style: bold;
}

/* === Collapsible === */
Collapsible {
    background: #231b13;
    border: tall #5a4a32;
    padding: 0;
    margin: 1;
}

CollapsibleTitle {
    color: #c9a959;
    background: #231b13;
    padding: 0 1;
}

CollapsibleTitle:hover {
    background: #3d2e1f;
}

CollapsibleTitle:focus {
    background: #3d2e1f;
    color: #ffd700;
}

/* === Text Area === */
TextArea {
    background: #1a1512;
    border: tall #5a4a32;
}

TextArea:focus {
    border: tall #c9a959;
}
"""


# Ornamental separators
ORNAMENT_HEAVY = "═══════════════════════════════════════════════════════════"
ORNAMENT_LIGHT = "───────────────────────────────────────────────────────────"
ORNAMENT_DOTTED = "- - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
ORNAMENT_DIAMOND = "◆ ─ ◆ ─ ◆ ─ ◆ ─ ◆ ─ ◆ ─ ◆ ─ ◆ ─ ◆ ─ ◆ ─ ◆ ─ ◆ ─ ◆"
ORNAMENT_RUNIC = "᛫ ᛫ ᛫ ᛫ ᛫ ᛫ ᛫ ᛫ ᛫ ᛫ ᛫ ᛫ ᛫ ᛫ ᛫ ᛫ ᛫ ᛫ ᛫ ᛫ ᛫ ᛫ ᛫ ᛫"

DRAGON_SEPARATOR = ORNAMENT_HEAVY
