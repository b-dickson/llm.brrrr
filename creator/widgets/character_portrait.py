"""
Character Portrait - ASCII art portraits for each race.
"""

from textual.widgets import Static
from textual.reactive import reactive


# Large ASCII art portraits for each race category
PORTRAITS = {
    # === Transformer Races ===
    "nord": r"""[#a0c4e8]
       ___
      /   \
     | o o |
      \ _ /
    __/   \__
   /  NORD   \
  /  warrior  \
 |  ╔═══════╗  |
 |  ║ ⚔ MHA ║  |
 |  ╚═══════╝  |
  \___________/
[/]""",

    "imperial": r"""[#c9a959]
       ___
      /👑 \
     | o o |
      \ ‿ /
    __/   \__
   / IMPERIAL \
  /  balanced  \
 |  ╔═══════╗  |
 |  ║ ⚖ MHA ║  |
 |  ╚═══════╝  |
  \___________/
[/]""",

    "altmer": r"""[#e8d9a0]
        /\
       /  \
      /o  o\
       \ ‿ /
    ___/  \___
   /  ALTMER  \
  /  powerful  \
 |  ╔═══════╗  |
 |  ║ ✨MHA ║  |
 |  ╚═══════╝  |
  \___________/
[/]""",

    "dragonborn": r"""[#ff6b35]
      ,  ,
     /(  )\
    ( o  o )
     \    /
   ___\  /___
  / DRAGON- \
 /   BORN    \
 |  ╔═══════╗ |
 |  ║ 🐉MHA ║ |
 |  ╚═══════╝ |
  \__________/
[/]""",

    "daedra": r"""[#8b0000]
     ╱╲___╱╲
    ( • _ • )
     )     (
    /  |||  \
   / DAEDRA  \
  /  8B GQA   \
 |  ╔═══════╗  |
 |  ║ 🔥GQA ║  |
 |  ╚═══════╝  |
  \___________/
[/]""",

    "aedra": r"""[#f0e6d2]
      ☆ ☆ ☆
     \  |  /
      \   /
     (  ⭐  )
   ___/   \___
   /  AEDRA  \
  /  70B GQA  \
 |  ╔═══════╗  |
 |  ║ ⭐GQA ║  |
 |  ╚═══════╝  |
  \___________/
[/]""",

    # === Mamba/Dwemer Races ===
    "dwemer": r"""[#b8860b]
      ┌───┐
      │⚙⚙│
      └─┬─┘
     ╔══╧══╗
     ║DWEMR║
     ╠═════╣
     ║MAMBA║
     ║ SSM ║
     ╚═════╝
    ╱╱   ╲╲
[/]""",

    "dwemer_centurion": r"""[#cd853f]
     ╔═════╗
     ║ 🤖 ║
     ╠═════╣
     ║CNTRN║
     ╠═════╣
     ║MAMBA║
     ║ 1B  ║
     ╠═════╣
     ║ ⚙⚙⚙ ║
     ╚═════╝
[/]""",

    "dwemer_numidium": r"""[#daa520]
   ╔═══════════╗
   ║  NUMIDIUM ║
   ║    🏛️     ║
   ╠═══════════╣
   ║  MAMBA-2  ║
   ║    3B     ║
   ╠═══════════╣
   ║ ⚙ SSM ⚙  ║
   ║  32K CTX  ║
   ╚═══════════╝
[/]""",

    # === Hybrid/Falmer Races ===
    "falmer": r"""[#708090]
     ╱     ╲
    (  x x  )
     \     /
    ╔═══════╗
    ║FALMER ║
    ╠═══════╣
    ║HYBRID ║
    ║ATN+FLA║
    ╚═══════╝
     ╲     ╱
[/]""",

    "falmer_warmonger": r"""[#4a4a4a]
    ⚔  ⚔  ⚔
     ╲ | ╱
      \|/
     (X X)
    ╔═════╗
    ║WAR- ║
    ║MONGR║
    ╠═════╣
    ║HYBRD║
    ║ 3B  ║
    ╚═════╝
[/]""",

    # === Linear/Argonian Races ===
    "argonian": r"""[#228b22]
        /\
       /  \
      / 🦎 \
     /  ▽   \
    ╔═══════╗
    ║ARGONIN║
    ╠═══════╣
    ║DELTANET
    ║LINEAR ║
    ╚═══════╝
    ~~ 🌊 ~~
[/]""",

    "argonian_shadowscale": r"""[#2f4f4f]
      🌙
     /  \
    / 🗡️ \
   /SHDWSCL\
  ╔════════╗
  ║DELTANET║
  ║  1B    ║
  ╠════════╣
  ║O(n) 🗡️ ║
  ╚════════╝
[/]""",

    "argonian_veezara": r"""[#228b22]
    🌿 ⚔️ 🌿
     \  |  /
      \ | /
     (🦎▽🦎)
   ╔══════════╗
   ║ VEEZARA  ║
   ╠══════════╣
   ║GatedDelta║
   ║ Net 3B   ║
   ╠══════════╣
   ║SequMixer ║
   ║ NATIVE   ║
   ╚══════════╝
[/]""",

    # === MoE/Khajiit Races ===
    "khajiit": r"""[#deb887]
     /\_/\
    ( o.o )
     > ^ <
   /KHAJIIT\
  ╔════════╗
  ║MoE 8x1B║
  ╠════════╣
  ║8 EXPRT ║
  ║TOP-2   ║
  ╚════════╝
   🐱 wares
[/]""",

    "khajiit_mane": r"""[#f4a460]
    👑 /\_/\ 👑
      ( ^.^ )
       > * <
     THE MANE
   ╔══════════╗
   ║ MoE 8x7B ║
   ╠══════════╣
   ║ 8 EXPERT ║
   ║  56B TOT ║
   ╚══════════╝
[/]""",

    # === Normalized/Bosmer Race ===
    "bosmer": r"""[#6b8e23]
      🌲🌲🌲
       \|/
      ( ‿ )
       /|\
    VALENWOOD
   ╔═════════╗
   ║  nGPT   ║
   ╠═════════╣
   ║NORMALZD ║
   ║ L2NORM  ║
   ╚═════════╝
[/]""",

    # === Custom ===
    "custom": r"""[#7a6e5a]
      ?????
       ???
      ?   ?
       ???
    ╔═══════╗
    ║CUSTOM ║
    ╠═══════╣
    ║ YOUR  ║
    ║CREATE ║
    ╚═══════╝
     🔧 🔧
[/]""",
}

