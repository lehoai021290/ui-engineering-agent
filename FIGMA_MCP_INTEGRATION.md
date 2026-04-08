# Figma MCP Integration Guide

This guide explains how to complete the Figma MCP tool integration for full automation.

## Current Status

✅ **Workflow Implemented**: Complete 5-step Figma UI generation workflow
⚠️ **MCP Tools Placeholder**: The actual Figma MCP tool calls are placeholders and need to be connected

## What Needs to Be Done

### Step 1: Load Figma MCP Tools in Agent

The agent needs to load Figma MCP tools. Update `agent.py`:

```python
# In agent.py, add to _setup_tools method

def _setup_tools(self) -> List[Tool]:
    """Setup tools for the agent"""
    tools = []

    # ... existing tools ...

    # Load Figma MCP tools
    figma_tools = self._load_figma_mcp_tools()
    tools.extend(figma_tools)

    return tools

def _load_figma_mcp_tools(self) -> List[Tool]:
    """Load Figma MCP tools for UI generation"""
    from langchain.tools import ToolSearch

    # Load Figma MCP tools
    tools = []

    # Tool 1: Generate Figma Design
    tools.append(Tool(
        name="figma_generate_design",
        func=self._call_mcp_figma_generate,
        description="""Generate Figma design from web prototype URL.
                      Captures HTML/CSS/JS and creates Figma file."""
    ))

    # Tool 2: Use Figma (run scripts)
    tools.append(Tool(
        name="figma_use_figma",
        func=self._call_mcp_figma_use,
        description="""Run JavaScript code in Figma file context.
                      Used for component mapping and token application."""
    ))

    return tools

def _call_mcp_figma_generate(self, params: dict) -> dict:
    """Call mcp__figma__generate_figma_design"""
    # TODO: Implement actual MCP call
    # This requires loading the Figma MCP server
    pass

def _call_mcp_figma_use(self, params: dict) -> dict:
    """Call mcp__figma__use_figma"""
    # TODO: Implement actual MCP call
    pass
```

### Step 2: Connect MCP Tools to Wrapper

Update `skills/figma_ui_generation.py` placeholder functions:

#### 2.1: _capture_to_figma

Replace the placeholder in `_capture_to_figma`:

```python
def _capture_to_figma(prototype_url: str, output_mode: str, feature_name: str) -> Dict:
    """Capture web prototype to Figma using Figma MCP"""

    # Get team key first
    whoami_result = mcp__figma__whoami()
    team_key = whoami_result['teams'][0]['key']  # Use first available team

    # Call Figma MCP tool
    result = mcp__figma__generate_figma_design({
        "url": prototype_url,
        "outputMode": output_mode,
        "fileName": f"SprouX - {feature_name}",
        "planKey": team_key
    })

    return {
        "status": "success",
        "file_key": result['fileKey'],
        "file_url": result['fileUrl'],
        "message": "Prototype captured to Figma"
    }
```

#### 2.2: _replace_components

Replace the placeholder in `_replace_components`:

```python
def _replace_components(file_key: str, components_mapping: Dict) -> Dict:
    """Replace generic layers with design system components"""

    # Generate component mapping script
    script = _generate_component_mapping_script(components_mapping)

    # Call Figma MCP tool to run the script
    result = mcp__figma__use_figma({
        "fileKey": file_key,
        "code": script
    })

    return {
        "status": "success",
        "components_mapped": result.get('componentsMapped', 0),
        "components_created": result.get('componentsCreated', 0),
        "node_ids": result.get('nodeIds', []),
        "message": "Components replaced successfully"
    }

def _generate_component_mapping_script(components_mapping: Dict) -> str:
    """Generate JavaScript code for component mapping"""
    # This generates the actual Figma plugin code
    # See original SKILL.md for the script template
    script = """
    // Component mapping script
    const components = """ + json.dumps(components_mapping) + """;

    // Find and replace logic here
    // (See SKILL.md Step 3 for complete script)
    """
    return script
```

#### 2.3: _apply_foundation_tokens

Replace the placeholder in `_apply_foundation_tokens`:

