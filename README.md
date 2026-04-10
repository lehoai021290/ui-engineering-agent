# Nexus - UI Engineering Agent

**Version:** 3.0.0
**Type:** Pure Claude Code Agent
**Status:** ✅ Active
**Last Updated:** 2026-04-10

---

## Overview

**Nexus** is a specialized Claude Code subagent that transforms design specifications into functional web prototypes and Figma designs using the SprouX design system.

### Key Capabilities

- ✅ **Design-to-Code Translation** - Converts specs, wireframes, or prompts into prototypes
- ✅ **Design System Integration** - Uses SprouX components and tokens (53 components, 169 tokens)
- ✅ **Figma UI Generation** - Captures prototypes to Figma with automated component mapping
- ✅ **Accessibility Validation** - WCAG 2.1 AA compliance checking
- ✅ **Autonomous Decision-Making** - Makes informed design decisions when specs are incomplete
- ✅ **Desktop-First Responsive** - Optimized for 1440px → 375px breakpoints

---

## How It Works

Nexus operates as a **Claude Code subagent** invoked via the Task tool:

### Invocation

```markdown
When the user mentions:
- "Generate web prototype"
- "Create Figma design from prototype"
- "Build UI from wireframes"
- "Generate dashboard from requirements"

Use the Task tool with subagent_type="ui-engineering"
```

### What Happens

1. Claude Code launches Nexus as a subagent
2. Nexus reads `SYSTEM_PROMPT.md` for workflow instructions
3. Executes the appropriate workflow (Parse → Prototype → Figma → Validate)
4. Returns results to the main Claude Code session

---

## Workflows

Nexus executes **4 core workflows** documented in `SYSTEM_PROMPT.md`:

### 1. Parse Requirements
**Input:** Design specs, wireframes, requirements, or prompts
**Output:** Structured requirements with component list and layout

**Use when:** User provides incomplete or unstructured input

---

### 2. Generate Web Prototype
**Input:** Structured requirements (from Workflow 1)
**Output:** HTML/CSS/JS files using SprouX design system

**Critical Requirements:**
- ✅ **Links to `SprouX_design system/src/index.css`** (foundation tokens)
- ✅ **References React components** from `src/components/ui/` (structure patterns)
- ✅ **Uses Tailwind classes** that map to design tokens
- ✅ **NO replicated CSS variables** (must use `index.css`)

**Features:**
- Tailwind CSS classes mapped to design tokens from `index.css`
- Metadata attributes for 90-95% Figma mapping accuracy
- Desktop-first responsive design
- Accessibility attributes (ARIA, semantic HTML)

**Example Output:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <!-- CRITICAL: Link to SprouX design system -->
    <link rel="stylesheet" href="../../SprouX_design system/src/index.css">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body>
    <button
      class="inline-flex items-center justify-center h-9 px-4 rounded-lg bg-primary text-primary-foreground"
      data-component="Button"
      data-variant="primary"
      data-size="default"
      data-figma-node="9:1071">
      Submit
    </button>
</body>
</html>
```

---

### 3. Generate Figma UI
**Input:** Web prototype (HTML file)
**Output:** Figma design with component mapping

**5-Step Process:**
1. Capture web prototype to Figma
2. Load design system mappings (`components.json`, `foundations.json`)
3. Replace generic layers with SprouX component instances
4. Apply foundation tokens (colors, spacing, typography)
5. Generate human-friendly mapping report (terminal output)

**Automation:** ~80% automated, ~20% manual refinement needed

---

### 4. Validate Accessibility
**Input:** Web prototype
**Output:** WCAG 2.1 AA compliance report

**Checks:**
- Semantic HTML structure
- ARIA attributes
- Color contrast (4.5:1 for text, 3:1 for UI)
- Keyboard navigation
- Form accessibility

---

## Architecture

### Pure Claude Code Agent

```
User Request
    ↓
Claude Code (Main Session)
    ↓
Task Tool (subagent_type="ui-engineering")
    ↓
