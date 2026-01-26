"""
Skyrim Theme - The Colors of Tamriel
CSS theme for the LLMRIM TUI.
"""

# Color palette
COLORS = {
    "gold": "#c9a959",
    "gold_dark": "#a88932",
    "gold_light": "#e8d9a0",
    "bronze": "#8b7355",
    "leather": "#1a1512",
    "leather_light": "#2a1f14",
    "parchment": "#3d2e1f",
    "parchment_light": "#4d3e2f",
    "text": "#d4c4a8",
    "text_muted": "#7a6e5a",
    "text_bright": "#f0e6d2",
    "border": "#5a4a32",
    "border_light": "#6a5a42",
    "danger": "#8b0000",
    "danger_light": "#a52a2a",
    "success": "#2e5a1c",
    "success_light": "#3e7a2c",
    "frost": "#a0c4e8",
    "fire": "#ff6b35",
}

SKYRIM_CSS = """
/* ==========================================================================
   THE ELDER MODELS V: LLMRIM - Skyrim Theme
   ========================================================================== */

/* Global Styles */
Screen {
    background: #1a1512;
}

/* Title styling */
.title {
    text-style: bold;
    color: #c9a959;
    text-align: center;
}

.subtitle {
    color: #8b7355;
    text-align: center;
}

/* Parchment container */
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

/* Dragon border styling */
.dragon-border {
    border: heavy #5a4a32;
    border-title-color: #c9a959;
    border-title-style: bold;
    background: #2a1f14;
    padding: 1 2;
}

/* Stat bars */
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

/* Buttons */
Button {
    background: #3d2e1f;
    color: #d4c4a8;
    border: tall #5a4a32;
}

Button:hover {
    background: #4d3e2f;
    color: #e8d9a0;
    border: tall #6a5a42;
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
}

Button.-primary:hover {
    background: #6a5a42;
    color: #e8d9a0;
}

/* Input fields */
Input {
    background: #2a1f14;
    color: #d4c4a8;
    border: tall #5a4a32;
}

Input:focus {
    border: tall #c9a959;
}

/* Labels */
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

/* Selection list */
SelectionList {
    background: #2a1f14;
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

/* Option list */
OptionList {
    background: #2a1f14;
    border: tall #5a4a32;
}

OptionList > .option-list--option-highlighted {
    background: #3d2e1f;
    color: #c9a959;
}

/* Radio buttons and checkboxes */
RadioButton {
    background: transparent;
    color: #d4c4a8;
}

RadioButton:focus {
    color: #c9a959;
}

RadioButton.-on {
    color: #c9a959;
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
}

/* Progress bars */
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

/* Tabs */
TabbedContent {
    background: #1a1512;
}

Tabs {
    background: #2a1f14;
}

Tab {
    background: #2a1f14;
    color: #7a6e5a;
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
    background: #2a1f14;
    padding: 1;
}

/* Scrollbars */
Scrollbar {
    background: #2a1f14;
}

Scrollbar > .scrollbar--bar {
    background: #5a4a32;
}

Scrollbar > .scrollbar--bar:hover {
    background: #6a5a42;
}

/* Data tables */
DataTable {
    background: #2a1f14;
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

/* Footer */
Footer {
    background: #2a1f14;
    color: #7a6e5a;
}

Footer > .footer--key {
    color: #c9a959;
    background: #3d2e1f;
}

Footer > .footer--description {
    color: #d4c4a8;
}

/* Header */
Header {
    background: #2a1f14;
    color: #c9a959;
}

/* Containers */
Container {
    background: transparent;
}

Horizontal {
    background: transparent;
}

Vertical {
    background: transparent;
}

/* Static text */
Static {
    background: transparent;
    color: #d4c4a8;
}

/* Rich text */
RichLog {
    background: #2a1f14;
    border: tall #5a4a32;
    padding: 1;
}

/* Custom race card */
.race-card {
    background: #2a1f14;
    border: tall #5a4a32;
    padding: 1 2;
    margin: 1;
    width: 40;
    height: 12;
}

.race-card:hover {
    border: tall #6a5a42;
    background: #3d2e1f;
}

.race-card:focus {
    border: tall #c9a959;
    background: #3d2e1f;
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

/* Standing stones */
.stone-panel {
    background: #2a1f14;
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
    border-title-color: #2e5a1c;
}

/* Summary screen */
.summary-box {
    background: #2a1f14;
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

/* Parameter display */
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

/* Lore text */
.lore-text {
    color: #7a6e5a;
    text-style: italic;
}

/* Dramatic messages */
.dramatic {
    color: #c9a959;
    text-style: bold italic;
    text-align: center;
}

/* Title screen specific */
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

/* Slider widget */
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
"""


# ASCII art for title screen
TITLE_ART = r"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║     ████████╗██╗  ██╗███████╗    ███████╗██╗     ██████╗ ███████╗██████╗     ║
║     ╚══██╔══╝██║  ██║██╔════╝    ██╔════╝██║     ██╔══██╗██╔════╝██╔══██╗    ║
║        ██║   ███████║█████╗      █████╗  ██║     ██║  ██║█████╗  ██████╔╝    ║
║        ██║   ██╔══██║██╔══╝      ██╔══╝  ██║     ██║  ██║██╔══╝  ██╔══██╗    ║
║        ██║   ██║  ██║███████╗    ███████╗███████╗██████╔╝███████╗██║  ██║    ║
║        ╚═╝   ╚═╝  ╚═╝╚══════╝    ╚══════╝╚══════╝╚═════╝ ╚══════╝╚═╝  ╚═╝    ║
║                                                                              ║
║                    ███╗   ███╗ ██████╗ ██████╗ ███████╗██╗      ███████╗     ║
║                    ████╗ ████║██╔═══██╗██╔══██╗██╔════╝██║      ██╔════╝     ║
║                    ██╔████╔██║██║   ██║██║  ██║█████╗  ██║      ███████╗     ║
║                    ██║╚██╔╝██║██║   ██║██║  ██║██╔══╝  ██║      ╚════██║     ║
║                    ██║ ╚═╝ ██║╚██████╔╝██████╔╝███████╗███████╗ ███████║     ║
║                    ╚═╝     ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝╚══════╝ ╚══════╝     ║
║                                                                              ║
║                              ██╗   ██╗                                       ║
║                              ██║   ██║                                       ║
║                              ██║   ██║                                       ║
║                              ╚██╗ ██╔╝                                       ║
║                               ╚████╔╝                                        ║
║                                ╚═══╝                                         ║
║                                                                              ║
║                         ██╗     ██╗     ███╗   ███╗██████╗ ██╗███╗   ███╗    ║
║                         ██║     ██║     ████╗ ████║██╔══██╗██║████╗ ████║    ║
║                         ██║     ██║     ██╔████╔██║██████╔╝██║██╔████╔██║    ║
║                         ██║     ██║     ██║╚██╔╝██║██╔══██╗██║██║╚██╔╝██║    ║
║                         ███████╗███████╗██║ ╚═╝ ██║██║  ██║██║██║ ╚═╝ ██║    ║
║                         ╚══════╝╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚═╝     ╚═╝    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

TITLE_ART_SMALL = r"""
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║              T H E   E L D E R   M O D E L S               ║
║                                                            ║
║                          ══╦══                             ║
║                            ║                               ║
║                            V                               ║
║                                                            ║
║                      L L M R I M                           ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
"""

DRAGON_SEPARATOR = "═══════════════════════════════════════════════════════════"
