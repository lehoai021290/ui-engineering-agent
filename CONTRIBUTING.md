# Contributing to UI Engineering Agent

## Setup for Team Members

### Prerequisites
- Python 3.9 or higher
- Figma MCP server configured in Claude Code
- Access to SprouX design system files

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ui-engineering
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify installation**
   ```bash
   python cli.py --help
   ```

### Environment Setup

Create a `.env` file in the root directory:
```
ANTHROPIC_API_KEY=your_api_key_here
FIGMA_ACCESS_TOKEN=your_figma_token_here
```

### Usage

Run the agent via command line:
```bash
./cli.py design-to-figma <design-spec-file>
```

Or use it within Claude Code as an agent.

### Project Structure

```
ui-engineering/
├── agent.py                    # Main CrewAI agent definition
├── orchestrator.py             # Workflow orchestration
├── cli.py                      # Command-line interface
├── bmad_integration.py         # BMAD framework integration
├── skills/                     # Specialized skills
│   ├── figma_ui_generation.py
│   └── web_prototype_generation.py
├── tools/                      # Agent tools
│   ├── design_spec_parser.py
│   ├── handoff_generator.py
│   └── accessibility_checker.py
├── workflows/                  # Workflow implementations
│   └── adaptive.py
└── templates/                  # Output templates
```

### Making Changes

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes
3. Test thoroughly
4. Submit a pull request

### Testing

Run the agent on sample design specs:
```bash
python cli.py design-to-figma examples/sample-design.md
```

### Questions?

Contact the SprouX team or open an issue.
