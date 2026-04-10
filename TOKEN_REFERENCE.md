# SprouX Design System - Token Reference

**Purpose:** Quick reference for design tokens mapped to Tailwind CSS classes
**Source:** `SprouX_UI-UX team/design ops/figma-mappings/foundations.json`
**Version:** 3.0.0 (Pure Claude Code)
**Last Updated:** 2026-04-10

---

## How to Use This Reference

When generating web prototypes, use **Tailwind CSS classes** that map to design system tokens.

**Example:**
```html
<!-- Correct: Uses design system token classes -->
<div class="bg-card border border-border rounded-lg p-xl">
  <h3 class="text-foreground typo-heading-small">Title</h3>
  <p class="text-muted-foreground typo-paragraph-small">Description</p>
</div>

<!-- Incorrect: Custom CSS -->
<div style="background: #ffffff; border: 1px solid #e5e5e0; border-radius: 8px; padding: 24px;">
```

---

## Colors

### Background Colors

| Tailwind Class | Figma Variable | Usage |
|----------------|----------------|-------|
| `bg-background` | background | Page/app background |
| `bg-foreground` | foreground | Inverted background |
| `bg-card` | card | Card backgrounds |
| `bg-card-subtle` | card-subtle | Subtle card variant |
| `bg-popover` | popover | Popover/dropdown backgrounds |
| `bg-muted` | muted | Muted backgrounds |
| `bg-accent` | accent | Accent backgrounds |
| `bg-accent-selected` | accent-selected | Selected state |
| `bg-canvas` | canvas | Canvas/drawing areas |

### Primary/Brand Colors

| Tailwind Class | Figma Variable | Usage |
|----------------|----------------|-------|
| `bg-primary` | primary | Primary action backgrounds |
| `bg-primary-hover` | primary-hover | Primary hover state |
| `bg-primary-subtle` | primary-subtle | Subtle primary background |
| `bg-secondary` | secondary | Secondary action backgrounds |
| `bg-secondary-hover` | secondary-hover | Secondary hover state |
| `bg-brand` | brand | Brand color backgrounds |
| `bg-brand-hover` | brand-hover | Brand hover state |
| `bg-brand-subtle` | brand-subtle | Subtle brand background |

### Semantic Colors

| Tailwind Class | Figma Variable | Usage |
|----------------|----------------|-------|
| `bg-destructive` | destructive | Destructive/delete actions |
| `bg-destructive-subtle` | destructive-subtle | Subtle destructive background |
| `bg-success` | success | Success states |
| `bg-success-subtle` | success-subtle | Subtle success background |
| `bg-warning` | warning | Warning states |
| `bg-warning-subtle` | warning-subtle | Subtle warning background |
| `bg-emphasis` | emphasis | Emphasis/highlight |
| `bg-emphasis-subtle` | emphasis-subtle | Subtle emphasis background |

### Interactive States

| Tailwind Class | Figma Variable | Usage |
|----------------|----------------|-------|
| `bg-input` | input | Input field backgrounds |
| `bg-input-readonly` | input-readonly | Read-only input backgrounds |
| `bg-outline` | outline | Outline button backgrounds |
| `bg-outline-hover` | outline-hover | Outline hover state |
| `bg-ghost` | ghost | Ghost button backgrounds |
| `bg-ghost-hover` | ghost-hover | Ghost hover state |
| `bg-backdrop` | backdrop | Modal/dialog backdrops |

---

### Text Colors

| Tailwind Class | Figma Variable | Usage |
|----------------|----------------|-------|
| `text-foreground` | foreground | Primary text color |
| `text-foreground-subtle` | foreground-subtle | Subtle/secondary text |
| `text-muted-foreground` | muted-foreground | Muted/disabled text |
| `text-primary-foreground` | primary-foreground | Text on primary backgrounds |
| `text-secondary-foreground` | secondary-foreground | Text on secondary backgrounds |
| `text-accent-foreground` | accent-foreground | Text on accent backgrounds |
| `text-card-foreground` | card-foreground | Text on card backgrounds |
| `text-popover-foreground` | popover-foreground | Text on popover backgrounds |
| `text-destructive-foreground` | destructive-foreground | Text on destructive backgrounds |
| `text-success-foreground` | success-foreground | Text on success backgrounds |
| `text-warning-foreground` | warning-foreground | Text on warning backgrounds |
| `text-emphasis-foreground` | emphasis-foreground | Text on emphasis backgrounds |
| `text-brand-foreground` | brand-foreground | Text on brand backgrounds |