Nexus Subagent
    ├─ Reads: SYSTEM_PROMPT.md (workflow instructions)
    ├─ Reads: COMPONENT_PATTERNS.md (component HTML patterns)
    ├─ Reads: TOKEN_REFERENCE.md (design token reference)
    ├─ Loads: figma-mappings/*.json (design system data)
    └─ Executes: Workflows (Parse → Prototype → Figma → Validate)
    ↓
Returns Results to Main Session
```

**No Python Dependencies** - Pure prompt-based generation using MCP tools

---

## Files & Documentation

### Core Files

| File | Purpose |
|------|---------|
| `SYSTEM_PROMPT.md` | Complete workflow instructions (loaded by Claude Code) |
| `COMPONENT_PATTERNS.md` | HTML patterns for all 53 SprouX components |
| `TOKEN_REFERENCE.md` | Design token reference (169 tokens) |
| `AGENT.md` | Agent metadata and capabilities |
| `LESSONS_LEARNED.md` | Internal notes and patterns |
| `README.md` | This file - User guide |

### Templates

| File | Purpose |
|------|---------|
| `templates/implementation_review.md` | Output template for implementation reviews |

### Reference Files (Not Executed)

| Directory | Purpose |
|-----------|---------|
| `skills/` | Python reference implementations (not executed by agent) |
| `tools/` | Python utility references (not executed by agent) |

**Note:** Python files in `skills/` and `tools/` are **reference documentation only**. Nexus doesn't execute Python code - all logic is implemented in SYSTEM_PROMPT.md using prompt-based instructions.

---

## Design System Integration

### SprouX Design System

**Location:** `SprouX_UI-UX team/design ops/figma-mappings/`

**Components:**
- **Total:** 53 mapped components
- **Categories:** Core (11), Common (25), Specialized (10), Utility (7)
- **Figma Library:** `ihKZCnJS2UrsQzpzEFYI4u` ([SprouX - DS] Foundation & Component)

**Foundation Tokens:**
- **Colors:** 73 tokens (backgrounds, text, borders, focus rings)
- **Typography:** 13 text styles
- **Spacing:** 41 spacing tokens
- **Sizing:** 23 sizing tokens
- **Radius:** 11 border radius values
- **Shadows:** 6 shadow definitions
- **Total:** 169 tokens

### Component Mapping

**Automation Level:** ~80% automated

**How It Works:**
1. Metadata attributes in HTML (`data-component="Button"`, `data-figma-node="9:1071"`)
2. Figma MCP tools import components from library
3. Replace captured HTML elements with SprouX component instances
4. Apply design tokens as Figma variables

**Accuracy:** 90-95% with metadata attributes vs 60-70% without

---

## Quality Standards

| Aspect | Standard |
|--------|----------|
| **Accessibility** | WCAG 2.1 AA compliance minimum |
| **Performance** | Lighthouse score > 90 |
| **Responsive** | Desktop-first (1440px → 1024px → 768px → 375px) |
| **Design System** | 100% component mapping when available |
| **Code Quality** | Semantic HTML, Tailwind CSS, ARIA attributes |

---

## Example Usage

### Scenario: Generate Dashboard from Requirements

**User Request:**
```
Generate a creator dashboard with:
- Stats cards showing campaigns, revenue, backers
- Action feed with priority-based tasks
- Recent activity timeline
- Community panel
```

**What Nexus Does:**

1. **Parse Requirements** (Workflow 1)
   - Identifies components: Card, Badge, Button, Accordion
   - Structures layout: Grid for stats, feed for actions, columns for bottom section

2. **Generate Prototype** (Workflow 2)
   - Creates HTML with Tailwind classes: `bg-card`, `border-border`, `rounded-lg`, `p-xl`
   - Adds metadata: `data-component="Card"`, `data-figma-node="179:29234"`
   - Implements desktop-first responsive: `grid-cols-4` → `grid-cols-2` → `grid-cols-1`

3. **Generate Figma UI** (Workflow 3)
   - Captures prototype to Figma
   - Replaces generic cards with SprouX Card component instances
   - Applies design tokens (colors, spacing, typography)
   - Outputs mapping report to terminal

4. **Validate Accessibility** (Workflow 4)
   - Checks semantic HTML (`<main>`, `<section>`, `<article>`)
   - Verifies ARIA labels on interactive elements
   - Tests color contrast ratios
   - Generates accessibility report

**Deliverables:**
- `index.html` - Prototype with design system integration
- `styles.css` - Minimal custom CSS (Tailwind handles most)
- Figma design URL with 80% automation coverage
- Accessibility audit report

---

## Workflow Scenarios

### Scenario A: Full Pipeline
```
User provides: Wireframes + Design Specs
    ↓
Parse Requirements → Generate Prototype → Generate Figma → Validate
    ↓
Deliver: Prototype + Figma + Audit
```

### Scenario B: Prototype Only
```
User provides: Requirements or prompt
    ↓
Parse Requirements → Generate Prototype → Validate
    ↓
Deliver: Prototype + Audit
```

### Scenario C: Figma from Existing Prototype
```
User provides: HTML file path
    ↓
Generate Figma UI
    ↓
Deliver: Figma design
```

### Scenario D: Autonomous (Minimal Input)
```
User says: "Build a login page"
    ↓
Parse → Infer Components → Generate → Figma → Validate
    ↓
Deliver: Prototype + Figma + Audit + Decision Log
```

---

## Quick Reference

### Common Components

See `COMPONENT_PATTERNS.md` for complete patterns.

**Button:**
```html
<button class="inline-flex items-center justify-center h-size-md px-md gap-xs rounded-lg bg-primary text-primary-foreground typo-paragraph-small-semibold"
        data-component="Button" data-variant="primary" data-size="default" data-figma-node="9:1071">
  Text
</button>
```

**Badge:**
```html
<span class="inline-flex items-center px-sm py-3xs rounded bg-success-subtle text-success-foreground typo-paragraph-mini-semibold"
      data-component="Badge" data-variant="success" data-figma-node="19:6979">
  Active
</span>
```

**Card:**
```html
<div class="p-xl rounded-lg bg-card border border-border" data-component="Card" data-figma-node="179:29234">
  <h3 class="typo-heading-small text-foreground mb-xs">Title</h3>
  <p class="typo-paragraph-small text-muted-foreground">Content</p>
</div>
```

### Common Tokens

See `TOKEN_REFERENCE.md` for complete reference.

**Colors:** `bg-primary`, `text-foreground`, `border-border`
**Spacing:** `gap-md`, `px-xl`, `py-sm`
**Typography:** `typo-heading-large`, `typo-paragraph-small`
**Sizing:** `h-size-md`, `size-icon-lg`
**Radius:** `rounded-lg`, `rounded-full`

---

## Troubleshooting

### Issue: Prototype doesn't use design system correctly

**Symptoms:**
- Custom CSS variables instead of Tailwind classes
- No metadata attributes (`data-component`, etc.)
- Hardcoded colors instead of semantic tokens

**Solution:**
Ensure Nexus follows Workflow 2 in SYSTEM_PROMPT.md:
1. Load design system mappings before generating
2. Use Tailwind classes from TOKEN_REFERENCE.md
3. Follow component patterns from COMPONENT_PATTERNS.md
4. Add required metadata attributes

---

### Issue: Low Figma mapping accuracy

**Symptoms:**
- Less than 70% component replacement
- Manual work exceeds 30%

**Solution:**
Check metadata attributes in generated HTML:
```html
<!-- Required attributes -->
data-component="Button"      <!-- Component name -->
data-variant="primary"       <!-- Variant -->
data-size="default"          <!-- Size -->
data-figma-node="9:1071"     <!-- Figma node ID -->
```

Without these attributes, mapping accuracy drops from 90-95% to 60-70%.

---

### Issue: Accessibility validation fails

**Common Issues:**
- Missing ARIA labels on interactive elements
- Low color contrast ratios
- Non-semantic HTML (divs instead of buttons)
- Missing form labels

**Solution:**
Follow accessibility guidelines in SYSTEM_PROMPT.md Workflow 4:
- Use semantic HTML (`<button>`, `<input>`, `<label>`)
- Add ARIA attributes (`aria-label`, `aria-describedby`)
- Ensure 4.5:1 contrast for text, 3:1 for UI components
- Link labels to inputs

---

## Version History

### 3.0.0 (2026-04-10) - Pure Claude Code Refactoring
- ✅ Removed Python execution dependencies
- ✅ Converted logic to prompt-based workflows in SYSTEM_PROMPT.md
- ✅ Created COMPONENT_PATTERNS.md (53 component patterns)
- ✅ Created TOKEN_REFERENCE.md (169 token mappings)
- ✅ Updated documentation to reflect pure Claude Code architecture
- ✅ Deleted deprecated figma_ui_generation.py
- ✅ Marked remaining Python files as reference only

### 2.0.0 (2026-04-09) - Architecture Transition
- Partial migration to Claude Code agent
- Added SYSTEM_PROMPT.md
- Deprecated figma_ui_generation.py

### 1.3.0 (2026-04-08) - Metadata Enhancement
- Added data-* attributes for 90-95% Figma mapping accuracy
- Enhanced web prototype generation

### 1.2.0 (2026-04-08) - Design System Integration
- Integrated SprouX design system mappings
- 100% consistency with design tokens

---

## Support

**Documentation:**
- `SYSTEM_PROMPT.md` - Complete workflow guide
- `COMPONENT_PATTERNS.md` - Component HTML patterns
- `TOKEN_REFERENCE.md` - Design token reference
- `AGENT.md` - Agent capabilities

**Design System:**
- `SprouX_UI-UX team/design ops/figma-mappings/` - Component & token mappings
- `SprouX_UI-UX team/design-system-component-usage-guidelines.md` - Usage guidelines

---

## License

Part of SprouX project - Internal use only
