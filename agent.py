"""
UI Engineering Agent - Core Implementation

CrewAI-based agent for design-to-code workflows
Handles flexible input (wireframes, requirements, or prompts)
Collaborates with BMAD UX Designer agent
"""

from crewai import Agent, Task, Crew, Process
from langchain.tools import Tool
from langchain_anthropic import ChatAnthropic
import yaml
import os
from pathlib import Path
from typing import Dict, List, Optional

# Import our custom tools and workflows
from tools.design_spec_parser import parse_spec, DesignSpecParser
from tools.handoff_generator import HandoffReportGenerator
from tools.accessibility_checker import audit_accessibility
from skills.web_prototype_generation import generate_prototype
from skills.figma_ui_generation import generate_figma_design, generate_figma_from_file
from workflows.adaptive import AdaptiveWorkflow


class UIEngineeringAgent:
    """
    UI Engineering Agent for design-to-code workflows
    Built with CrewAI for multi-agent collaboration
    """

    def __init__(self, config_path: str = None):
        """
        Initialize UI Engineering Agent

        Args:
            config_path: Path to config.yaml (defaults to ./config.yaml)
        """
        if config_path is None:
            config_path = Path(__file__).parent / "config.yaml"

        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        # Initialize components
        self.parser = DesignSpecParser()
        self.handoff_generator = HandoffReportGenerator()
        self.adaptive_workflow = AdaptiveWorkflow(agent=self)

        # Setup CrewAI components
        self.llm = self._setup_llm()
        self.tools = self._setup_tools()
        self.agent = self._create_agent()

    def _setup_llm(self) -> ChatAnthropic:
        """Setup Claude LLM for the agent"""
        model_name = self.config['agent']['model']

        # Map config model names to Anthropic model IDs
        model_mapping = {
            'claude-sonnet-4.5': 'claude-sonnet-4-20250514',
            'claude-opus-4.6': 'claude-opus-4-20250514',
            'claude-haiku-4.5': 'claude-haiku-4-20250514'
        }

        model_id = model_mapping.get(model_name, 'claude-sonnet-4-20250514')

        return ChatAnthropic(
            model=model_id,
            temperature=0.7,
            max_tokens=4096
        )

    def _setup_tools(self) -> List[Tool]:
        """Setup tools for the agent"""
        tools = []

        # Tool 1: Design Spec Parser
        tools.append(Tool(
            name="parse_design_spec",
            func=self._parse_design_spec_tool,
            description="""Parse design specifications from multiple input formats.
                          Input: file path, requirements text, or user prompt.
                          Handles: Markdown, YAML, JSON, plain text requirements, direct prompts.
                          Output: Structured design specification with completeness assessment.
                          Use this FIRST to understand what input you're working with."""
        ))

        # Tool 2: Web Prototype Generation
        tools.append(Tool(
            name="generate_web_prototype",
            func=self._generate_prototype_tool,
            description="""Generate functional web prototypes (HTML/CSS/JS) from requirements.
                          Input: design specification dictionary.
                          Output: Path to generated prototype files.
                          Use this to create interactive web prototypes from design specs."""
        ))

        # Tool 3: Figma UI Generation
        tools.append(Tool(
            name="generate_figma_ui",
            func=self._generate_figma_tool,
            description="""Convert web prototype code into Figma designs with component mapping.
                          Input: HTML file path or HTML code string.
                          Output: Figma file URL and component node IDs.
                          Use this after generating web prototype to create Figma UI."""
        ))

        # Tool 4: Accessibility Check
        tools.append(Tool(
            name="check_accessibility",
            func=self._check_accessibility_tool,
            description="""Validate HTML prototype against WCAG 2.1 AA standards.
                          Input: HTML file path.
                          Output: Accessibility audit report with issues and recommendations.
                          Use this to ensure prototypes meet accessibility standards."""
        ))

        # Tool 5: Generate Review Report
        tools.append(Tool(
            name="generate_review_report",
            func=self._generate_review_report_tool,
            description="""Generate implementation review report for UX Designer.
                          Input: Implementation results and metadata.
                          Output: Path to generated review report.
                          Use this as the final step to document implementation."""
        ))

        return tools

    def _create_agent(self) -> Agent:
        """Create the CrewAI agent with flexible input handling"""
        return Agent(
            role=self.config['agent']['persona']['role'],
            goal="""Translate UX designs OR user requirements into high-quality,
                    performant, and accessible UI code and Figma UI.
                    Adapt workflow based on input completeness.""",
            backstory="""You are an expert UI engineer with deep knowledge of
                        front-end development, design systems, and accessibility
                        standards. You excel at bridging the gap between design
                        and implementation, always considering technical feasibility,
                        performance, and user experience.

                        INPUT FLEXIBILITY - You handle multiple input scenarios:
                        1. Full handoff with wireframes: Follow design precisely
                        2. Design specs without wireframes: Make informed layout decisions
                        3. Requirements only: Generate complete design autonomously
                        4. Direct prompts: Create everything from minimal input

                        DECISION-MAKING AUTHORITY:
                        - Autonomous decisions: Component selection, layout, spacing,
                          interaction patterns, accessibility, responsive design
                        - Consult UX Designer: Strategic UX decisions, brand design,
                          complex user flows, novel patterns

                        WORKFLOW APPROACH:
                        1. Parse input to assess completeness
                        2. Select appropriate workflow (full/partial/autonomous)
                        3. Generate web prototype
                        4. Generate Figma UI UI
                        5. Validate accessibility
                        6. Document all decisions (especially autonomous ones)
                        7. Generate review report

                        Always be transparent about autonomous decisions and
                        recommend UX Designer review when strategic alignment is needed.""",
            tools=self.tools,
            llm=self.llm,
            verbose=True,
            allow_delegation=True,  # Can delegate to UX Designer
            memory=True  # Maintain conversation context
        )

    # Tool wrapper methods

    def _parse_design_spec_tool(self, input_source: str) -> str:
        """Tool wrapper for design spec parser"""
        try:
            spec = parse_spec(input_source)
            assessment = self.parser.assess_completeness(spec)

            result = {
                "spec": spec,
                "assessment": assessment
            }

            return f"""Design Specification Parsed:
- Format: {spec['format']}
- Completeness: {assessment['completeness_level']}
- Can Proceed: {assessment['can_proceed']}
- Requirements: {len(spec.get('requirements', []))} items
- Components: {len(spec.get('components', []))} identified
- Wireframes: {'Yes' if spec.get('wireframe_refs') else 'No'}

Assessment: {assessment['completeness_level']}
Recommendations: {', '.join(assessment.get('recommendations', []))}

Next Steps: {', '.join(assessment.get('recommendations', [])[:2])}
"""
        except Exception as e:
            return f"Error parsing design spec: {str(e)}"

    def _generate_prototype_tool(self, spec_dict: str) -> str:
        """Tool wrapper for web prototype generation"""
        try:
            # Parse spec_dict if it's a string
            import ast
            if isinstance(spec_dict, str):
                spec_dict = ast.literal_eval(spec_dict)

            result = generate_prototype(
                requirements=spec_dict.get('requirements', []),
                components=spec_dict.get('components', []),
                interactions=spec_dict.get('interactions', []),
                design_system='SprouX'
            )

            if result['status'] == 'success':
                return f"""Web Prototype Generated Successfully:
- Output Path: {result['output_path']}
- Files: {', '.join(result['generated_files'])}
- Components Used: {result['metadata']['components_used']}
- Interactions: {result['metadata']['interactions_implemented']}

Next: Use generate_figma_ui tool to create Figma UI
"""
            else:
                return f"Error generating prototype: {result.get('message', 'Unknown error')}"

        except Exception as e:
            return f"Error in prototype generation tool: {str(e)}"

    def _generate_figma_tool(self, html_path: str) -> str:
        """Tool wrapper for Figma UI generation"""
        try:
            result = generate_figma_from_file(html_path)

            if result['status'] == 'success':
                return f"""Figma UI Generated Successfully:
- Figma URL: {result['file_url']}
- Components: {len(result['component_node_ids'])} created
- Node IDs: {', '.join(result['component_node_ids'][:5])}
- Mapping: {result['mapping_report']['components_mapped']} mapped, {result['mapping_report']['components_created']} created

Next: Use check_accessibility tool to validate the prototype
"""
            else:
                return f"Error generating Figma UI: {result.get('message', 'Unknown error')}"

        except Exception as e:
            return f"Error in Figma generation tool: {str(e)}"

    def _check_accessibility_tool(self, html_file_path: str) -> str:
        """Tool wrapper for accessibility checker"""
        try:
            result = audit_accessibility(html_file_path)

            return f"""Accessibility Audit Complete:
- Status: {result['status']}
- WCAG Level: {result['wcag_level']}
- Issues Found: {result['issues_count']}
- File: {result['file']}

Issues:
{chr(10).join(['- ' + issue for issue in result['issues'][:5]])}

Recommendations:
{chr(10).join(['- ' + rec for rec in result['recommendations'][:3]])}

Next: Use generate_review_report tool to create final documentation
"""
        except Exception as e:
            return f"Error checking accessibility: {str(e)}"

    def _generate_review_report_tool(self, results_dict: str) -> str:
        """Tool wrapper for review report generation"""
        try:
            import ast
            if isinstance(results_dict, str):
                results_dict = ast.literal_eval(results_dict)

            output_path = "_bmad-output/ui-engineering/reports/implementation-review.md"
            report_path = self.handoff_generator.generate_implementation_review(
                data=results_dict,
                output_path=output_path
            )

            return f"""Implementation Review Report Generated:
- Report Path: {report_path}
- Ready for UX Designer review

Workflow Complete! All deliverables created.
"""
        except Exception as e:
            return f"Error generating review report: {str(e)}"

    # High-level execution methods

    def execute_workflow(self, workflow_type: str = "auto", input_data: Dict = None) -> Dict:
        """
        Execute workflow with automatic adaptation to input type

        Args:
            workflow_type: "auto" (detect), "full_handoff", "partial", "autonomous"
            input_data: Can be:
                - {"design_spec_path": "path/to/spec.md"}
                - {"requirements": "Build a login page..."}
                - {"user_prompt": "Create a dashboard"}

        Returns:
            Workflow execution results
        """
        # If auto, use adaptive workflow
        if workflow_type == "auto":
            # Determine input source
            if 'design_spec_path' in input_data:
                return self.adaptive_workflow.execute(input_data['design_spec_path'])
            elif 'requirements' in input_data:
                return self.adaptive_workflow.execute(
                    input_data['requirements'],
                    input_type="requirements"
                )
            elif 'user_prompt' in input_data:
                return self.adaptive_workflow.execute(
                    input_data['user_prompt'],
                    input_type="prompt"
                )
            else:
                raise ValueError("Invalid input_data format")

        # Otherwise, use CrewAI task-based execution
        elif workflow_type == "crewai_tasks":
            return self._execute_crewai_workflow(input_data)

        else:
            raise ValueError(f"Unknown workflow type: {workflow_type}")

    def _execute_crewai_workflow(self, input_data: Dict) -> Dict:
        """
        Execute workflow using CrewAI tasks
        This demonstrates using the agent with explicit tasks
        """
        input_source = (
            input_data.get('design_spec_path') or
            input_data.get('requirements') or
            input_data.get('user_prompt')
        )

        # Define tasks
        tasks = [
            Task(
                description=f"""Parse the design input from: {input_source}
                               Assess completeness and determine workflow type.
                               Use the parse_design_spec tool.""",
                agent=self.agent,
                expected_output="Design specification with completeness assessment"
            ),
            Task(
                description="""Based on the parsed design specification, generate a web prototype.
                               Use the generate_web_prototype tool with the parsed spec.""",
                agent=self.agent,
                expected_output="Path to generated web prototype files"
            ),
            Task(
                description="""Convert the generated web prototype into Figma UI.
                               Use the generate_figma_ui tool with the prototype HTML path.""",
                agent=self.agent,
                expected_output="Figma file URL with component node IDs"
            ),
            Task(
                description="""Validate the prototype for accessibility compliance.
                               Use the check_accessibility tool with the HTML file.""",
                agent=self.agent,
                expected_output="Accessibility audit report"
            ),
            Task(
                description="""Generate final implementation review report.
                               Document all deliverables and any autonomous decisions made.
                               Use the generate_review_report tool.""",
                agent=self.agent,
                expected_output="Path to implementation review report"
            )
        ]

        # Create crew
        crew = Crew(
            agents=[self.agent],
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )

        # Execute
        result = crew.kickoff()

        return {
            "status": "success",
            "workflow": "crewai_tasks",
            "result": str(result)
        }

    def quick_generate(self, user_input: str) -> Dict:
        """
        Quick generation from user input
        Automatically selects workflow and generates everything

        Args:
            user_input: Design spec path, requirements, or prompt

        Returns:
            Complete workflow results
        """
        return self.execute_workflow(
            workflow_type="auto",
            input_data={"user_prompt": user_input}
        )


