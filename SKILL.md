---
name: web-color-design
description: Design, audit, or implement accessible website color palettes and semantic color tokens using HCI, visual perception, UI/UX, and WCAG 2.2 principles. Use when choosing backgrounds, text, accents, light or dark themes, interaction states, data visualization colors, or reviewing CSS and design systems for color and contrast (配色、色票、對比、深色模式). Prioritize readability, task performance, accessibility, and consistency over aesthetic trends.
---

# Website color design

Claims are tagged: **[N]** normative WCAG 2.2 requirement, **[E]** empirical
finding, **[H]** design heuristic. Do not present [H] as [N], or [E] as universal.

## Objective and decision priority

Design color around human tasks, not around a fashionable palette. Priorities:

1. Accessibility, legibility, and the user's own settings (theme, contrast, forced colors).
2. Task comprehension and error prevention.
3. Visual hierarchy and consistency.
4. Comfort and aesthetic preference.
5. Brand expression.

When two priorities conflict, first look for a solution that satisfies both —
usually by changing a color's role (e.g. brand color as a fill or large heading,
not body text) rather than its value. Only if none exists, let the higher
priority win and record the tradeoff. Treat legal or contractual brand
constraints as fixed inputs, and work around them.

## 1. Establish context

Inspect existing CSS, tokens, representative pages and components when
available. Identify the primary task (reading, navigating, purchasing, editing,
monitoring, exploring), audience, language and script, typography, devices and
ambient lighting, brand constraints, and required themes. Preserve existing
design-system conventions unless they conflict with the objective. If
information is missing, state assumptions and proceed with reversible
proposals; ask only when a consequential decision cannot be made responsibly.

## 2. Design for perception and attention

Reduce unnecessary visual search; spend attention on what the task needs. Color
reinforces hierarchy but cannot replace it.

- Use luminance contrast for legibility; hue and chroma for grouping, identity
  and meaning. Equal RGB/HSB brightness is not equal perceived brightness;
  saturated colors can also look brighter than their luminance suggests. [E]
- Color is a pre-attentive feature: a single distinct color pops out, but the
  effect weakens as more colors compete. Reserve prominent colors for the few
  actions or signals that deserve attention. [E]
- Keep large surfaces visually quiet by default: neutral or near-neutral, with a
  controlled brand tint only if it helps. [H]
- Carry hierarchy with typography, spacing, position and shape too, so it
  survives grayscale, forced colors and color-vision deficiency.
- Keep each semantic role visually consistent across pages; distinguish roles
  only where comprehension needs it.
- Avoid universal claims (blue = trust, red = danger, fixed 60/30/10 ratios).
  Meaning depends on culture, context and convention. [H]
- Evaluate colors in their real surroundings and display conditions: adjacent
  surfaces, type, images, shadows, overlays; bright outdoor light, auto
  brightness, warm-shift modes (Night Shift/True Tone), wide-gamut and low-end
  panels.

## 3. Choose a color model

- RGB/HEX for interchange and inspection; HSB/HSV for intuitive exploration;
  OKLCH for generating and adjusting more perceptually consistent scales.
- HSV's V is the max RGB channel and S is relative to V; HSL lightness is not
  perceptual either. OKLCH is approximate: it still has hue drift (notably in
  blues/purples) and high-chroma values often fall outside sRGB.
- When adjusting an existing color, change one dimension at a time: OKLCH
  lightness for tonal hierarchy, chroma for prominence, holding hue where
  practical.
- Always verify the rendered sRGB value. Out-of-gamut colors are clipped or
  gamut-mapped, and browsers do not all do it the same way; provide sRGB
  fallbacks where needed.
- Never infer WCAG conformance from HSB, HSL or OKLCH differences. Do not
  mandate fixed hue, saturation or brightness ranges for backgrounds.

## 4. Build semantic palettes

Make role and state relationships predictable, and changeable without editing
components.

Separate primitive scales from semantic tokens; components consume semantic
tokens. Add a component tier only if the design system is large enough to need
it. Define only the roles the product uses:

- Surfaces: canvas, content, raised, inset, overlay, code.
- Text: primary, secondary, muted, inverse, link, visited link.
- Borders: decorative divider, control boundary, focus ring.
- Actions: primary, secondary, destructive — foreground and background each.
- States: hover, active, focus-visible, selected, disabled, loading.
- Feedback: success, warning, error, info — foreground, background, border, icon.
- Data: categorical, sequential, diverging, missing values, selection.

Rules:

