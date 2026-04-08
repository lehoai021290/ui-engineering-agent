# UI Engineering Agent

Intelligent agent for design-to-code workflows with **zero dependency conflicts**. Transforms design specifications, requirements, or prompts into web prototypes and Figma UI.

> **Note:** Refactored to remove CrewAI dependency. See `REFACTORING_NOTES.md` for details.

## Features

- ✅ **Flexible Input Handling** - Works with wireframes, design specs, requirements, or simple prompts
- ✅ **Adaptive Workflows** - Automatically selects workflow based on input completeness
- ✅ **Multi-Agent Collaboration** - Integrates with BMAD UX Designer agent
- ✅ **Autonomous Design Decisions** - Makes informed decisions when specifications are incomplete
- ✅ **Web Prototype Generation** - Creates functional HTML/CSS/JS prototypes
- ✅ **Figma Integration** - Generates Figma UI with design system mapping
- ✅ **Accessibility Validation** - WCAG 2.1 AA compliance checking
- ✅ **Comprehensive Documentation** - Detailed implementation reviews with autonomous decisions logged

## Architecture

**Simplified, lightweight design with direct skill calls:**

```
CLI (click)
  ↓
Orchestrator (Python)
  ↓
Skills (standalone modules)
  ├── Design Spec Parser
  ├── Web Prototype Generation
  ├── Figma UI Generation (→ Figma MCP)
  └── Accessibility Checker
  ↓
BMAD Integration (optional)
  ├── Handoff Detection
  ├── Artifact Exchange
  └── Collaboration Protocol
```

**Input Modes:**
- Full Handoff (Wireframes + Specs)
- Partial Handoff (Specs Only)
- Requirements Only
- Direct Prompts

## Installation

### Prerequisites

- Python 3.9+
- Anthropic API key (for Claude)
- Git

### Setup

```bash
# Navigate to agent directory
cd .claude/agents/ui-engineering

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
export ANTHROPIC_API_KEY="your-api-key"
```

### Requirements

Create `requirements.txt`:

```txt
crewai==0.28.0
crewai-tools==0.2.0
langchain==0.1.0
langchain-anthropic==0.1.0
anthropic==0.18.0
pyyaml==6.0
click==8.1.0
```

## Usage

### Command Line Interface

The agent provides a comprehensive CLI for various operations:

```bash
# Make CLI executable
chmod +x cli.py

# Show help
python cli.py --help
```

### Common Commands

#### 1. Watch for BMAD Handoffs (Automatic Mode)

```bash
python cli.py watch

# With custom interval
python cli.py watch --interval 60
```

Monitors `_bmad-output/` for completed designs from UX Designer agent and automatically generates prototypes.

#### 2. Manual Implementation

```bash
python cli.py implement _bmad-output/ux-design/login-flow.md
```

Generates prototype and Figma UI from a specific design specification file.

#### 3. Quick Generation (Prompt-Based)

```bash
python cli.py generate "Build a login page with email and password"

python cli.py generate "Create a product dashboard with metrics and charts"
```

Generates complete prototype from a simple text description. Makes autonomous design decisions.

#### 4. HTML to Figma Conversion

```bash
python cli.py to-figma prototypes/dashboard.html
```

Converts an existing HTML prototype to Figma UI.

#### 5. Check Workflow Status

```bash
python cli.py status
```

Shows current BMAD workflow status and any pending handoffs.

#### 6. Request Clarification

```bash
python cli.py clarify \
  -q "Should we use modal or inline form?" \
  -q "What's the error state design?" \
  -c "Working on login flow"
```

Sends questions to UX Designer agent.

### Development Commands

```bash
# Parse and analyze design spec
python cli.py dev parse design-spec.md

# Run accessibility audit
python cli.py dev audit prototype.html

# Show agent info
python cli.py info
```

## Workflows

### Workflow 1: Full Handoff (Complete Design Specs)

**Input**: Wireframes + Design Specifications + User Flows

**Process**:
1. Parse design specifications
2. Generate web prototype following wireframes
3. Generate Figma UI
4. Validate accessibility
5. Generate implementation review

**Use Case**: When UX Designer provides complete design package

### Workflow 2: Partial Handoff (Specs Without Wireframes)

**Input**: Design Specifications + Component Requirements (no wireframes)

**Process**:
1. Parse requirements and components
2. Make autonomous layout decisions
3. Generate web prototype with inferred structure
4. Generate Figma UI
5. Validate accessibility
6. Document autonomous decisions in review

**Use Case**: When UX Designer provides specs but no visual wireframes

### Workflow 3: Autonomous Generation (Requirements Only)

**Input**: User Requirements or User Stories

**Process**:
1. Parse requirements
2. Infer all UI components
3. Make complete autonomous design decisions
4. Generate web prototype
5. Generate Figma UI
6. Validate accessibility
7. Comprehensive documentation of ALL decisions

**Use Case**: No UX Designer involved, or rapid prototyping from requirements

### Workflow 4: Quick Prompt (Minimal Input)

**Input**: Simple text prompt

**Process**:
1. Interpret prompt
2. Generate complete design autonomously
3. Create prototype and Figma UI
4. Document decisions

**Use Case**: Rapid exploration, proof-of-concept, user testing

## Input Formats

### Markdown Design Spec

```markdown
## User Flow
- User navigates to login page
- User enters email and password
- User clicks submit
- System validates and redirects

## Component Requirements
- Use Input (variant: default) for email field
- Use Input (variant: password) for password field
- Use Button (variant: primary) for submit
- Use Link for "Forgot password"

## Interactions
- Form validation on blur
- Error messages for invalid input
- Loading state on submit

## Accessibility
- WCAG 2.1 AA compliance
- Keyboard navigation support
- Screen reader announcements
```

