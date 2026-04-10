# Nexus - UI Engineering Agent Setup Guide

**Version:** 3.0.0
**Type:** Pure Claude Code Agent
**Last Updated:** 2026-04-10

---

## Overview

Nexus is a Claude Code subagent that requires **no installation** - it's ready to use once the files are in your project. This guide explains how to set up and use Nexus with your team.

---

## Prerequisites

### Required

1. **Claude Code** - The official CLI tool for Claude
   - Download: [claude.ai/code](https://claude.ai/code)
   - Requires: Claude Pro or API access

2. **SprouX Project Repository** - Team members need access to the SprouX repository
   - The agent files must be in: `.claude/agents/ui-engineering/`

3. **MCP Tools** (Pre-configured in Claude Code)
   - Figma MCP integration (for Figma UI generation)
   - Standard Claude Code tools (Read, Write, Bash, etc.)

### Optional

- **Figma account** - Only needed if generating Figma UI (Workflow 3)
- **Design system access** - Read access to `SprouX_UI-UX team/design ops/figma-mappings/`

---

## Setup Instructions

### Step 1: Clone the SprouX Repository

```bash
# Clone the repository (if not already done)
git clone <repository-url> SprouX
cd SprouX

# Verify agent files exist
ls -la .claude/agents/ui-engineering/
```

**Expected files:**
```
.claude/agents/ui-engineering/
├── AGENT.md
├── README.md
├── SYSTEM_PROMPT.md
├── COMPONENT_PATTERNS.md
├── TOKEN_REFERENCE.md
├── LESSONS_LEARNED.md
├── SETUP.md (this file)
├── skills/
├── tools/
└── templates/
```

### Step 2: Verify Claude Code Installation

```bash
# Check Claude Code is installed
claude --version

# If not installed, download from claude.ai/code
```

### Step 3: Navigate to Project Directory

```bash
# Claude Code works from your project directory
cd /path/to/SprouX
```

### Step 4: Start Using the Agent

**That's it!** No installation required. The agent is ready to use.

---

## How to Use Nexus

### Method 1: Via Task Tool (Recommended)

When working in Claude Code, invoke Nexus using the Task tool:

**Example conversation:**
```
User: "I need to generate a dashboard prototype from these requirements..."

Claude Code (Main): [Uses Task tool with subagent_type="ui-engineering"]
  ↓
Nexus Subagent: [Reads SYSTEM_PROMPT.md, executes workflows]
  ↓
Returns: Prototype files, Figma URL, reports
```

**You don't need to do anything special** - Claude Code automatically finds and launches the agent.

### Method 2: Direct Invocation (If Supported)

```bash
# If your Claude Code setup supports direct agent invocation
claude agent ui-engineering "Generate a login page prototype"
```

---

## Verification Steps

### Verify Agent is Accessible

**Test 1: Check Files**
```bash
# Verify all required files exist
ls .claude/agents/ui-engineering/SYSTEM_PROMPT.md
ls .claude/agents/ui-engineering/COMPONENT_PATTERNS.md
ls .claude/agents/ui-engineering/TOKEN_REFERENCE.md
```

**Test 2: Check Design System**
```bash
# Verify design system mappings exist
ls "SprouX_UI-UX team/design ops/figma-mappings/components.json"
ls "SprouX_UI-UX team/design ops/figma-mappings/foundations.json"
```

**Test 3: Simple Generation Test**

Ask Claude Code to generate a simple component:
```
"Generate an HTML button using the SprouX design system"
```

**Expected output:**
```html
<button
  class="inline-flex items-center justify-center h-size-md px-md gap-xs rounded-lg bg-primary text-primary-foreground typo-paragraph-small-semibold"
  data-component="Button"
  data-variant="primary"
  data-size="default"
  data-figma-node="9:1071">
  Click Me
</button>
```

If you see Tailwind classes, metadata attributes, and design system integration → **Setup successful!**

---

## Team Collaboration

### Git Workflow

**Agent files are version-controlled:**

```bash
# Pull latest agent updates
git pull origin main

# Agent updates automatically available
# No reinstallation needed
```

**Shared improvements:**
- Team member updates COMPONENT_PATTERNS.md → Everyone benefits
- New workflows added to SYSTEM_PROMPT.md → Available to all
- Token mappings updated → Automatically reflected

### Best Practices

1. **Keep agent files in sync:**
   ```bash
   git pull origin main  # Before starting work
   ```

2. **Don't modify agent files directly** (unless you're the maintainer)
   - Agent files are shared infrastructure
   - Changes affect entire team
   - Coordinate updates via pull requests

3. **Report issues:**
   - If agent generates incorrect output, report in team channel
   - Include: input requirements, actual output, expected output

---

## Configuration (Optional)

