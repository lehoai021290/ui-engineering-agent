# SprouX Design System - Component HTML Patterns

**Purpose:** Reference guide for generating design-system-compliant HTML components
**Target:** Claude Code agents implementing Workflow 2 (Generate Web Prototype)
**Source:** Extracted from `web_prototype_generation.py` patterns
**Version:** 3.0.0 (Pure Claude Code)
**Last Updated:** 2026-04-10

---

## Critical Requirements

### 1. Link to SprouX Design System CSS (MANDATORY)

**Every HTML prototype MUST include in `<head>`:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Page Title</title>

    <!-- CRITICAL: Link to SprouX design system foundation -->
    <link rel="stylesheet" href="../../SprouX_design system/src/index.css">

    <!-- Tailwind CDN for utility classes -->
    <script src="https://cdn.tailwindcss.com"></script>
</head>
```

**Why:**
- `index.css` contains all foundation tokens (colors, spacing, typography, radius, shadows)
- DO NOT replicate CSS variables - use the design system file
- Design tokens are maintained in one place

### 2. Always Include Metadata Attributes

**Required on every component:**
```html
data-component="ComponentName"   <!-- Exact component name for 90-95% mapping accuracy -->
data-variant="variantName"       <!-- Component variant (when applicable) -->
data-size="sizeName"             <!-- Component size (when applicable) -->
data-figma-node="nodeId"         <!-- Figma node ID from components.json -->
```

**Why:** These attributes enable **90-95% Figma mapping accuracy** vs 60-70% with inference alone.

### 3. Use Tailwind CSS Classes That Map to Design Tokens

**Correct:**
```html
<button class="bg-primary text-primary-foreground rounded-lg px-md py-sm">
```
(Classes map to CSS variables defined in `index.css`)

**Incorrect:**
```html
<button style="background-color: #3b82f6; color: white;">
```
(Hardcoded values bypass design system)

### 4. Load Design System Context

Before generating components, read:
- `SprouX_UI-UX team/design ops/figma-mappings/components.json` - Get Figma node IDs
- `SprouX_UI-UX team/design ops/figma-mappings/foundations.json` - Get design tokens
- `SprouX_design system/src/components/ui/` - Reference React component structure

---

## Component Patterns

### Button

**Figma Node:** `9:1071`

**Base Structure:**
```html
<button
  class="inline-flex items-center justify-center h-size-md px-md gap-xs rounded-lg [variant-classes] typo-paragraph-small-semibold"
  data-component="Button"
  data-variant="[variant]"
  data-size="default"
  data-figma-node="9:1071">
  Button Text
</button>
```

**Variants:**

| Variant | Classes |
|---------|---------|
| **primary** | `bg-primary text-primary-foreground` |
| **secondary** | `bg-secondary text-secondary-foreground` |
| **outline** | `border border-border bg-outline text-foreground` |
| **destructive** | `bg-destructive text-destructive-foreground` |
| **ghost** | `bg-transparent text-foreground hover:bg-accent` |

**Example - Primary Button:**
```html
<button
  class="inline-flex items-center justify-center h-size-md px-md gap-xs rounded-lg bg-primary text-primary-foreground typo-paragraph-small-semibold"
  data-component="Button"
  data-variant="primary"
  data-size="default"
  data-figma-node="9:1071">
  Submit
</button>
```

**Example - Destructive Button:**
```html
<button
  class="inline-flex items-center justify-center h-size-md px-md gap-xs rounded-lg bg-destructive text-destructive-foreground typo-paragraph-small-semibold"
  data-component="Button"
  data-variant="destructive"
  data-size="default"
  data-figma-node="9:1071">
  Delete
</button>
```

---

### Badge

**Figma Node:** `19:6979`

**Base Structure:**
```html
<span
  class="inline-flex items-center px-sm py-3xs rounded [variant-classes] typo-paragraph-mini-semibold"
  data-component="Badge"
  data-variant="[variant]"
  data-figma-node="19:6979">
  Badge Text
