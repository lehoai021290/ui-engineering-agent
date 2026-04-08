"""
BMAD Integration Layer

Handles communication with BMAD UX Designer agent
Manages handoff detection, acknowledgment, and artifact exchange
"""

import yaml
import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class BMADIntegration:
    """
    Manage communication with BMAD UX Designer agent
    """

    def __init__(self, bmad_output_dir: str = "_bmad-output"):
        self.bmad_output_dir = Path(bmad_output_dir)
        self.ux_design_dir = self.bmad_output_dir / "ux-design"
        self.ui_engineering_dir = self.bmad_output_dir / "ui-engineering"

        # Create output directory
        self.ui_engineering_dir.mkdir(parents=True, exist_ok=True)
        (self.ui_engineering_dir / "reports").mkdir(exist_ok=True)
        (self.ui_engineering_dir / "prototypes").mkdir(exist_ok=True)
        (self.ui_engineering_dir / "figma").mkdir(exist_ok=True)

    def check_for_handoff(self) -> Optional[Dict]:
        """
        Check if UX Designer has completed a design for handoff

        Returns:
            Dict with handoff data if available, None otherwise
        """
        # Look for status file indicating design completion
        status_file = self.bmad_output_dir / "workflow-status.yaml"

        if not status_file.exists():
            return None

        try:
            with open(status_file, 'r') as f:
                status = yaml.safe_load(f)
        except Exception as e:
            print(f"Error reading workflow status: {e}")
            return None

        # Check if design phase is complete
        design_phase = status.get('design_phase', {})

        if design_phase.get('status') == 'completed':
            return {
                "design_spec_path": design_phase.get('output'),
                "wireframes": design_phase.get('wireframes', []),
                "timestamp": design_phase.get('completed_at'),
                "design_phase": design_phase
            }

        return None

    def acknowledge_handoff(self, handoff_data: Dict) -> None:
        """
        Acknowledge receipt of design handoff
        Updates workflow status to indicate implementation has started

        Args:
            handoff_data: Handoff information from check_for_handoff()
        """
        status_file = self.bmad_output_dir / "workflow-status.yaml"

        # Load existing status
        try:
            with open(status_file, 'r') as f:
                status = yaml.safe_load(f) or {}
        except FileNotFoundError:
            status = {}

        # Update with implementation phase
        status['implementation_phase'] = {
            "status": "in_progress",
            "owner": "ui-engineering-agent",
            "started_at": datetime.now().isoformat(),
            "design_spec_source": handoff_data.get('design_spec_path'),
            "handoff_acknowledged": True
        }

        # Write back
        with open(status_file, 'w') as f:
            yaml.dump(status, f, default_flow_style=False)

        print(f"✅ Acknowledged handoff from UX Designer")
        print(f"   Design spec: {handoff_data.get('design_spec_path')}")

    def send_implementation_artifacts(self, artifacts: Dict) -> None:
        """
        Send implementation artifacts back to UX Designer

        Args:
            artifacts: Implementation results including prototype, Figma, etc.
        """
        # Create implementation review file
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        review_file = self.ui_engineering_dir / "reports" / f"review-{timestamp}.md"

        # Generate review report (if not already done)
        if 'review_report_path' not in artifacts:
            from tools.handoff_generator import HandoffReportGenerator
            generator = HandoffReportGenerator()

            generator.generate_implementation_review(
                data=artifacts,
                output_path=str(review_file)
            )
            artifacts['review_report_path'] = str(review_file)

        # Update workflow status
        self._update_workflow_status(artifacts)

        print(f"✅ Implementation artifacts sent to UX Designer")
        print(f"   Review report: {artifacts.get('review_report_path')}")

    def _update_workflow_status(self, artifacts: Dict) -> None:
        """Update workflow status with implementation results"""
        status_file = self.bmad_output_dir / "workflow-status.yaml"

        try:
            with open(status_file, 'r') as f:
                status = yaml.safe_load(f) or {}
        except FileNotFoundError:
            status = {}

        # Determine final status
        final_status = "awaiting_review"
        if artifacts.get('blockers'):
            final_status = "blocked"

        # Update implementation phase
        if 'implementation_phase' not in status:
            status['implementation_phase'] = {}

        status['implementation_phase'].update({
            "status": final_status,
            "completed_at": datetime.now().isoformat(),
            "workflow": artifacts.get('workflow', 'unknown'),
            "completeness_level": artifacts.get('completeness_level', 'unknown'),
            "artifacts": {
                "prototype": artifacts.get('prototype_path'),
                "figma": artifacts.get('figma_url'),
                "review_report": artifacts.get('review_report_path'),
                "accessibility_status": artifacts.get('accessibility_status')
            },
            "autonomous_decisions": len(artifacts.get('autonomous_decisions', [])),
            "blockers": artifacts.get('blockers', []),
            "recommendations": artifacts.get('recommendations', [])
        })

        # Write back
        with open(status_file, 'w') as f:
            yaml.dump(status, f, default_flow_style=False)

    def request_clarification(self, questions: List[str], context: Dict) -> None:
        """
        Request clarification from UX Designer

        Args:
            questions: List of questions needing clarification
            context: Context about the implementation
        """
        clarification_file = self.ui_engineering_dir / "clarification-needed.md"

        content = f"""# Clarification Needed

**From**: UI Engineering Agent
**To**: UX Designer Agent
**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Context

**Design Spec**: {context.get('design_spec', 'N/A')}
**Current Status**: {context.get('status', 'In progress')}
**Workflow**: {context.get('workflow', 'Unknown')}

## Questions

{self._format_questions(questions)}

---

**Impact**: Implementation is paused pending clarification.

**Please provide feedback so I can continue with implementation.**
"""

        with open(clarification_file, 'w') as f:
            f.write(content)

        # Update status
        status_file = self.bmad_output_dir / "workflow-status.yaml"
        try:
            with open(status_file, 'r') as f:
                status = yaml.safe_load(f) or {}
        except FileNotFoundError:
            status = {}

        if 'implementation_phase' not in status:
            status['implementation_phase'] = {}

        status['implementation_phase']['status'] = 'needs_clarification'
        status['implementation_phase']['clarification_file'] = str(clarification_file)
        status['implementation_phase']['questions_count'] = len(questions)

        with open(status_file, 'w') as f:
            yaml.dump(status, f, default_flow_style=False)

        print(f"⚠️ Clarification requested from UX Designer")
        print(f"   Questions: {len(questions)}")
        print(f"   File: {clarification_file}")

    def _format_questions(self, questions: List[str]) -> str:
        """Format questions as markdown list"""
        return "\n".join([f"{i+1}. {q}" for i, q in enumerate(questions)])

    def get_handoff_status(self) -> Dict:
        """
        Get current handoff status

        Returns:
            Status dictionary with current state
        """
        status_file = self.bmad_output_dir / "workflow-status.yaml"

        if not status_file.exists():
            return {
                "has_handoff": False,
                "status": "No workflow status file found"
            }

        try:
            with open(status_file, 'r') as f:
                status = yaml.safe_load(f) or {}
        except Exception as e:
            return {
                "has_handoff": False,
                "status": f"Error reading status: {e}"
            }

        design_phase = status.get('design_phase', {})
        impl_phase = status.get('implementation_phase', {})

        return {
            "has_handoff": design_phase.get('status') == 'completed',
            "design_status": design_phase.get('status'),
            "implementation_status": impl_phase.get('status'),
            "design_spec": design_phase.get('output'),
            "implementation_owner": impl_phase.get('owner'),
            "full_status": status
        }