```python
def _apply_foundation_tokens(file_key: str, foundations_mapping: Dict) -> Dict:
    """Apply design tokens to Figma layers"""

    # Generate token application script
    script = _generate_token_application_script(foundations_mapping)

    # Call Figma MCP tool
    result = mcp__figma__use_figma({
        "fileKey": file_key,
        "code": script
    })

    return {
        "status": "success",
        "colors_linked": result.get('colorsLinked', 0),
        "spacing_linked": result.get('spacingLinked', 0),
        "typography_linked": result.get('typographyLinked', 0),
        "tokens_applied": result.get('tokensApplied', 0),
        "message": "Foundation tokens applied"
    }

def _generate_token_application_script(foundations_mapping: Dict) -> str:
    """Generate JavaScript code for token application"""
    # This generates the actual Figma plugin code
    # See original SKILL.md for the script template
    script = """
    // Token application script
    const tokens = """ + json.dumps(foundations_mapping) + """;

    // Apply tokens logic here
    // (See SKILL.md Step 4 for complete script)
    """
    return script
```

### Step 3: Access MCP Tools in Wrapper

The wrapper needs access to the MCP tool functions. Two approaches:

#### Approach A: Pass MCP Tools to Wrapper

```python
# In agent.py, modify _generate_figma_tool

def _generate_figma_tool(self, html_path: str) -> str:
    """Tool wrapper for Figma UI generation"""
    from skills.figma_ui_generation import generate_figma_from_file

    # Pass MCP tools to the wrapper
    result = generate_figma_from_file(
        html_path,
        mcp_figma_generate=self.mcp_figma_generate,  # Pass MCP tool
        mcp_figma_use=self.mcp_figma_use              # Pass MCP tool
    )

    # ... rest of tool wrapper
```

```python
# In skills/figma_ui_generation.py

def generate_figma_design(
    html_code: str,
    # ... other params ...
    mcp_figma_generate=None,  # MCP tool passed from agent
    mcp_figma_use=None         # MCP tool passed from agent
) -> Dict:
    # Use these in _capture_to_figma, _replace_components, etc.
    pass
```

#### Approach B: Global MCP Tool Access

```python
# Create mcp_tools.py

class FigmaMCPTools:
    """Singleton for Figma MCP tool access"""
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.generate_design = None
        self.use_figma = None

    def initialize(self, generate_fn, use_fn):
        self.generate_design = generate_fn
        self.use_figma = use_fn

# In agent.py
from mcp_tools import FigmaMCPTools

def _setup_llm(self):
    # ... after loading MCP tools ...
    FigmaMCPTools.get_instance().initialize(
        self.mcp_figma_generate,
        self.mcp_figma_use
    )

# In skills/figma_ui_generation.py
from mcp_tools import FigmaMCPTools

def _capture_to_figma(...):
    mcp = FigmaMCPTools.get_instance()
    result = mcp.generate_design({...})
```

### Step 4: Complete Mapping Scripts

Port the complete JavaScript mapping scripts from your SKILL.md:

1. **Component Mapping Script** (from SKILL.md Step 3)
2. **Token Application Script** (from SKILL.md Step 4)

These scripts need to be generated dynamically based on the mapping JSON files.

## Testing

### Test Without Full Integration (Current State)

```bash
cd .claude/agents/ui-engineering

# Test with placeholder functions
python3 -c "
from skills.figma_ui_generation import generate_figma_design
result = generate_figma_design('<html>...</html>')
print(result)
"
```

This will run the workflow with placeholder results.

### Test With Full Integration (After Completion)

```bash
# 1. Ensure prototype is running
cd SprouX_design\ system
pnpm dev  # Runs on localhost:5173

# 2. Run agent with Figma generation
cd ../. claude/agents/ui-engineering
python cli.py generate "Build a login page" --with-figma

# 3. Check Figma file was created
# The agent should output the Figma URL
```

## Required Files

### Mapping Configuration Files

Ensure these exist:
- ✅ `SprouX_UI-UX team/design ops/figma-mappings/components.json`
- ✅ `SprouX_UI-UX team/design ops/figma-mappings/foundations.json`

### Figma Library

- File Key: `ihKZCnJS2UrsQzpzEFYI4u`
- Library: [SprouX - DS] Foundation & Component

## Next Steps

1. **Load Figma MCP tools** in agent.py
2. **Connect MCP tools** to wrapper functions
3. **Implement mapping scripts** for component replacement and token application
4. **Test end-to-end** workflow
5. **Document** any issues or improvements
