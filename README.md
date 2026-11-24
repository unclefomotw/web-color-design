# web-color-design

An agent skill for designing, auditing, and implementing accessible website
color palettes and semantic color tokens. It grounds decisions in HCI, visual
perception, UI/UX practice, and WCAG 2.2, and it prioritizes readability, task
performance, and accessibility over aesthetic trends.

## Install

```sh
npx skills add <owner>/web-color-design
```

Or copy this directory into your agent's skills folder, for example
`~/.claude/skills/web-color-design/` for Claude Code.

## What it covers

- Decision priorities and task context (reading, interactive products, data)
- Perception and attention: luminance vs. hue, emphasis, hierarchy
- Reading comfort over sustained use, as a goal separate from legibility:
  contrast band, glare, saturation, visual noise, luminance stability, and how
  to verify comfort with readers
- Color models: HEX/RGB, HSV, OKLCH and their limits
- Semantic token architecture, state matrices, feedback colors
- WCAG 2.2 AA/AAA gates: text and non-text contrast, links, focus, flashing
- Limits of the WCAG 2 contrast ratio and when to add perceptual review
- Dark themes, CJK typography, data visualization palettes
- User settings: `prefers-color-scheme`, `prefers-contrast`,
  `prefers-reduced-transparency`, forced colors, `accent-color`
- Verification and reporting formats

Claims in the skill are tagged **[N]** (normative WCAG), **[E]** (empirical
finding), or **[H]** (design heuristic).

## Files

| Path | Purpose |
|---|---|
| `SKILL.md` | The skill instructions |
| `references/output-template.md` | Formats for palette proposals, audits, and implementation reports |
| `scripts/contrast.py` | WCAG 2.x contrast checker (Python 3, standard library only) |
| `scripts/test_contrast.py` | Known-value tests for the checker |

## Contrast checker

```sh
python3 scripts/contrast.py '#767676' '#fff'
python3 scripts/contrast.py 'oklch(0.55 0.15 250)' '#fafafa'
python3 scripts/contrast.py 'rgb(0 0 0 / 0.6)' '#ffffff'      # alpha is composited
python3 scripts/contrast.py --link '#0066cc' '#333' '#fff'    # color-only link check
python3 scripts/contrast.py --over '#ffffff' '#00000080'      # resolve a translucent layer
python3 scripts/contrast.py --file pairs.txt --json            # batch: name, fg, bg per line
```

Ratios are truncated, never rounded up, so a result at a threshold boundary
is never reported as passing when it fails. Out-of-sRGB OKLCH colors are
clipped with a warning; browsers may gamut-map them differently, so verify
rendered values in the browser.

Run the tests:

```sh
python3 -m unittest discover -s scripts
```

## Caveats

Passing color-contrast checks does not by itself make a site WCAG-conformant.
The skill and the checker support review; they do not replace testing with
real users and assistive technology.

## License

[MIT](LICENSE)
