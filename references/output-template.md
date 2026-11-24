# Output templates

Use the template that matches the request. Every ratio must come from
`scripts/contrast.py`, browser inspection, or another real measurement; mark
anything else as "target" or "not measured".

## Palette proposal

### Assumptions
- Primary task / audience / themes / brand constraints, one line each.

### Tokens

| Token | Light | Dark | Paired with | Ratio (L / D) | Required | Status |
|---|---|---|---|---|---|---|
| `--color-text-primary` | `#1a1a1a` | `#e8e8e6` | `--color-surface-content` | … / … | 4.5 (target 7) | … |
| `--color-text-link` | … | … | surface, and `text-primary` | … / … | 4.5; 3 vs text if no underline | … |
| `--color-border-control` | … | … | adjacent surface | … | 3 | … |
| `--color-focus-ring` | … | … | every surface it can appear on | … | 3 | … |

Include every role the product uses, including states (hover, selected,
selected+focus, disabled) and feedback colors.

### CSS
```css
:root { color-scheme: light dark; /* primitives, then semantic tokens */ }
```

### Rationale
Short, tied to the task: why this hierarchy, where accent color is spent, what
was traded off.

### Reading comfort
- Expected session length and lighting:
- Comfort decisions (contrast band, surface tone, saturation, noise, luminance
  stability, theme options):
- Verified by: reader test (n, duration, ratings) / heuristic self-review only /
  not checked

### Measured vs. intended
- Measured: (pairs checked, tool used)
- Not measured: (gradients, images, forced colors, real devices, reader
  comfort testing)

### Remaining risks

## Audit

Order findings by accessibility impact, then task impact.

| # | Severity | Component / page | Problem (measured) | Criterion or rationale | Fix |
|---|---|---|---|---|---|
| 1 | Blocker | Form error state | Error shown only by red border; border 2.1:1 vs surface | SC 1.4.1, 1.4.11, 3.3.1 | Add error text tied with `aria-describedby`; border `#b3261e` (6.53:1 vs `#fff`) |

Severity: Blocker (content or action unusable for some users), Major (fails a
WCAG AA criterion or causes likely errors), Minor (hierarchy, consistency, or
reading comfort, e.g. glare, saturated backgrounds behind text, luminance
jumps), Suggestion. Escalate a comfort issue to Major when it affects the
primary reading surface of a long-reading product.

End with checks that were not performed.

## Implementation report
- Changed files
- Checks run (command or tool + result)
- States and conditions not verified
