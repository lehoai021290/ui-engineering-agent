# Nexus UI Engineering Agent - Team Installation Guide

This guide helps your team members install and use the Nexus UI engineering agent in their Claude Code environment.

## What is Nexus?

Nexus is a specialized UI engineering agent that generates web prototypes and Figma designs from requirements:
- Generates functional web prototypes (HTML/CSS/JS) from requirements, wireframes, or direct prompts
- Creates Figma UI visualizations FROM code (not the other way around)
- Makes autonomous design decisions when specs are incomplete
- Validates accessibility (WCAG 2.1 AA) and performance (Lighthouse > 90)
- Supports multiple input scenarios: full handoff, partial specs, requirements only, or direct prompts

## Prerequisites

- Claude Code CLI installed and configured
- Git installed
- Access to the team's GitHub repository: `lehoai021290/ui-engineering-agent`

## Installation Steps

### Step 1: Clone the Agent Repository

```bash
# Clone the Nexus agent code
cd ~/.claude/agents/
git clone https://github.com/lehoai021290/ui-engineering-agent.git ui-engineering

# Alternatively, if you prefer project-specific installation:
cd /path/to/your/project/.claude/agents/
git clone https://github.com/lehoai021290/ui-engineering-agent.git ui-engineering
```

### Step 2: Install Dependencies (Optional)

The agent can run without external dependencies for basic functionality. However, for full features:

```bash
cd ~/.claude/agents/ui-engineering
pip3 install -r requirements.txt
```

**Note:** If you encounter dependency conflicts, you can skip this step. The agent's core functionality works through Claude Code's built-in tools.

### Step 3: Install the Nexus Skill

Create the nexus skill in your Claude Code skills directory:

```bash
# Create the skill directory
mkdir -p ~/.claude/skills/nexus

# Download the SKILL.md file (ask your team lead for the file, or copy from below)
```

**SKILL.md content:**

```markdown
---
name: nexus
description: Invoke Nexus, the specialized UI engineering agent that converts designs to code, generates prototypes from URLs, and automates design-to-code workflows. Use this skill whenever the user mentions Nexus, UI engineering, design-to-code conversion, Figma-to-code, prototype generation, web prototypes, or wants to build UI components from designs. Also trigger when the user shares Figma URLs with the intent to generate code, asks to convert websites to prototypes, or needs automated design implementation. This skill should be used proactively for any design-to-code task, even if the user doesn't explicitly say "use Nexus".
---

# Nexus - UI Engineering Agent

Nexus is your specialized UI engineering agent that bridges the gap between design vision and working code.

## When to Use This Skill

Use Nexus whenever you want to:

- **Convert Figma designs to code** - Extract design context and generate production-ready React components
- **Generate prototypes from URLs** - Capture existing web pages and convert them to editable code
- **Build UI components from designs** - Automated design-to-code workflows with proper component structure
- **Implement design systems** - Convert design system components into coded implementations
- **Automate design workflows** - Watch for Figma changes and automatically generate updated code

**Trigger contexts:**
- You mention "Nexus" explicitly
- You share Figma URLs and want code generation
- You ask to "convert this design to code"
- You want to "build" or "implement" a UI from a design
- You request "prototype generation" from a website URL
- You ask for "design-to-code" or "Figma-to-code" workflows
- You want to extract design tokens or component specs from Figma

## How to Use Nexus

Simply mention what you need in Claude Code:

**Examples:**
- "Nexus, convert this Figma design to React: [Figma URL]"
- "Can you generate a prototype from this page: [Website URL]"
- "Build the refund confirmation dialog from our design system"
- "Extract design tokens from this Figma file"

Claude Code will automatically invoke the Nexus agent when appropriate.

## What Nexus Produces

**Typical outputs:**
- **Web prototype files** - Functional HTML/CSS/JS files
- **Figma UI files** - Generated Figma designs with proper node structure
- **Implementation review reports** - Technical feasibility assessments
- **Accessibility audit results** - WCAG compliance validation
- **Design decision logs** - Documentation of autonomous choices made
- **Performance analysis** - Lighthouse scores and optimization recommendations

## Important Notes

- Nexus GENERATES web prototypes from requirements (HTML/CSS/JS, not React by default)
- Nexus CREATES Figma designs from code, it doesn't read Figma files
- Can work with minimal input - makes autonomous design decisions when needed
- Follows WCAG 2.1 AA accessibility standards and targets Lighthouse score > 90
- Generated prototypes should be reviewed before production deployment
- Integrates with BMAD UX Designer agent for collaborative workflows
```

Save this content to: `~/.claude/skills/nexus/SKILL.md`

### Step 4: Restart Claude Code

```bash
# Restart your Claude Code session to load the new skill
# The skill should now appear in your available skills list
```

### Step 5: Verify Installation

Test that Nexus is properly installed:

```bash
# Start a Claude Code session
claude

# In the chat, type:
/nexus

# Or simply describe a requirement-to-prototype task:
"Build a user registration form with email validation"
```

If the installation is successful, you should see Nexus mentioned in the available skills list.

## Using Nexus

### Method 1: Explicit Invocation

```
/nexus

# Or

Nexus, [your request here]
```

### Method 2: Natural Language

Just describe what you need:
- "Build a user registration form with email and password validation"
- "Create a pricing table prototype with three tiers and monthly/annual toggle"
- "Generate a dashboard layout from this wireframe: [file path]"
- "Build a login page with accessibility features"

Claude Code will automatically invoke Nexus when it detects a requirement-to-prototype task.

### Method 3: Terminal Command (Alternative)

If you installed dependencies and want direct CLI access:

```bash
# Add to your ~/.zshrc or ~/.bashrc:
alias nexus="python3 ~/.claude/agents/ui-engineering/cli.py"

# Then reload:
source ~/.zshrc

# Use in terminal:
nexus info
nexus generate --url https://example.com
nexus watch
```

## Troubleshooting

### Skill Not Appearing

**Solution:**
1. Verify SKILL.md exists at: `~/.claude/skills/nexus/SKILL.md`
2. Check the YAML frontmatter is properly formatted
3. Restart Claude Code
4. Run: `ls ~/.claude/skills/` to confirm directory exists

### Agent Not Found

**Solution:**
1. Verify agent directory exists at: `~/.claude/agents/ui-engineering/`
2. Check AGENT.md file exists in the directory
3. Ensure Git clone was successful
4. Try cloning again: `git clone https://github.com/lehoai021290/ui-engineering-agent.git ~/.claude/agents/ui-engineering`

### Dependency Errors

**Solution:**
1. Dependencies are optional for basic functionality
2. If needed, install in a virtual environment:
   ```bash
   cd ~/.claude/agents/ui-engineering
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Or skip dependencies - Claude Code tools provide core functionality

## Keeping Nexus Updated

```bash
# Update to the latest version
cd ~/.claude/agents/ui-engineering
git pull origin main

# Check for skill updates from your team lead
```

## Support

**Questions or issues?**
- Contact your team lead
- Check the GitHub repository: https://github.com/lehoai021290/ui-engineering-agent
- Report issues in your team's communication channel

## Team Resources

- **GitHub Repository:** https://github.com/lehoai021290/ui-engineering-agent
- **Agent Path:** `~/.claude/agents/ui-engineering/`
- **Skill Path:** `~/.claude/skills/nexus/`

---

**Installation complete!** You're ready to use Nexus for design-to-code automation. 🎉