- Define foreground/background **pairs**, not isolated swatches.
- Decorative dividers need not meet control-boundary contrast; control
  boundaries that identify a control do (see §5).
- Secondary and muted text that conveys information must still meet text contrast.
- Do not lower opacity across the board: the resulting contrast depends on
  whatever is underneath. Resolve to an opaque value, or measure every
  underlying surface.
- **State matrix.** States combine: selected+hover, selected+focus,
  focus+error, disabled+selected. Each combination that can occur must stay
  distinguishable from its neighbours. Touch devices have no hover, so never put
  required information in hover alone.
- **Disabled.** Exempt from contrast [N], but must still be recognizable as a
  present-but-unavailable control; where users may not know why, explain it in
  text. [H]
- **Warning/yellow.** Yellow text on light surfaces rarely reaches 4.5:1. Use
  yellow for fills or icons, with dark amber or neutral text. [H]

## 5. Accessibility acceptance gates

Default to WCAG 2.2 AA unless a stricter target is required. Consult the
normative text for formal conformance reviews or ambiguous cases.

**Text contrast [N]**
- Normal text ≥ 4.5:1. Large text (≥ 18 pt / 24 CSS px, or ≥ 14 pt / ≈ 18.67
  CSS px bold) ≥ 3:1. AAA: 7:1 and 4.5:1.
- Never round a failing result up (4.49 fails).
- Placeholder text that conveys information is text.

**Non-text contrast [N]**
- Visual information needed to identify controls, their states, and meaningful
  graphical objects ≥ 3:1 against adjacent colors. This includes focus
  indicators, input boundaries when they are the only cue to the control, chart
  marks that carry meaning, and adjacent chart segments.

**Not by color alone [N]**
- Add labels, icons, patterns, shape or underlines.
- Errors need explanatory text associated with the field, not just a red outline.
- Inline links: underline by default. A color-only link must meet three
  constraints at once: link vs background ≥ 4.5, body text vs background
  ≥ 4.5, link vs body text ≥ 3, and it needs a non-color cue on hover and
  keyboard focus. The three-way constraint is often unsatisfiable on dark
  surfaces; persistent underlines avoid it. Check with `contrast.py --link`.

**Focus [N]**
- Keyboard focus must be visible (2.4.7). Its indicator falls under non-text
  contrast. Author content must not fully hide it (2.4.11, AA).
- Focus Appearance (2.4.13) is AAA. Do not conflate it with AA.
- Prefer a distinct outline with offset over a subtle hue shift. [H]

**Flashing [N]**
- No content flashes more than three times per second unless below the general
  and red flash thresholds (2.3.1). Saturated red flashes are especially risky.
  This applies to color transitions and animated states too.

**Scope**
- Check every state and surface: placeholders, selection, links, visited links,
  syntax highlighting, validation, overlays, translucent layers, gradients,
  image backgrounds.
- Text-contrast exceptions: inactive controls, pure decoration, invisible text,
  text incidental to a picture with significant other content, logotypes.
- Non-text exceptions: inactive controls, unmodified user-agent appearance,
  graphics where the presentation is essential.
- Exceptions never apply to content that is active or merely secondary.

**Measurement**
- Run `scripts/contrast.py` (hex, rgb(), oklch(); composites translucent
  foregrounds; prints truncated ratios) or use browser inspection. Do not
  compute ratios mentally.
- Formula: linearize each sRGB channel (c ≤ 0.04045 ? c/12.92 :
  ((c+0.055)/1.055)^2.4); L = 0.2126R + 0.7152G + 0.0722B; ratio = (L₁+0.05)/(L₂+0.05).
- For transparency, measure the composited color. For variable backgrounds,
  measure the least favorable region.
- Never fabricate measurements. Passing color checks does not establish WCAG
  conformance.

**Limits of the WCAG 2 ratio**
- The WCAG 2 ratio is the conformance gate, not a readability guarantee. [E]
- It tends to overstate legibility of light-on-dark and mid-dark pairs, judges
  some mid-tone fills (e.g. orange) poorly, and ignores font weight and size.
- For dark themes, colored buttons and thin fonts, add a perceptual review: a
  visual check at real size and weight, optionally an advisory perceptual
  metric such as APCA. Advisory metrics come from WCAG 3 drafts, are not
  normative, and never replace the WCAG 2 result.

**Comfort**
- Sufficient contrast does not mean pure black on pure white. For long-form
  body text, ~7:1 is a robust voluntary starting target; then test comfort. [H]

## 6. Adapt to the task, script and theme