---

### Border Colors

| Tailwind Class | Figma Variable | Usage |
|----------------|----------------|-------|
| `border-border` | border | Default borders |
| `border-border-strong` | border-strong | Strong/emphasized borders |
| `border-border-subtle` | border-subtle | Subtle/light borders |
| `border-destructive` | destructive | Destructive/error borders |
| `border-success` | success | Success borders |
| `border-warning` | warning | Warning borders |
| `border-emphasis` | emphasis | Emphasis borders |
| `border-brand` | brand | Brand color borders |

---

### Focus Ring Colors

| Tailwind Class | Figma Variable | Usage |
|----------------|----------------|-------|
| `focus-ring` | ring | Default focus ring |
| `focus-ring-error` | ring-error | Error state focus |
| `focus-ring-success` | ring-success | Success state focus |
| `focus-ring-warning` | ring-warning | Warning state focus |
| `focus-ring-brand` | ring-brand | Brand color focus |
| `focus-ring-emphasis` | ring-emphasis | Emphasis focus |

**Focus Ring Pattern:**
```html
<button class="focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2">
  Button
</button>
```

---

## Typography

### Font Families

| Purpose | CSS Variable | Value |
|---------|-------------|-------|
| **Sans Serif** | `--font-sans` | 'Geist', system-ui, sans-serif |
| **Monospace** | `--font-mono` | 'Geist Mono', ui-monospace, monospace |
| **Heading** | `--font-heading` | 'Fraunces', serif |

### Typography Classes

| Class | Usage | Font | Size | Weight |
|-------|-------|------|------|--------|
| `typo-heading-large` | Page titles | Heading | 32px | 600 |
| `typo-heading-medium` | Section titles | Heading | 24px | 600 |
| `typo-heading-small` | Subsection titles | Heading | 18px | 600 |
| `typo-paragraph-regular` | Body text | Sans | 16px | 400 |
| `typo-paragraph-small` | Small body text | Sans | 14px | 400 |
| `typo-paragraph-small-semibold` | Emphasized small text | Sans | 14px | 600 |
| `typo-paragraph-mini` | Caption/meta text | Sans | 12px | 400 |
| `typo-paragraph-mini-semibold` | Emphasized captions | Sans | 12px | 600 |

---

## Spacing

### Gap (Flex/Grid Spacing)

| Class | Value | Pixels |
|-------|-------|--------|
| `gap-4xs` | 2px | 2 |
| `gap-3xs` | 4px | 4 |
| `gap-2xs` | 6px | 6 |
| `gap-xs` | 8px | 8 |
| `gap-sm` | 12px | 12 |
| `gap-md` | 16px | 16 |
| `gap-lg` | 20px | 20 |
| `gap-xl` | 24px | 24 |
| `gap-2xl` | 32px | 32 |
| `gap-3xl` | 40px | 40 |
| `gap-4xl` | 48px | 48 |
| `gap-5xl` | 64px | 64 |

### Padding

| Class | Value | Use For |
|-------|-------|---------|
| `p-3xs` | 4px | Minimal padding |
| `p-2xs` | 6px | Tight padding |
| `p-xs` | 8px | Small padding |
| `p-sm` | 12px | Compact padding |
| `p-md` | 16px | Standard padding |
| `p-lg` | 20px | Comfortable padding |
| `p-xl` | 24px | Spacious padding |
| `p-2xl` | 32px | Large padding |

**Directional variants:**
- `px-md` - Horizontal padding (left + right)
- `py-md` - Vertical padding (top + bottom)
- `pt-md` - Top padding
- `pr-md` - Right padding
- `pb-md` - Bottom padding
- `pl-md` - Left padding

### Margin

| Class | Value | Use For |
|-------|-------|---------|
| `m-xs` | 8px | Small margin |
| `m-sm` | 12px | Standard margin |
| `m-md` | 16px | Medium margin |
| `m-lg` | 20px | Large margin |
| `m-xl` | 24px | Extra large margin |
| `m-2xl` | 32px | Spacious margin |

**Directional variants:**
- `mx-auto` - Center horizontally
- `mt-xl` - Top margin
- `mb-md` - Bottom margin
- etc.