# Example usage
if __name__ == "__main__":
    import sys

    # Initialize agent
    agent = UIEngineeringAgent()

    # Example 1: Full handoff with design spec
    if len(sys.argv) > 1 and sys.argv[1] == "full":
        print("Running full handoff workflow...")
        result = agent.execute_workflow(
            workflow_type="auto",
            input_data={
                "design_spec_path": "_bmad-output/ux-design/onboarding-flow.md"
            }
        )
        print(f"\nResult: {result['status']}")
        print(f"Workflow: {result['workflow']}")

    # Example 2: Requirements only
    elif len(sys.argv) > 1 and sys.argv[1] == "requirements":
        print("Running autonomous generation workflow...")
        result = agent.execute_workflow(
            workflow_type="auto",
            input_data={
                "requirements": """
                User Story: As a user, I want to log in with email and password

                Acceptance Criteria:
                - Email input field with validation
                - Password input field (masked)
                - Remember me checkbox
                - Forgot password link
                - Submit button
                - Error messages for invalid credentials
                """
            }
        )
        print(f"\nResult: {result['status']}")
        print(f"Workflow: {result['workflow']}")

    # Example 3: Quick prompt
    elif len(sys.argv) > 1:
        user_prompt = " ".join(sys.argv[1:])
        print(f"Running quick generation: {user_prompt}")
        result = agent.quick_generate(user_prompt)
        print(f"\nResult: {result['status']}")

    else:
        print("UI Engineering Agent - Ready")
        print("\nUsage:")
        print("  python agent.py full                    # Full handoff workflow")
        print("  python agent.py requirements            # Requirements-only workflow")
        print("  python agent.py <prompt>                # Quick generation")
        print("\nExample:")
        print("  python agent.py 'Build a product dashboard with metrics'")
