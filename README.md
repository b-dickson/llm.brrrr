# The Elder Models V: LLMRIM

A Skyrim-themed terminal UI for designing LLM architectures. Pick a race,
tweak the stats, walk between the standing stones, and out comes a complete
[OLMo-core](https://github.com/allenai/OLMo-core) config + training script.

*"Fus Ro Brrr… your training begins."*

## Install & run

```bash
uv sync          # ~10 deps, no torch — fast
uv run llmrim
```

Generated files land in `./models/<your-model-name>/`.

To actually train one of the generated configs you also need olmo-core
(2.5.0+ for the `SequenceMixer` API and native `GatedDeltaNet`):

```bash
uv sync --extra olmo            # pulls v2.5.0 from GitHub
uv sync --extra olmo --extra flash   # …plus flash-attn / fla
```

## Races

| Family | Races | Architecture |
|---|---|---|
| Men | Nord, Imperial, Altmer, Dragonborn | GPT-2 small → XL |
| Divine | Daedra, Aedra | LLaMA-3 8B / 70B (GQA + RoPE) |
| Argonian | Argonian, Shadowscale, Veezara | GatedDeltaNet (native, O(n)) |
| Falmer | Falmer, Warmonger | Hybrid attention + GatedDeltaNet |
| Khajiit | Khajiit, Mane | Mixture of Experts |
| Bosmer | Bosmer | nGPT (normalized) |
| Dwemer | Dwemer, Centurion, Numidium | linear-recurrent (emitted as GDN) |
| — | Custom | start from scratch |

## Keys

| | |
|---|---|
| arrows / tab | navigate |
| enter | confirm |
| escape | back |
| g / f | generate config / full package |
| q | quit |

## Layout

```
creator/
  app.py          # Textual app + screen wiring
  config.py       # ModelConfig dataclass
  presets.py      # the 18 races
  generator.py    # emits olmo-core 2.5.0 Python
  theme.py        # one weathered-parchment palette
  screens/        # title, race select, attributes, stones, summary
  widgets/        # parchment, slider, sheet, portrait
```

The TUI itself only depends on `textual` — the olmo-core imports live
inside generated string templates, so `uv sync` stays light.