### Requirements Text

```
User Story: As a user, I want to log in with email and password

Acceptance Criteria:
- Email input with validation
- Password input (masked)
- Remember me checkbox
- Forgot password link
- Submit button
- Error handling
```

### Direct Prompt

```
"Build a product dashboard with sales metrics, charts, and recent activity"
```

## Integration with BMAD

### Setup

1. Ensure BMAD UX Designer agent is configured
2. Verify `_bmad-output/` directory structure exists
3. Run UI Engineering Agent in watch mode

### Workflow Status File

Location: `_bmad-output/workflow-status.yaml`

```yaml
design_phase:
  status: completed
  owner: ux-designer
  output: _bmad-output/ux-design/onboarding-flow.md
  completed_at: "2026-04-07T10:30:00"

implementation_phase:
  status: in_progress
  owner: ui-engineering-agent
  started_at: "2026-04-07T10:35:00"
  artifacts:
    prototype: _bmad-output/ui-engineering/prototypes/...
    figma: https://figma.com/file/...
    review_report: _bmad-output/ui-engineering/reports/review-*.md
```

### Handoff Protocol

1. **UX Designer** completes design → Sets `design_phase.status = completed`
2. **UI Engineering Agent** detects handoff → Sets `implementation_phase.status = in_progress`
3. **Agent** generates artifacts → Updates `implementation_phase.artifacts`
4. **Agent** completes work → Sets `implementation_phase.status = awaiting_review`
5. **UX Designer** reviews → Provides feedback or approves

## Output Artifacts

### Generated Files

```
_bmad-output/ui-engineering/
├── prototypes/
│   └── 20260407-103500/
│       ├── index.html
│       ├── styles.css
│       └── script.js
├── figma/
│   └── component-exports/
├── reports/
│   └── review-20260407-103500.md
└── logs/
```

### Implementation Review Report

Includes:
- Input summary and completeness level
- Autonomous design decisions (if any)
- Deliverables (prototype + Figma links)
- Technical notes and constraints
- Accessibility audit results
- Questions for UX review
- Recommendations

## Configuration

Edit `config.yaml` to customize:

```yaml
agent:
  model: "claude-sonnet-4.5"  # claude-opus-4.6, claude-haiku-4.5

  quality_standards:
    accessibility:
      wcag_level: "AA"
    performance:
      lighthouse_threshold: 90

  decision_making:
    autonomous_scope:
      - component_selection
      - layout_structure
      - spacing_and_sizing
    consult_ux_designer_for:
      - strategic_user_flows
      - brand_visual_design
```

## Development

### Project Structure

```
.claude/agents/ui-engineering/
├── AGENT.md                    # Agent documentation
├── README.md                   # This file
├── config.yaml                 # Configuration
├── agent.py                    # Core agent (CrewAI)
├── orchestrator.py             # Workflow orchestration
├── bmad_integration.py         # BMAD communication
├── cli.py                      # Command-line interface
├── skills/
│   ├── figma_ui_generation.py
│   └── web_prototype_generation.py
├── tools/
│   ├── design_spec_parser.py
│   ├── handoff_generator.py
│   └── accessibility_checker.py
├── workflows/
│   └── adaptive.py
├── templates/
│   └── implementation_review.md
└── tests/
    ├── test_agent.py
    └── test_integration.py
```

### Running Tests

```bash
pytest tests/
```

### Adding New Skills

1. Create skill file in `skills/`
2. Implement skill function
3. Add to `config.yaml`
4. Update agent tools in `agent.py`

## Examples

### Example 1: Full Design Handoff

```bash
# UX Designer creates: _bmad-output/ux-design/checkout-flow.md

# Start watch mode
python cli.py watch

# Agent automatically:
# 1. Detects handoff
# 2. Parses wireframes and specs
# 3. Generates prototype
# 4. Generates Figma UI
# 5. Sends review to UX Designer
```

### Example 2: Requirements-Only Implementation

```bash
python cli.py implement requirements.txt

# Agent autonomously:
# 1. Infers UI components
# 2. Designs layout
# 3. Generates prototype
# 4. Generates Figma UI
# 5. Documents all decisions
```

### Example 3: Quick Exploration

```bash
python cli.py generate "Build a settings page with theme toggle and notification preferences"

# Agent creates:
# - Complete prototype in minutes
# - Figma UI
# - Accessibility validated
```

## Troubleshooting

### Issue: Agent not detecting handoffs

**Solution**: Check `_bmad-output/workflow-status.yaml` exists and `design_phase.status = completed`

### Issue: Prototype generation fails

**Solution**: Verify design spec is well-formatted. Use `python cli.py dev parse <file>` to debug.

### Issue: Figma integration errors

**Solution**: Check Figma API credentials and permissions. Verify `figma-ui-generation` skill is properly configured.

## Roadmap

- [ ] Enhanced web prototype generation with LLM
- [ ] Real Figma API integration
- [ ] Interactive prototype previews
- [ ] Design system sync
- [ ] Multi-page prototype support
- [ ] Version control for prototypes
- [ ] Collaboration comments

## Version

**Current Version**: 1.0.0
**Last Updated**: 2026-04-07

## Support

For issues and questions:
- Check the [AGENT.md](./AGENT.md) documentation
- Review workflow logs in `_bmad-output/ui-engineering/logs/`
- Inspect implementation review reports

## License

Part of SprouX project - Internal use only