---

## Sizing

### Component Heights

| Class | Value | Use For |
|-------|-------|---------|
| `h-size-xs` | 24px | Mini components |
| `h-size-sm` | 32px | Small components |
| `h-size-md` | 36px | Regular/Default components |
| `h-size-lg` | 40px | Large components |
| `h-size-xl` | 48px | Extra large components |

**Usage:**
```html
<button class="h-size-md px-md">Default Button</button>
<button class="h-size-lg px-lg">Large Button</button>
```

### Icon Sizes

| Class | Value | Use For |
|-------|-------|---------|
| `size-icon-xs` | 12px | Mini icons |
| `size-icon-sm` | 16px | Small icons |
| `size-icon-md` | 20px | Regular icons |
| `size-icon-lg` | 24px | Large icons |
| `size-icon-xl` | 32px | Extra large icons |

### Width/Height Utilities

| Class | Value |
|-------|-------|
| `size-xs` | 24px × 24px |
| `size-sm` | 32px × 32px |
| `size-md` | 40px × 40px |
| `size-lg` | 48px × 48px |

---

## Border Radius

| Class | Value | Use For |
|-------|-------|---------|
| `rounded-sm` | 4px | Subtle rounding |
| `rounded` | 6px | Default rounding |
| `rounded-md` | 6px | Medium rounding |
| `rounded-lg` | 8px | Large rounding |
| `rounded-xl` | 12px | Extra large rounding |
| `rounded-2xl` | 16px | Very large rounding |
| `rounded-full` | 9999px | Circles/pills |

**Custom SprouX radius:**
| Class | Value | Note |
|-------|-------|------|
| `rounded-10` | 10px | Custom SprouX value (not in default Tailwind) |

---

## Shadows

| Name | Value | Use For |
|------|-------|---------|
| **shadow-sm** | 0 1px 2px rgba(...) | Subtle elevation |
| **shadow** | 0 2px 4px rgba(...) | Default shadow |
| **shadow-md** | 0 4px 6px rgba(...) | Medium elevation |
| **shadow-lg** | 0 10px 15px rgba(...) | High elevation |
| **shadow-xl** | 0 20px 25px rgba(...) | Very high elevation |
| **shadow-2xl** | 0 25px 50px rgba(...) | Maximum elevation |

**Usage:**
```html
<div class="shadow-md rounded-lg bg-card">Card with shadow</div>
```

---

## Letter Spacing

| Purpose | Value |
|---------|-------|
| **Tight** | -0.01em |
| **Normal** | 0em |
| **Wide** | 0.02em |

---

## Quick Reference: Common Combinations

### Card
```html
<div class="bg-card border border-border rounded-lg p-xl shadow-sm">
  <h3 class="text-foreground typo-heading-small mb-xs">Title</h3>
  <p class="text-muted-foreground typo-paragraph-small">Content</p>
</div>
```

### Primary Button
```html
<button class="bg-primary text-primary-foreground h-size-md px-md rounded-lg typo-paragraph-small-semibold">
  Submit
</button>
```

### Input Field
```html
<input
  type="text"
  class="h-size-md px-md rounded-lg border border-input bg-background text-foreground typo-paragraph-small"
  placeholder="Enter text" />
```

### Success Badge
```html
<span class="bg-success-subtle text-success-foreground px-sm py-3xs rounded typo-paragraph-mini-semibold">
  Active
</span>
```

---

## Loading Design Tokens

**Before generating prototypes, read the design system configuration:**

```
1. Read: SprouX_UI-UX team/design ops/figma-mappings/foundations.json
2. Read: SprouX_UI-UX team/design ops/figma-mappings/components.json
3. Use classes from this reference
4. Add metadata attributes (data-component, data-variant, etc.)
```

---

## Total Token Count

**Category Breakdown:**
- **Colors:** 73 token mappings
- **Typography:** 13 text styles
- **Spacing:** 41 spacing tokens
- **Sizing:** 23 sizing tokens
- **Radius:** 11 border radius values
- **Shadows:** 6 shadow definitions
- **Letter Spacing:** 2 tracking values

**Total:** 169 design tokens

---

**For complete token definitions, see:**
- `SprouX_UI-UX team/design ops/figma-mappings/foundations.json`
- `SprouX_design system/src/index.css` (CSS custom properties)