</span>
```

**Variants:**

| Variant | Classes |
|---------|---------|
| **default** | `bg-primary text-primary-foreground` |
| **secondary** | `bg-secondary text-secondary-foreground` |
| **success** | `bg-success-subtle text-success-foreground` |
| **warning** | `bg-warning-subtle text-warning-foreground` |
| **destructive** | `bg-destructive-subtle text-destructive-foreground` |
| **outline** | `border border-border bg-transparent text-foreground` |

**Example - Success Badge:**
```html
<span
  class="inline-flex items-center px-sm py-3xs rounded bg-success-subtle text-success-foreground typo-paragraph-mini-semibold"
  data-component="Badge"
  data-variant="success"
  data-figma-node="19:6979">
  Active
</span>
```

---

### Alert

**Figma Node:** Check `components.json` for Alert node ID

**Base Structure:**
```html
<div
  class="p-md rounded-lg [variant-classes] border-l-4 [border-variant]"
  data-component="Alert"
  data-variant="[variant]"
  data-figma-node="[nodeId]">
  <p class="typo-paragraph-small-semibold [text-variant]">Title</p>
  <p class="typo-paragraph-small text-foreground-subtle mt-2xs">Message text</p>
</div>
```

**Variants:**

| Variant | Background | Border | Title Text |
|---------|------------|--------|------------|
| **default** | `bg-primary-subtle` | `border-primary` | `text-foreground` |
| **success** | `bg-success-subtle` | `border-success` | `text-success-foreground` |
| **warning** | `bg-warning-subtle` | `border-warning` | `text-warning-foreground` |
| **destructive** | `bg-destructive-subtle` | `border-destructive` | `text-destructive-foreground` |

**Example - Error Alert:**
```html
<div
  class="p-md rounded-lg bg-destructive-subtle border-l-4 border-destructive"
  data-component="Alert"
  data-variant="destructive"
  data-figma-node="[Alert-nodeId]">
  <p class="typo-paragraph-small-semibold text-destructive-foreground">Error</p>
  <p class="typo-paragraph-small text-foreground-subtle mt-2xs">Something went wrong. Please try again.</p>
</div>
```

---

### Card

**Figma Node:** `179:29234`

**Base Structure:**
```html
<div
  class="p-xl rounded-lg bg-card border border-border"
  data-component="Card"
  data-figma-node="179:29234">
  <h3 class="typo-heading-small text-foreground mb-xs">Card Title</h3>
  <p class="typo-paragraph-small text-muted-foreground">Card content and description.</p>
</div>
```

**Example - Stat Card:**
```html
<div
  class="p-xl rounded-lg bg-card border border-border"
  data-component="Card"
  data-figma-node="179:29234">
  <p class="typo-paragraph-small text-muted-foreground mb-xs">Total Revenue</p>
  <p class="typo-heading-large text-foreground">$45,231</p>
  <p class="typo-paragraph-mini text-success-foreground mt-xs">+12% from last month</p>
</div>
```

---

### Input

**Figma Node:** Check `components.json` for Input node ID

**Base Structure:**
```html
<input
  type="[type]"
  placeholder="[placeholder]"
  class="h-size-md px-md rounded-lg border [state-border] bg-background text-foreground typo-paragraph-small"
  data-component="Input"
  data-size="default"
  data-state="[state]"
  data-figma-node="[nodeId]" />
```

**States:**

| State | Border Class |
|-------|-------------|
| **default** | `border-input` |
| **error** | `border-destructive` |
| **disabled** | `border-border opacity-50` |

**Example - Email Input:**
```html
<input
  type="email"
  placeholder="Email address"
  class="h-size-md px-md rounded-lg border border-input bg-background text-foreground typo-paragraph-small"
  data-component="Input"
  data-size="default"
  data-state="default"
  data-figma-node="[Input-nodeId]" />
```

**Example - Error State Input:**
```html
<input
  type="text"
  placeholder="Username"
  class="h-size-md px-md rounded-lg border border-destructive bg-background text-foreground typo-paragraph-small"
  data-component="Input"
  data-size="default"
  data-state="error"
  data-figma-node="[Input-nodeId]"
  aria-invalid="true"
  aria-describedby="username-error" />