### Figma MCP Configuration

**If your team uses Figma UI generation (Workflow 3):**

1. **Check Figma MCP is enabled:**
   ```bash
   # Verify in Claude Code settings
   cat ~/.claude/settings.json | grep figma
   ```

2. **Ensure Figma library access:**
   - Library: `[SprouX - DS] Foundation & Component`
   - File ID: `ihKZCnJS2UrsQzpzEFYI4u`
   - Team members need view access

3. **Test Figma integration:**
   ```
   Ask Claude: "Capture this HTML to Figma"
   ```

---

## Common Scenarios

### Scenario 1: New Team Member Onboarding

**Steps:**
1. Clone SprouX repository
2. Install Claude Code
3. Navigate to SprouX directory
4. Start using - no additional setup!

**First task:** Generate a simple card component to verify setup

---

### Scenario 2: Working Remotely

**No special setup needed:**
- Agent files are in the repository
- Claude Code is local on your machine
- Works offline (except Figma generation)

---

### Scenario 3: Multiple Projects

**If working on multiple projects:**
```bash
# Each project can have its own agent version
cd project-a
ls .claude/agents/ui-engineering/  # Uses Project A's agent

cd project-b
ls .claude/agents/ui-engineering/  # Uses Project B's agent
```

Claude Code uses the agent from your **current working directory**.

---

## Troubleshooting

### Issue: "Agent not found"

**Cause:** Not in SprouX project directory

**Solution:**
```bash
# Navigate to SprouX root
cd /path/to/SprouX

# Verify you're in the right place
ls .claude/agents/ui-engineering/
```

---

### Issue: "Design system not found"

**Cause:** Missing design system mappings

**Solution:**
```bash
# Check files exist
ls "SprouX_UI-UX team/design ops/figma-mappings/"

# Should see:
# - components.json
# - foundations.json
# - README.md
```

If missing, pull latest from git:
```bash
git pull origin main
```

---

### Issue: Agent generates custom CSS instead of Tailwind

**Cause:** Agent not following SYSTEM_PROMPT.md properly

**Solution:**
1. Check SYSTEM_PROMPT.md exists and is up-to-date
2. Verify COMPONENT_PATTERNS.md exists
3. Explicitly mention "use SprouX design system" in request

---

### Issue: Figma generation fails

**Possible causes:**
1. **Figma MCP not configured** - Check Claude Code settings
2. **No Figma library access** - Request access from design team
3. **Network issues** - Figma requires internet connection

**Solution:**
```bash
# Check Figma MCP status
claude config list | grep figma

# If not configured, contact team lead
```

---

## Getting Help

### Documentation

1. **README.md** - User guide and overview
2. **SYSTEM_PROMPT.md** - Complete workflow documentation
3. **COMPONENT_PATTERNS.md** - Component HTML patterns
4. **TOKEN_REFERENCE.md** - Design token reference
5. **AGENT.md** - Agent capabilities and metadata

### Support Channels

- **Team Slack:** #design-system channel
- **GitHub Issues:** Report bugs and request features
- **Documentation:** Check README.md first

### Quick Reference

**Generate prototype:**
```
"Generate a dashboard with stats cards and charts"
```

**Figma from prototype:**
```
"Convert this HTML to Figma: /path/to/prototype.html"
```

**Check accessibility:**
```
"Validate accessibility of /path/to/prototype.html"
```

---

## Version Updates

### When Agent Updates

**Automatic via Git:**
```bash
git pull origin main
# Agent automatically uses latest version
# No reinstall needed
```

**Check version:**
```bash
# View AGENT.md for current version
grep "Version:" .claude/agents/ui-engineering/AGENT.md
```

**Breaking changes:**
- Announced in team channels
- Migration guide provided if needed
- Usually backward-compatible

---

## Summary

### For Team Members

✅ **Setup is simple:**
1. Clone SprouX repo
2. Install Claude Code
3. Start using (no installation)

✅ **No configuration needed** (unless using Figma generation)

✅ **Updates are automatic** (via git pull)

✅ **Works offline** (except Figma features)

### For Team Leads

✅ **Zero installation overhead** - Pure Claude Code

✅ **Version controlled** - Agent updates via git

✅ **Team-wide consistency** - Everyone uses same patterns

✅ **Easy onboarding** - New members productive immediately

---

## Next Steps

1. ✅ Clone repository (if not done)
2. ✅ Install Claude Code
3. ✅ Test with simple component generation
4. ✅ Try full prototype workflow
5. ✅ Explore COMPONENT_PATTERNS.md and TOKEN_REFERENCE.md

**Ready to start!** Open Claude Code in your SprouX directory and ask it to generate a component.

---

**Questions?** Check README.md or ask in #design-system channel.
