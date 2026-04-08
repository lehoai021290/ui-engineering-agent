#!/usr/bin/env python3
"""
UI Engineering Agent - Command Line Interface

Professional CLI for UI Engineering Agent operations
Refactored to call skills directly without CrewAI dependency
"""

import click
from orchestrator import WorkflowOrchestrator
from bmad_integration import BMADIntegration
from pathlib import Path


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """
    UI Engineering Agent - Design-to-Code Automation

    Intelligent agent for generating web prototypes and Figma UI
    from design specifications, requirements, or prompts.
    """
    pass


@cli.command()
@click.option('--interval', '-i', default=30, help='Polling interval in seconds')
@click.option('--max-iterations', '-m', default=None, type=int, help='Maximum polling iterations')
def watch(interval, max_iterations):
    """
    Watch for design handoffs from BMAD UX Designer

    Monitors _bmad-output/ for completed designs and automatically
    generates prototypes and Figma UI.
    """
    orchestrator = WorkflowOrchestrator()

    click.echo(click.style("🔍 UI Engineering Agent - Watch Mode", fg='cyan', bold=True))
    click.echo()

    orchestrator.watch_for_handoff(interval=interval, max_iterations=max_iterations)


@cli.command()
@click.argument('design_spec_path', type=click.Path(exists=True))
def implement(design_spec_path):
    """
    Implement a specific design specification

    Generates web prototype and Figma UI from a design spec file.
    Supports markdown, YAML, and JSON formats.

    Example:
        ui-engineer implement _bmad-output/ux-design/login-flow.md
    """
    orchestrator = WorkflowOrchestrator()

    click.echo(click.style("🚀 UI Engineering Agent - Manual Implementation", fg='cyan', bold=True))
    click.echo(f"   Design Spec: {design_spec_path}")
    click.echo()

    result = orchestrator.manual_execution(design_spec_path)

    if result.get('status') == 'success':
        click.echo()
        click.secho("✅ Implementation successful!", fg='green', bold=True)
    else:
        click.echo()
        click.secho(f"❌ Implementation failed: {result.get('message', 'Unknown error')}", fg='red')


@cli.command()
@click.argument('prompt', nargs=-1, required=True)
def generate(prompt):
    """
    Quick generation from user prompt

    Generates complete prototype and Figma UI from a simple
    text description. Makes autonomous design decisions.

    Example:
        ui-engineer generate "Build a login page with email and password"
    """
    orchestrator = WorkflowOrchestrator()

    user_prompt = " ".join(prompt)

    click.echo(click.style("⚡ UI Engineering Agent - Quick Generation", fg='cyan', bold=True))
    click.echo(f"   Prompt: {user_prompt}")
    click.echo()

    result = orchestrator.quick_generate(user_prompt)

    if result.get('status') == 'success':
        click.echo()
        click.secho("✅ Generation successful!", fg='green', bold=True)
    else:
        click.echo()
        click.secho(f"❌ Generation failed: {result.get('message', 'Unknown error')}", fg='red')


@cli.command()
@click.argument('html_file', type=click.Path(exists=True))
@click.option('--output', '-o', help='Output Figma file name')
def to_figma(html_file, output):
    """
    Convert HTML prototype to Figma UI

    Takes an existing HTML file and generates Figma UI
    with design system mapping.

    Example:
        ui-engineer to-figma prototypes/dashboard.html
    """
    from skills.figma_ui_generation import generate_figma_from_file

    click.echo(click.style("🎨 Converting HTML to Figma", fg='cyan', bold=True))
    click.echo(f"   HTML File: {html_file}")
    click.echo()

    result = generate_figma_from_file(html_file)

    if result['status'] == 'success':
        click.echo()
        click.secho("✅ Figma UI created!", fg='green', bold=True)
        click.echo(f"   Figma URL: {result['file_url']}")
        click.echo(f"   Components: {len(result['component_node_ids'])}")
    else:
        click.echo()
        click.secho(f"❌ Conversion failed: {result.get('message', 'Unknown error')}", fg='red')


@cli.command()
def status():
    """
    Check current workflow status

    Shows the current state of BMAD workflow integration
    and any pending handoffs or implementations.
    """
    orchestrator = WorkflowOrchestrator()

    click.echo(click.style("📊 Workflow Status", fg='cyan', bold=True))
    click.echo()

    orchestrator.status()