<p id="username-error" class="text-destructive typo-paragraph-mini mt-xs">Username is required</p>
```

---

### Checkbox

**Figma Node:** Check `components.json` for Checkbox node ID

**Base Structure:**
```html
<label class="flex items-center gap-xs">
  <input
    type="checkbox"
    class="size-md rounded border-border"
    data-component="Checkbox"
    data-state="[checked|unchecked]"
    data-figma-node="[nodeId]" />
  <span class="typo-paragraph-small text-foreground">Label text</span>
</label>
```

**Example:**
```html
<label class="flex items-center gap-xs">
  <input
    type="checkbox"
    checked
    class="size-md rounded border-border"
    data-component="Checkbox"
    data-state="checked"
    data-figma-node="[Checkbox-nodeId]" />
  <span class="typo-paragraph-small text-foreground">I agree to terms and conditions</span>
</label>
```

---

### Avatar

**Figma Node:** `18:1398`

**Base Structure:**
```html
<div
  class="size-[size] rounded-full bg-[color] flex items-center justify-center typo-paragraph-small-semibold text-[text-color]"
  data-component="Avatar"
  data-size="[size]"
  data-figma-node="18:1398">
  [Initials]
</div>
```

**Sizes:**

| Size | Width/Height |
|------|--------------|
| **xs** | `24px` (size-xs) |
| **sm** | `32px` (size-sm) |
| **md** | `40px` (size-md) |
| **lg** | `48px` (size-lg) |

**Example:**
```html
<div
  class="size-md rounded-full bg-primary flex items-center justify-center typo-paragraph-small-semibold text-primary-foreground"
  data-component="Avatar"
  data-size="md"
  data-figma-node="18:1398">
  JD
</div>
```

---

### Accordion

**Figma Node:** `66:5034`

**Base Structure:**
```html
<div
  class="accordion bg-card border border-border rounded-lg overflow-hidden"
  data-component="Accordion"
  data-figma-node="66:5034">
  <button
    class="accordion-header flex items-center justify-between w-full p-md hover:bg-accent"
    aria-expanded="false"
    aria-controls="accordion-content-1">
    <span class="typo-paragraph-base-medium text-foreground">Accordion Title</span>
    <span class="text-muted-foreground">›</span>
  </button>
  <div
    id="accordion-content-1"
    class="accordion-content hidden p-md border-t border-border">
    <p class="typo-paragraph-small text-muted-foreground">Accordion content goes here.</p>
  </div>
</div>
```

---

## Layout Patterns

### Container

**Desktop-first responsive container:**
```html
<div class="container max-w-screen-xl mx-auto px-xl py-2xl">
  <!-- Content -->
</div>
```

**Breakpoints:**
- Desktop: `max-w-screen-xl` (1280px)
- Tablet: Media query at 1024px
- Mobile: Media query at 768px

---

### Grid Layout

**4-column grid (desktop):**
```html
<div class="grid grid-cols-4 gap-md">
  <div class="bg-card border border-border rounded-lg p-lg">Column 1</div>
  <div class="bg-card border border-border rounded-lg p-lg">Column 2</div>
  <div class="bg-card border border-border rounded-lg p-lg">Column 3</div>
  <div class="bg-card border border-border rounded-lg p-lg">Column 4</div>
</div>
```

**Responsive grid:**
```html
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-md">
  <!-- Columns -->
</div>
```

---

### Flex Layout

**Horizontal flex with gap:**
```html
<div class="flex flex-wrap gap-md items-center">
  <button>Button 1</button>
  <button>Button 2</button>
  <button>Button 3</button>
