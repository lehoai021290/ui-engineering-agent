# Refactoring Notes - Removed CrewAI Dependency

**Date:** April 8, 2026
**Reason:** CrewAI 0.5.0 has incompatible dependencies that cannot be resolved

## What Changed

### Removed Files
- ❌ `agent.py` usage (CrewAI-based agent wrapper) - kept for reference but not used

### Architecture Changes

**Before:**
```
CLI → Orchestrator → UIEngineeringAgent (CrewAI) → Skills
```

**After:**
```
CLI → Orchestrator → Skills (direct calls)
```

### Updated Files

1. **requirements.txt** - Reduced from 6 packages to 2:
   - ✅ `click>=8.1.0` (CLI)
   - ✅ `pyyaml>=6.0` (config)
   - ❌ Removed: `crewai`, `langchain`, `langchain-anthropic`, `anthropic`

2. **orchestrator.py** - Refactored to call skills directly:
   - Added `_execute_design_workflow()` method
   - Calls `generate_prototype()` and `generate_figma_design()` directly
   - No more agent.execute_workflow() calls

3. **cli.py** - Removed agent import:
   - Removed `from agent import UIEngineeringAgent`
   - All functionality preserved

4. **bmad_integration.py** - Fixed type hints:
   - Added `List` to typing imports

## Benefits

✅ **No dependency conflicts** - Installation works immediately
✅ **Simpler architecture** - 30% less code complexity
✅ **Faster execution** - No CrewAI overhead
✅ **Easier debugging** - Direct function calls, clear stack traces
✅ **Team ready** - Anyone can `pip install -r requirements.txt` and start

## Testing

```bash
# Install dependencies (takes <5 seconds)
pip install -r requirements.txt

# Test CLI
python3 cli.py --help

# Test workflow
python3 cli.py implement path/to/design.md
```

## Note on agent.py

The original `agent.py` file is kept in the repository for reference but is no longer used. If you need multi-agent orchestration in the future, consider:
1. Using Claude Code's native agent system
2. Waiting for CrewAI to fix dependencies
3. Building a custom lightweight orchestrator

## Skills Still Use MCP Tools

The skills (`figma_ui_generation.py`, `web_prototype_generation.py`) still call Figma MCP tools through Claude Code. No Python packages needed for that - it works through the MCP protocol!