# Smaller inline portraits for list views
MINI_PORTRAITS = {
    "nord": "[#a0c4e8]⚔️ ╔N╗[/]",
    "imperial": "[#c9a959]👑 ╔I╗[/]",
    "altmer": "[#e8d9a0]✨ ╔A╗[/]",
    "dragonborn": "[#ff6b35]🐉 ╔D╗[/]",
    "daedra": "[#8b0000]🔥 ╔Δ╗[/]",
    "aedra": "[#f0e6d2]⭐ ╔Ω╗[/]",
    "dwemer": "[#b8860b]⚙️ ╔⛭╗[/]",
    "dwemer_centurion": "[#cd853f]🤖 ╔C╗[/]",
    "dwemer_numidium": "[#daa520]🏛️ ╔N╗[/]",
    "falmer": "[#708090]🦇 ╔F╗[/]",
    "falmer_warmonger": "[#4a4a4a]⚔️ ╔W╗[/]",
    "argonian": "[#228b22]🦎 ╔🜄╗[/]",
    "argonian_shadowscale": "[#2f4f4f]🗡️ ╔S╗[/]",
    "argonian_veezara": "[#228b22]🌊 ╔V╗[/]",
    "khajiit": "[#deb887]🐱 ╔K╗[/]",
    "khajiit_mane": "[#f4a460]👑 ╔M╗[/]",
    "bosmer": "[#6b8e23]🌲 ╔B╗[/]",
    "custom": "[#7a6e5a]🔧 ╔?╗[/]",
}


class CharacterPortrait(Static):
    """A widget displaying ASCII art character portrait."""

    DEFAULT_CSS = """
    CharacterPortrait {
        width: auto;
        height: auto;
        padding: 1;
        text-align: center;
    }
    """

    race = reactive("custom")

    def __init__(
        self,
        race: str = "custom",
        id: str | None = None,
        classes: str | None = None,
    ) -> None:
        super().__init__(id=id, classes=classes, markup=True)
        self.race = race

    def render(self) -> str:
        """Render the portrait for the current race."""
        return PORTRAITS.get(self.race, PORTRAITS["custom"])

    def watch_race(self, race: str) -> None:
        """Update when race changes."""
        self.refresh()


def get_portrait(race: str) -> str:
    """Get the ASCII portrait for a race."""
    return PORTRAITS.get(race, PORTRAITS["custom"])


def get_mini_portrait(race: str) -> str:
    """Get the mini inline portrait for a race."""
    return MINI_PORTRAITS.get(race, MINI_PORTRAITS["custom"])