### Reading and documentation
- Use quiet surfaces, readable body text and clearly recognizable links.
- Positive polarity (dark on light) outperformed negative polarity in several
  reading and proofreading studies, more so at small sizes. [E] It is a
  reasonable default for text-heavy sites.
- Neither light nor dark mode is universally healthier. Some low-vision users
  (e.g. with glare sensitivity) read better on dark.
- For technical content, audit every syntax token, inline code, code selection,
  diagram and callout.

### CJK and dense scripts
- Chinese, Japanese and Korean glyphs pack many strokes into the same em box,
  so thin weights at small sizes lose strokes sooner than Latin text.
- Do not lean on the 14 pt bold "large text" allowance for CJK body copy. Aim
  above the minimum for thin or light CJK weights, and check rendered text on
  real devices. [H]

### Dark themes
- Build a separate semantic palette; do not invert light colors mechanically.
- Shadows barely read on dark surfaces. Express elevation mainly through
  lighter surface tones, keeping adjacent panels distinguishable. [H]
- Light text on dark can bloom (halation), especially for people with
  astigmatism. Slightly off-white text and avoiding very thin weights help.
  Pure black/white is neither mandatory nor prohibited. [H]
- Reduce chroma of large accent areas and re-test bright accents against dark
  surfaces. Re-check every pair with the WCAG 2 limits above in mind.
- Check images, logos and illustrations for dark-mode variants or backgrounds.

### Interactive products
- Make primary actions discoverable.
- Distinguish destructive actions with text and appropriate confirmation, not
  color alone.

### Data visualization
- Sequential data: lightness changes monotonically. Diverging data: palette
  centers on a meaningful midpoint. Avoid rainbow/jet scales for ordered data.
- Categorical data: keep the set small (roughly 6–8). Beyond that, group,
  highlight, or label directly. [H]
- Do not separate categories by red/green hue alone: also vary lightness, or
  use pairs like blue/orange, plus markers, patterns or direct labels.
- Give missing data its own style; never encode it like zero.
- Check color-vision-deficiency simulations and grayscale. Simulation does not
  replace contrast checks or users.

### User settings and theme implementation
- If both themes are supported, honor `prefers-color-scheme` initially, provide
  an accessible explicit override, persist it, and set `color-scheme` to the
  active theme so native controls match.
- Honor `prefers-contrast: more` (stronger borders and text) and, where
  feasible, `less`. Honor `prefers-reduced-transparency` by replacing
  translucent or blurred layers with opaque surfaces.
- Use `accent-color` to theme native checkboxes, radios and ranges instead of
  rebuilding them.
- Test `forced-colors: active`: rely on system colors (Canvas, CanvasText,
  LinkText, ButtonText, Highlight), keep focus and boundaries visible, and never
  set `forced-color-adjust: none` globally.
- Verify initial render (no wrong-theme flash), theme transitions, embedded
  content, illustrations and native controls.
- Do not add a second theme without scope approval when it significantly
  expands the work.

## 7. Implement and verify

Validate what users actually receive, not the intended palette.

- Use CSS custom properties or the existing token architecture. Preserve
  behavior, layout and typography unless a change is necessary and in scope.
  Avoid unnecessary dependencies.
- Measure rendered colors, not token definitions.
- Run automated checks when available (axe, Lighthouse, browser contrast
  tools). They miss or defer gradients, image backgrounds, pseudo-elements,
  overlays and many states, and they cover only part of accessibility. Treat
  "needs review" as unchecked, not as passed.
- Manually inspect representative pages at mobile and desktop sizes: both
  themes, keyboard focus, the state matrix, overlays, forced colors, increased
  contrast, and relevant color-vision simulations. Check text at its real size
  and weight.
- For meaningful tradeoffs, compare alternatives in realistic tasks: reading
  accuracy and speed, comprehension, completion, errors, subjective comfort. Do
  not present preference as measured performance.
- Report checks that could not be performed.

## 8. Required output

Use the formats in `references/output-template.md`. Do not produce a literature
review or fetch research by default; give the rationale, tradeoffs and measured
results that apply.

- **Palette proposal:** assumptions; semantic tokens with usable CSS values;
  key pair ratios with pass/fail; rationale tied to the task; remaining risks.
- **Audit:** findings ranked by accessibility impact, then task impact; affected
  components; specific fixes with measured replacement values.
- **Implementation:** changed files, checks run, unverified states.

Always keep measured results apart from targets and recommendations. Never call
a palette objectively optimal, or a site WCAG-compliant, on the basis of
palette tests alone.
