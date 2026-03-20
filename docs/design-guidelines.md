# MEDGRAPH — Design Guidelines

## Color Palette

### Severity System
| Severity | Token | Tailwind | Hex (light) |
|----------|-------|----------|-------------|
| Critical | `--color-critical` | `red-600` | `#dc2626` |
| Major | `--color-major` | `orange-500` | `#f97316` |
| Moderate | `--color-moderate` | `yellow-500` | `#eab308` |
| Minor | `--color-minor` | `blue-400` | `#60a5fa` |

### UI Colors
| Role | Token | Value |
|------|-------|-------|
| Primary action | `--color-primary` | `blue-600` (#2563eb) |
| Surface | `--color-surface` | white / gray-950 |
| Border | `--color-border` | gray-200 / gray-800 |
| Muted text | `--color-muted` | gray-500 |
| Disclaimer bg | `--color-disclaimer` | amber-50 / amber-950 |

---

## Typography
- **Font stack**: `system-ui, -apple-system, "Segoe UI", Roboto, sans-serif`
- **Monospace** (drug IDs, enzyme codes): `ui-monospace, "Cascadia Code", monospace`
- Scale: Tailwind defaults (`text-sm`, `text-base`, `text-lg`, `text-xl`, `text-2xl`)
- Drug names: `font-semibold`; severity labels: `font-bold uppercase text-xs tracking-wide`

---

## Themes

### Light (default)
- Background: `white` / `gray-50`
- Card surface: `white` with `gray-200` border
- Primary text: `gray-900`

### Dark
- Background: `gray-950`
- Card surface: `gray-900` with `gray-800` border
- Primary text: `gray-50`
- Theme toggled via `dark` class on `<html>`; CSS variables swap automatically

---

## Component Patterns

### Severity Badge
```
[CRITICAL]   bg-red-100 text-red-700 border border-red-300   (+ icon: ⚠)
[MAJOR]      bg-orange-100 text-orange-700
[MODERATE]   bg-yellow-100 text-yellow-700
[MINOR]      bg-blue-100 text-blue-700
```
Always pair color with a text label and icon — never color alone (color-blind friendly).

### Interaction Card
- White card, `rounded-xl shadow-sm border`
- Header: drug pair names + severity badge (right-aligned)
- Body: mechanism description, cascade path, evidence toggle

### Progress / Risk Bar
- Horizontal bar, width = `risk_score / 100 * 100%`
- Color transitions: green (0–30) → yellow (30–60) → orange (60–80) → red (80–100)

### Cascade Path Steps
- Numbered steps in a vertical timeline
- Each step: source → relation arrow → target (enzyme or drug)
- Final step highlights toxicity outcome in `red-100` bubble

---

## Medical Disclaimer Banner
- **Always visible** at top of every page (part of `AppShell`)
- Background: `amber-50` border `amber-300` text `amber-900`
- Text: _"This tool is for informational purposes only. It does not constitute medical advice. Always consult a qualified healthcare professional."_
- Must not be dismissible or hidden by any layout change

---

## Responsive Breakpoints
| Breakpoint | Width | Layout |
|-----------|-------|--------|
| Mobile | 375 px | Single column, stacked cards |
| Tablet | 768 px | Two-column results grid |
| Desktop | 1280 px | Sidebar + main content |

Use Tailwind responsive prefixes: `sm:` (640), `md:` (768), `lg:` (1024), `xl:` (1280).

---

## Accessibility
- Target: **WCAG 2.1 AA**
- All interactive elements keyboard-navigable (visible `:focus-visible` ring)
- Severity conveyed by icon + text, not color alone
- `aria-label` on icon-only buttons; `role="alert"` on error messages
- Minimum contrast ratio: 4.5:1 for body text, 3:1 for large text
- `<html lang="en">` set; landmark regions (`<main>`, `<nav>`, `<aside>`)