@cli.command()
@click.option('--questions', '-q', multiple=True, required=True, help='Question to ask UX Designer')
@click.option('--context', '-c', help='Context description')
def clarify(questions, context):
    """
    Request clarification from UX Designer

    Pauses implementation and sends questions to UX Designer for review.

    Example:
        ui-engineer clarify -q "Should we use modal or inline form?" -q "What's the error state?"
    """
    orchestrator = WorkflowOrchestrator()

    context_dict = {
        "design_spec": "Current implementation",
        "status": "Needs clarification",
        "workflow": "Manual"
    }

    if context:
        context_dict["description"] = context

    orchestrator.request_clarification(list(questions), context_dict)

    click.secho("✅ Clarification request sent!", fg='green')


@cli.group()
def dev():
    """Development and testing commands"""
    pass


@dev.command()
@click.argument('design_spec_path', type=click.Path(exists=True))
def parse(design_spec_path):
    """
    Parse and analyze design specification

    Shows detailed analysis of design spec completeness and
    what workflow will be used.
    """
    from tools.design_spec_parser import DesignSpecParser

    parser = DesignSpecParser()

    click.echo(click.style("🔍 Parsing Design Specification", fg='cyan', bold=True))
    click.echo(f"   File: {design_spec_path}")
    click.echo()

    spec = parser.parse(design_spec_path)
    assessment = parser.assess_completeness(spec)

    click.echo(click.style("Specification Details:", fg='yellow', bold=True))
    click.echo(f"   Format: {spec['format']}")
    click.echo(f"   Source: {spec['source']}")
    click.echo(f"   Requirements: {len(spec.get('requirements', []))}")
    click.echo(f"   Components: {len(spec.get('components', []))}")
    click.echo(f"   Interactions: {len(spec.get('interactions', []))}")
    click.echo(f"   Wireframes: {len(spec.get('wireframe_refs', []))}")
    click.echo()

    click.echo(click.style("Completeness Assessment:", fg='yellow', bold=True))
    click.echo(f"   Level: {assessment['completeness_level']}")
    click.echo(f"   Can Proceed: {assessment['can_proceed']}")

    if assessment.get('missing_elements'):
        click.echo(f"   Missing: {', '.join(assessment['missing_elements'])}")

    if assessment.get('recommendations'):
        click.echo()
        click.echo(click.style("Recommendations:", fg='yellow', bold=True))
        for rec in assessment['recommendations']:
            click.echo(f"   • {rec}")


@dev.command()
@click.argument('html_file', type=click.Path(exists=True))
def audit(html_file):
    """
    Run accessibility audit on HTML file

    Validates HTML against WCAG 2.1 AA standards.
    """
    from tools.accessibility_checker import audit_accessibility

    click.echo(click.style("♿ Accessibility Audit", fg='cyan', bold=True))
    click.echo(f"   File: {html_file}")
    click.echo()

    result = audit_accessibility(html_file)

    click.echo(click.style("Audit Results:", fg='yellow', bold=True))
    click.echo(f"   Status: {result['status']}")
    click.echo(f"   WCAG Level: {result['wcag_level']}")
    click.echo(f"   Issues: {result['issues_count']}")

    if result['issues']:
        click.echo()
        click.echo(click.style("Issues Found:", fg='red', bold=True))
        for issue in result['issues']:
            click.echo(f"   • {issue}")

    if result['recommendations']:
        click.echo()
        click.echo(click.style("Recommendations:", fg='yellow', bold=True))
        for rec in result['recommendations']:
            click.echo(f"   • {rec}")


@cli.command()
def info():
    """
    Show agent information and configuration
    """
    import yaml

    config_path = Path(__file__).parent / "config.yaml"

    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    click.echo(click.style("UI Engineering Agent v1.0.0", fg='cyan', bold=True))
    click.echo()

    click.echo(click.style("Configuration:", fg='yellow', bold=True))
    click.echo(f"   Name: {config['agent']['name']}")
    click.echo(f"   Model: {config['agent']['model']}")
    click.echo(f"   Role: {config['agent']['persona']['role']}")
    click.echo()

    click.echo(click.style("Skills:", fg='yellow', bold=True))
    for skill in config['agent']['skills']:
        click.echo(f"   • {skill['name']} ({skill['type']})")

    click.echo()
    click.echo(click.style("Workflows:", fg='yellow', bold=True))
    for workflow in config['agent']['workflows']['available']:
        click.echo(f"   • {workflow['name']}: {workflow['description']}")


if __name__ == '__main__':
    cli()