</div>
```

**Vertical stack:**
```html
<div class="flex flex-col gap-lg">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
</div>
```

---

## Typography Classes

| Purpose | Class |
|---------|-------|
| **Large Heading** | `typo-heading-large` |
| **Medium Heading** | `typo-heading-medium` |
| **Small Heading** | `typo-heading-small` |
| **Regular Paragraph** | `typo-paragraph-regular` |
| **Small Paragraph** | `typo-paragraph-small` |
| **Semibold Paragraph** | `typo-paragraph-small-semibold` |
| **Mini Text** | `typo-paragraph-mini` |
| **Mini Semibold** | `typo-paragraph-mini-semibold` |

---

## Color Classes

### Background Colors

| Purpose | Class |
|---------|-------|
| **Primary** | `bg-primary` |
| **Secondary** | `bg-secondary` |
| **Destructive** | `bg-destructive` |
| **Success** | `bg-success` |
| **Warning** | `bg-warning` |
| **Card** | `bg-card` |
| **Background** | `bg-background` |
| **Muted** | `bg-muted` |
| **Accent** | `bg-accent` |

### Text Colors

| Purpose | Class |
|---------|-------|
| **Foreground** | `text-foreground` |
| **Muted** | `text-muted-foreground` |
| **Primary** | `text-primary-foreground` |
| **Destructive** | `text-destructive-foreground` |
| **Success** | `text-success-foreground` |
| **Warning** | `text-warning-foreground` |

### Border Colors

| Purpose | Class |
|---------|-------|
| **Default** | `border-border` |
| **Input** | `border-input` |
| **Primary** | `border-primary` |
| **Destructive** | `border-destructive` |

---

## Spacing Classes

| Size | Class (Gap) | Class (Padding) | Value |
|------|-------------|-----------------|-------|
| **3xs** | `gap-3xs` | `p-3xs` | 4px |
| **2xs** | `gap-2xs` | `p-2xs` | 6px |
| **xs** | `gap-xs` | `p-xs` | 8px |
| **sm** | `gap-sm` | `p-sm` | 12px |
| **md** | `gap-md` | `p-md` | 16px |
| **lg** | `gap-lg` | `p-lg` | 20px |
| **xl** | `gap-xl` | `p-xl` | 24px |
| **2xl** | `gap-2xl` | `p-2xl` | 32px |

---

## Border Radius Classes

| Size | Class | Value |
|------|-------|-------|
| **Small** | `rounded-sm` | 4px |
| **Default** | `rounded` | 6px |
| **Medium** | `rounded-md` | 6px |
| **Large** | `rounded-lg` | 8px |
| **XL** | `rounded-xl` | 12px |
| **2XL** | `rounded-2xl` | 16px |
| **Full** | `rounded-full` | 9999px (circle) |

---

## Component Grouping

When showcasing multiple component variants, use `data-component-group`:

```html
<div class="flex flex-wrap gap-md" data-component-group="buttons">
  <button data-component="Button" data-variant="primary">Primary</button>
  <button data-component="Button" data-variant="secondary">Secondary</button>
  <button data-component="Button" data-variant="outline">Outline</button>
</div>
```

---

## Generic Component Fallback

For components not listed above, use this generic pattern:

```html
<div
  class="p-md rounded border border-border bg-muted/50"
  data-component="[ComponentName]"
  data-figma-node="[nodeId]">
  <p class="typo-paragraph-small text-muted-foreground">[ComponentName] component example</p>
</div>
```

---

## Critical Reminders

1. ✅ **ALWAYS include `data-component` attribute** - This is non-negotiable
2. ✅ **ALWAYS include `data-figma-node`** - Read from `components.json`
3. ✅ **Use Tailwind classes** - Never use inline styles or custom CSS classes
4. ✅ **Add Tailwind CDN** - Include `<script src="https://cdn.tailwindcss.com"></script>` in `<head>`
5. ✅ **Desktop-first responsive** - Base styles for 1440px, override for smaller screens
6. ✅ **Semantic HTML** - Use proper `<button>`, `<input>`, `<label>`, etc.
7. ✅ **Accessibility** - Include ARIA attributes when appropriate

---

**For questions or missing components, check:**
- `SprouX_UI-UX team/design ops/figma-mappings/components.json` - All 53 components
- `SprouX_UI-UX team/design-system-component-usage-guidelines.md` - Component guidelines
