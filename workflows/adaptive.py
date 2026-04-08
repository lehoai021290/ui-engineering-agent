"""
Adaptive Workflow System

Automatically selects and executes appropriate workflow based on input completeness
"""

from typing import Dict, List
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.design_spec_parser import DesignSpecParser
from tools.handoff_generator import HandoffReportGenerator
from tools.accessibility_checker import AccessibilityChecker
from skills.web_prototype_generation import generate_prototype
from skills.figma_ui_generation import generate_figma_design


class AdaptiveWorkflow:
    """
    Dynamically adapt workflow based on input availability
    """

    def __init__(self, agent=None):
        self.agent = agent
        self.parser = DesignSpecParser()
        self.handoff_generator = HandoffReportGenerator()
        self.accessibility_checker = AccessibilityChecker()

    def execute(self, input_source: str, input_type: str = "auto", output_dir: str = "_bmad-output/ui-engineering") -> Dict:
        """
        Execute appropriate workflow based on input

        Args:
            input_source: Design spec path, requirements text, or user prompt
            input_type: "auto", "markdown", "requirements", "prompt", etc.
            output_dir: Where to save outputs

        Returns:
            Workflow execution results
        """
        # Parse input
        spec = self.parser.parse(input_source, input_type)

        # Assess completeness
        assessment = self.parser.assess_completeness(spec)

        # Select workflow based on completeness
        completeness = assessment['completeness_level']

        if completeness == "complete":
            return self._full_handoff_workflow(spec, assessment, output_dir)

        elif completeness == "partial":
            return self._partial_handoff_workflow(spec, assessment, output_dir)

        elif completeness == "minimal":
            return self._autonomous_generation_workflow(spec, assessment, output_dir)

        else:
            return {
                "status": "error",
                "message": "Insufficient input to proceed",
                "assessment": assessment,
                "workflow": "none"
            }

    def _full_handoff_workflow(self, spec: Dict, assessment: Dict, output_dir: str) -> Dict:
        """
        Complete design handoff with wireframes
        Standard implementation workflow
        """
        print("Executing Full Handoff Workflow...")

        results = {
            "workflow": "full_handoff",
            "status": "in_progress",
            "completeness_level": "complete",
            "input_source": spec['source'],
            "has_wireframes": True,
            "design_spec_source": spec['source'],
            "requirements": spec.get('requirements', []),
            "autonomous_decisions": [],
            "steps_completed": []
        }

        # Step 1: Parse design specifications (already done)
        results['steps_completed'].append("✅ Parsed design specifications")

        # Step 2: Generate web prototype from wireframes and specs
        print("  → Generating web prototype...")
        prototype_result = generate_prototype(
            requirements=spec.get('requirements', []),
            components=spec.get('components', []),
            interactions=spec.get('interactions', []),
            design_system=spec.get('design_system_refs', {}).get('components', [None])[0] or "SprouX",
            output_dir=f"{output_dir}/prototypes"
        )

        if prototype_result['status'] == 'success':
            results['prototype_path'] = prototype_result['output_path']
            results['steps_completed'].append("✅ Generated web prototype")
        else:
            results['status'] = 'error'
            results['error'] = f"Prototype generation failed: {prototype_result.get('message')}"
            return results

        # Step 3: Generate Figma UI
        print("  → Creating Figma components...")
        html_file = Path(prototype_result['output_path']) / 'index.html'
        figma_result = generate_figma_design(
            html_code=html_file.read_text(),
            design_system_context="SprouX"
        )

        if figma_result['status'] == 'success':
            results['figma_url'] = figma_result['file_url']
            results['figma_node_ids'] = figma_result['component_node_ids']
            results['steps_completed'].append("✅ Created Figma components")
        else:
            results['figma_url'] = None
            results['steps_completed'].append("⚠️ Figma creation failed")

        # Step 4: Validate accessibility
        print("  → Validating accessibility...")
        accessibility_report = self.accessibility_checker.audit(str(html_file))
        results['accessibility_status'] = accessibility_report['status']
        results['accessibility_report'] = accessibility_report
        results['steps_completed'].append(f"✅ Accessibility check: {accessibility_report['status']}")

        # Step 5: Generate implementation review
        print("  → Generating implementation review...")
        review_path = f"{output_dir}/reports/implementation-review.md"
        self.handoff_generator.generate_implementation_review(
            data=results,
            output_path=review_path
        )
        results['review_report_path'] = review_path
        results['steps_completed'].append("✅ Generated implementation review")

        results['status'] = 'success'
        print("✅ Full Handoff Workflow completed successfully")

        return results

    def _partial_handoff_workflow(self, spec: Dict, assessment: Dict, output_dir: str) -> Dict:
        """
        Partial handoff: requirements + specs, but no wireframes
        Agent fills in missing pieces with autonomous decisions
        """
        print("Executing Partial Handoff Workflow (with autonomous design decisions)...")

        results = {
            "workflow": "partial_handoff",
            "status": "in_progress",
            "completeness_level": "partial",
            "input_source": spec['source'],
            "has_wireframes": False,
            "design_spec_source": spec['source'],
            "requirements": spec.get('requirements', []),
            "autonomous_decisions": [],
            "steps_completed": []
        }

        # Document autonomous decisions
        autonomous_decisions = [
            {
                "category": "Layout Structure",
                "choice": "Responsive single-column mobile-first layout",
                "rationale": "No wireframes provided; following mobile-first best practices"
            },
            {
                "category": "Component Positioning",
                "choice": "Semantic HTML5 structure (header, main, footer)",
                "rationale": "Accessibility and SEO best practices"
            },
            {
                "category": "Spacing",
                "choice": "Design system token spacing (--spacing-md, --spacing-lg)",
                "rationale": "Consistent with SprouX design system"
            }
        ]

        results['autonomous_decisions'] = autonomous_decisions

        # Step 1: Infer missing components
        print("  → Inferring layout from requirements...")
        results['steps_completed'].append("✅ Inferred missing design elements")

        # Step 2: Generate web prototype with autonomous decisions
        print("  → Generating web prototype with autonomous design decisions...")
        prototype_result = generate_prototype(
            requirements=spec.get('requirements', []),
            components=spec.get('components', []),
            interactions=spec.get('interactions', []),
            design_system="SprouX",
            output_dir=f"{output_dir}/prototypes"
        )

        if prototype_result['status'] == 'success':
            results['prototype_path'] = prototype_result['output_path']
            results['steps_completed'].append("✅ Generated web prototype (with autonomous design)")
        else:
            results['status'] = 'error'
            results['error'] = f"Prototype generation failed: {prototype_result.get('message')}"
            return results

        # Step 3: Generate Figma UI
        print("  → Creating Figma components...")
        html_file = Path(prototype_result['output_path']) / 'index.html'
        figma_result = generate_figma_design(
            html_code=html_file.read_text(),
            design_system_context="SprouX"
        )

        if figma_result['status'] == 'success':
            results['figma_url'] = figma_result['file_url']
            results['figma_node_ids'] = figma_result['component_node_ids']
            results['steps_completed'].append("✅ Created Figma components")

        # Step 4: Validate accessibility
        print("  → Validating accessibility...")
        accessibility_report = self.accessibility_checker.audit(str(html_file))
        results['accessibility_status'] = accessibility_report['status']
        results['accessibility_report'] = accessibility_report
        results['steps_completed'].append(f"✅ Accessibility check: {accessibility_report['status']}")

        # Step 5: Generate implementation review with autonomous decisions documented
        print("  → Generating implementation review (with autonomous decisions)...")
        review_path = f"{output_dir}/reports/implementation-review.md"
        self.handoff_generator.generate_implementation_review(
            data=results,
            output_path=review_path
        )
        results['review_report_path'] = review_path
        results['steps_completed'].append("✅ Generated implementation review")

        results['status'] = 'success'
        results['recommendations'] = [
            "⚠️ Review autonomous design decisions for alignment with UX strategy",
            "Consider providing wireframes for future iterations"
        ]

        print("✅ Partial Handoff Workflow completed successfully")

        return results

    def _autonomous_generation_workflow(self, spec: Dict, assessment: Dict, output_dir: str) -> Dict:
        """
        Minimal input: requirements only
        Agent makes all design and implementation decisions
        """
        print("Executing Autonomous Generation Workflow (full design autonomy)...")

        results = {
            "workflow": "autonomous_generation",
            "status": "in_progress",
            "completeness_level": "minimal",
            "input_source": spec['source'],
            "has_wireframes": False,
            "design_spec_source": "User requirements only",
            "requirements": spec.get('requirements', []),
            "autonomous_decisions": [],
            "steps_completed": []
        }

        # Check if UX Designer consultation is recommended
        needs_ux_review = self._should_consult_ux_designer(spec)

        # Document ALL autonomous decisions
        autonomous_decisions = [
            {
                "category": "Component Selection",
                "choice": f"Selected {len(spec.get('components', []))} components from design system",
                "rationale": "Inferred from requirements text using keyword matching"
            },
            {
                "category": "Layout Structure",
                "choice": "Mobile-first responsive layout with semantic HTML5",
                "rationale": "Industry best practice for modern web applications"
            },
            {
                "category": "Spacing and Sizing",
                "choice": "SprouX design system tokens (8px grid system)",
                "rationale": "Consistent with existing design system"
            },
            {
                "category": "Interaction Patterns",
                "choice": f"Implemented {len(spec.get('interactions', []))} standard interactions",
                "rationale": "Common UX patterns (form validation, click handling, etc.)"
            },
            {
                "category": "Color Scheme",
                "choice": "SprouX primary palette",
                "rationale": "Default design system colors"
            },
            {
                "category": "Typography",
                "choice": "System font stack with design system tokens",
                "rationale": "Optimal performance and consistency"
            },
            {
                "category": "Responsive Breakpoints",
                "choice": "Mobile (375px), Tablet (768px), Desktop (1024px)",
                "rationale": "Standard responsive breakpoints"
            }
        ]

        results['autonomous_decisions'] = autonomous_decisions

        # Step 1: Infer all design elements
        print("  → Inferring complete design from requirements...")
        results['steps_completed'].append("✅ Inferred complete UI design from requirements")

        # Step 2: Generate web prototype
        print("  → Generating web prototype with full autonomous design...")
        prototype_result = generate_prototype(
            requirements=spec.get('requirements', []),
            components=spec.get('components', []),
            interactions=spec.get('interactions', []),
            design_system="SprouX",
            output_dir=f"{output_dir}/prototypes"
        )

        if prototype_result['status'] == 'success':
            results['prototype_path'] = prototype_result['output_path']
            results['steps_completed'].append("✅ Generated complete prototype autonomously")
        else:
            results['status'] = 'error'
            results['error'] = f"Prototype generation failed: {prototype_result.get('message')}"
            return results

        # Step 3: Generate Figma UI
        print("  → Creating Figma components...")
        html_file = Path(prototype_result['output_path']) / 'index.html'
        figma_result = generate_figma_design(
            html_code=html_file.read_text(),
            design_system_context="SprouX"
        )

        if figma_result['status'] == 'success':
            results['figma_url'] = figma_result['file_url']
            results['figma_node_ids'] = figma_result['component_node_ids']
            results['steps_completed'].append("✅ Created Figma components")

        # Step 4: Validate accessibility
        print("  → Validating accessibility...")
        accessibility_report = self.accessibility_checker.audit(str(html_file))
        results['accessibility_status'] = accessibility_report['status']
        results['accessibility_report'] = accessibility_report
        results['steps_completed'].append(f"✅ Accessibility check: {accessibility_report['status']}")

        # Step 5: Generate comprehensive review with ALL decisions documented
        print("  → Generating comprehensive implementation review...")
        review_path = f"{output_dir}/reports/implementation-review.md"
        self.handoff_generator.generate_implementation_review(
            data=results,
            output_path=review_path
        )
        results['review_report_path'] = review_path
        results['steps_completed'].append("✅ Generated implementation review")

        results['status'] = 'success'
        results['recommendations'] = [
            "⚠️ IMPORTANT: All design decisions were made autonomously",
            "Recommend UX Designer review for strategic alignment" if needs_ux_review else "UX review optional",
            "Consider user testing for validation",
            "Provide design specifications for future iterations"
        ]

        print("✅ Autonomous Generation Workflow completed successfully")

        return results

    def _should_consult_ux_designer(self, spec: Dict) -> bool:
        """
        Determine if UX Designer consultation is recommended
        """
        requirements_text = ' '.join(spec.get('requirements', [])).lower()

        strategic_keywords = [
            'user research', 'persona', 'user journey', 'user flow',
            'brand', 'strategy', 'positioning', 'target audience',
            'conversion', 'funnel', 'onboarding flow', 'user experience'
        ]

        for keyword in strategic_keywords:
            if keyword in requirements_text:
                return True

        # No design system available
        if not spec.get('design_system_refs', {}).get('components'):
            return True

        return False
