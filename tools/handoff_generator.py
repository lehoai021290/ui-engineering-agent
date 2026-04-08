"""
Handoff Report Generator

Generates implementation review reports for UX Designer
Includes documentation of autonomous design decisions
"""

from pathlib import Path
from datetime import datetime
import json
from typing import Dict, List, Optional


class HandoffReportGenerator:
    """
    Generate implementation review reports for UX Designer
    """

    def __init__(self, template_dir: str = None):
        if template_dir is None:
            template_dir = Path(__file__).parent.parent / "templates"
        self.template_dir = Path(template_dir)

    def generate_implementation_review(self, data: Dict, output_path: str) -> str:
        """
        Generate implementation review report

        Args:
            data: Implementation results and metadata
            output_path: Where to save the report

        Returns:
            Path to generated report
        """
        template = self._load_template("implementation_review.md")

        # Determine if autonomous decisions were made
        completeness_level = data.get('completeness_level', 'unknown')
        has_autonomous = completeness_level in ['minimal', 'partial']

        report = template.format(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            input_source=data.get('input_source', 'N/A'),
            completeness_level=completeness_level.upper(),
            has_wireframes="✅ Yes" if data.get('has_wireframes') else "❌ No",
            design_spec=data.get('design_spec_source', 'N/A'),
            requirements_summary=self._format_requirements(data.get('requirements', [])),
            autonomous_decisions_section=self._format_autonomous_section(data, has_autonomous),
            design_decisions_list=self._format_design_decisions(data.get('autonomous_decisions', [])),
            prototype_url=data.get('prototype_path', 'N/A'),
            figma_url=data.get('figma_url', 'N/A'),
            figma_nodes=self._format_figma_nodes(data.get('figma_node_ids', [])),
            technical_notes=self._format_technical_notes(data.get('technical_notes', [])),
            accessibility_status=data.get('accessibility_status', 'Not checked'),
            accessibility_details=self._format_accessibility(data.get('accessibility_report', {})),
            questions=self._format_questions(data.get('questions_for_ux', [])),
            constraints=self._format_constraints(data.get('constraints', [])),
            recommendations=self._format_recommendations(data.get('recommendations', []))
        )

        # Write to file
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w') as f:
            f.write(report)

        return str(output_file)

    def generate_clarification_request(self, questions: List[str], context: Dict, output_path: str) -> str:
        """
        Generate clarification request for UX Designer

        Args:
            questions: List of questions needing clarification
            context: Context about the implementation
            output_path: Where to save the request

        Returns:
            Path to generated request
        """
        content = f"""# Clarification Needed

**From**: UI Engineering Agent
**To**: UX Designer Agent
**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Context

**Design Spec**: {context.get('design_spec', 'N/A')}
**Current Status**: {context.get('status', 'In progress')}

## Questions

{self._format_questions(questions)}

---

**Impact**: Implementation is paused pending clarification.

**Please provide feedback so I can continue with implementation.**
"""

        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w') as f:
            f.write(content)

        return str(output_file)

    def _load_template(self, template_name: str) -> str:
        """Load markdown template"""
        template_path = self.template_dir / template_name

        if not template_path.exists():
            # Return default template
            return self._get_default_implementation_review_template()

        with open(template_path, 'r') as f:
            return f.read()

    def _get_default_implementation_review_template(self) -> str:
        """Default implementation review template"""
        return """# Implementation Review

**Generated**: {timestamp}
**Input Source**: {input_source}
**Input Completeness**: {completeness_level}

---

## Input Summary

**Design Spec**: {design_spec}
**Wireframes Available**: {has_wireframes}
**Requirements**:
{requirements_summary}

---

{autonomous_decisions_section}

---

## Deliverables

### Web Prototype
- **Location**: {prototype_url}
- **Status**: ✅ Complete

### Figma Components
- **File**: {figma_url}
- **Components**:
{figma_nodes}

---

## Technical Notes

{technical_notes}

---

## Accessibility

**Status**: {accessibility_status}

{accessibility_details}

---

## Questions for UX Review

{questions}

---

## Technical Constraints

{constraints}

---

## Recommendations

{recommendations}

---

**Next Steps**: Please review implementation and provide feedback.
"""

    def _format_autonomous_section(self, data: Dict, has_autonomous: bool) -> str:
        """Format autonomous decisions section"""
        if not has_autonomous:
            return "## Design Implementation\n\nImplementation follows provided design specifications precisely."

        completeness = data.get('completeness_level', 'partial')

        if completeness == 'minimal':
            note = "⚠️ **Autonomous Design Mode**: Due to minimal input (requirements only), all design decisions were made autonomously based on best practices and design system guidelines."
        else:
            note = "ℹ️ **Partial Autonomy**: Some design decisions were made autonomously due to missing wireframes."

        return f"""## Autonomous Design Decisions

{note}

### Design Decisions Made

{self._format_design_decisions(data.get('autonomous_decisions', []))}

> **Review Recommended**: Please review autonomous design decisions for strategic alignment with product vision.
"""

    def _format_requirements(self, requirements: List[str]) -> str:
        """Format requirements list"""
        if not requirements:
            return "  - No requirements specified"

        return "\n".join([f"  - {req}" for req in requirements[:5]])  # First 5

    def _format_design_decisions(self, decisions: List[Dict]) -> str:
        """Format autonomous design decisions"""
        if not decisions:
            return "No autonomous decisions made."

        lines = []
        for decision in decisions:
            if isinstance(decision, dict):
                category = decision.get('category', 'General')
                choice = decision.get('choice', 'N/A')
                rationale = decision.get('rationale', 'Based on best practices')
                lines.append(f"- **{category}**: {choice}")
                lines.append(f"  - *Rationale*: {rationale}")
            else:
                lines.append(f"- {decision}")

        return "\n".join(lines)

    def _format_figma_nodes(self, node_ids: List[str]) -> str:
        """Format Figma node IDs as markdown list"""
        if not node_ids:
            return "  - No components created yet"

        return "\n".join([f"  - {node}" for node in node_ids])

    def _format_technical_notes(self, notes: List[str]) -> str:
        """Format technical notes"""
        if not notes:
            return "No technical notes."

        return "\n".join([f"- {note}" for note in notes])

    def _format_accessibility(self, report: Dict) -> str:
        """Format accessibility report"""
        if not report:
            return "No accessibility audit performed yet."

        lines = [
            f"- **WCAG Level**: {report.get('wcag_level', 'AA')}",
            f"- **Issues Found**: {len(report.get('issues', []))}",
        ]

        if report.get('issues'):
            lines.append("\n**Issues**:")
            for issue in report['issues'][:5]:  # First 5
                lines.append(f"  - {issue}")

        return "\n".join(lines)

    def _format_questions(self, questions: List[str]) -> str:
        """Format questions for UX Designer"""
        if not questions:
            return "No questions at this time."

        return "\n".join([f"{i+1}. {q}" for i, q in enumerate(questions)])

    def _format_constraints(self, constraints: List[str]) -> str:
        """Format technical constraints"""
        if not constraints:
            return "No constraints identified."

        return "\n".join([f"- {c}" for c in constraints])

    def _format_recommendations(self, recommendations: List[str]) -> str:
        """Format recommendations"""
        if not recommendations:
            return "No additional recommendations."

        return "\n".join([f"- {rec}" for rec in recommendations])
