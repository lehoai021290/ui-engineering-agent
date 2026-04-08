"""
Workflow Orchestrator for UI Engineering Agent

Manages different collaboration workflows and execution modes
Refactored to call skills directly without CrewAI dependency
"""

from bmad_integration import BMADIntegration
from skills.figma_ui_generation import generate_figma_design
from skills.web_prototype_generation import generate_prototype
from tools.design_spec_parser import DesignSpecParser
import time
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime


class WorkflowOrchestrator:
    """
    Orchestrate different collaboration workflows
    Supports watch mode, manual execution, and various workflow patterns

    Directly calls skills without intermediate agent layer
    """

    def __init__(self):
        self.bmad = BMADIntegration()
        self.parser = DesignSpecParser()

    def _execute_design_workflow(self, design_spec_path: str) -> Dict:
        """
        Execute the complete design-to-code workflow
        Generates web prototype and Figma UI from design spec

        Args:
            design_spec_path: Path to design specification file

        Returns:
            Workflow execution results with paths and status
        """
        result = {
            "status": "in_progress",
            "workflow": "auto",
            "timestamp": datetime.now().isoformat()
        }

        try:
            # Step 1: Parse design specification
            print("📋 Parsing design specification...")
            spec = self.parser.parse(design_spec_path)
            result["design_spec"] = spec

            # Step 2: Generate web prototype
            print("🌐 Generating web prototype...")
            prototype_result = generate_prototype(spec)

            if prototype_result["status"] == "success":
                result["prototype_path"] = prototype_result.get("html_path")
                result["prototype_url"] = prototype_result.get("url")
                print(f"   ✅ Prototype: {result['prototype_path']}")
            else:
                raise Exception(f"Prototype generation failed: {prototype_result.get('message')}")

            # Step 3: Generate Figma UI from prototype
            print("🎨 Generating Figma UI...")
            figma_result = generate_figma_design(
                html_path=result["prototype_path"],
                design_spec=spec
            )

            if figma_result["status"] == "success":
                result["figma_url"] = figma_result.get("file_url")
                result["figma_file_key"] = figma_result.get("file_key")
                result["component_node_ids"] = figma_result.get("component_node_ids", [])
                print(f"   ✅ Figma: {result['figma_url']}")
            else:
                raise Exception(f"Figma generation failed: {figma_result.get('message')}")

            # Step 4: Generate review report (placeholder)
            result["review_report_path"] = str(Path(design_spec_path).parent / "implementation_review.md")

            result["status"] = "success"
            print("✅ Workflow completed successfully!")

        except Exception as e:
            result["status"] = "error"
            result["message"] = str(e)
            print(f"❌ Workflow failed: {e}")

        return result

    def watch_for_handoff(self, interval: int = 30, max_iterations: Optional[int] = None):
        """
        Watch for design handoff from BMAD UX Designer
        Poll-based approach (can be replaced with file watcher)

        Args:
            interval: Polling interval in seconds
            max_iterations: Maximum number of polls (None = infinite)
        """
        print("🔍 Watching for design handoff from UX Designer...")
        print(f"   Polling every {interval} seconds")
        print(f"   Monitoring: {self.bmad.bmad_output_dir}")
        print()

        iteration = 0

        while True:
            iteration += 1

            if max_iterations and iteration > max_iterations:
                print(f"Maximum iterations ({max_iterations}) reached. Stopping.")
                break

            # Check for handoff
            handoff = self.bmad.check_for_handoff()

            if handoff:
                print(f"✅ Design handoff received!")
                print(f"   Design spec: {handoff['design_spec_path']}")
                print(f"   Timestamp: {handoff.get('timestamp', 'N/A')}")
                print()

                # Acknowledge handoff
                self.bmad.acknowledge_handoff(handoff)

                # Execute workflow
                print("🚀 Starting implementation workflow...")
                try:
                    result = self._execute_design_workflow(handoff['design_spec_path'])

                    # Send artifacts back to UX Designer
                    self.bmad.send_implementation_artifacts(result)

                    print()
                    print("=" * 60)
                    print("✅ Implementation complete!")
                    print(f"   Workflow: {result.get('workflow', 'unknown')}")
                    print(f"   Status: {result.get('status', 'unknown')}")
                    print(f"   Prototype: {result.get('prototype_path', 'N/A')}")
                    print(f"   Figma: {result.get('figma_url', 'N/A')}")
                    print(f"   Review: {result.get('review_report_path', 'N/A')}")
                    print("=" * 60)
                    print()

                    # Continue watching for next handoff
                    print("🔍 Continuing to watch for next handoff...")

                except Exception as e:
                    print(f"❌ Error during workflow execution: {e}")
                    import traceback
                    traceback.print_exc()

            else:
                # No handoff yet
                if iteration == 1:
                    print("No handoff detected yet. Waiting...")
                elif iteration % 10 == 0:
                    print(f"Still watching... ({iteration} checks)")

            time.sleep(interval)

    def manual_execution(self, design_spec_path: str) -> Dict:
        """
        Manually execute workflow with specific design spec

        Args:
            design_spec_path: Path to design specification file

        Returns:
            Workflow execution results
        """
        print(f"🚀 Manual execution: {design_spec_path}")
        print()

        # Check if file exists
        if not Path(design_spec_path).exists():
            print(f"❌ Error: File not found: {design_spec_path}")
            return {
                "status": "error",
                "message": f"File not found: {design_spec_path}"
            }

        # Execute workflow
        try:
            result = self._execute_design_workflow(design_spec_path)

            # Send artifacts to BMAD
            self.bmad.send_implementation_artifacts(result)

            print()
            print("=" * 60)
            print("✅ Implementation complete!")
            print(f"   Workflow: {result.get('workflow', 'unknown')}")
            print(f"   Status: {result.get('status', 'unknown')}")
            print(f"   Prototype: {result.get('prototype_path', 'N/A')}")
            print(f"   Figma: {result.get('figma_url', 'N/A')}")
            print(f"   Review: {result.get('review_report_path', 'N/A')}")
            print("=" * 60)

            return result

        except Exception as e:
            print(f"❌ Error during execution: {e}")
            import traceback
            traceback.print_exc()
            return {
                "status": "error",
                "message": str(e)
            }

    def quick_generate(self, user_prompt: str) -> Dict:
        """
        Quick generation from user prompt
        No BMAD integration, just generate directly

        Args:
            user_prompt: User description or requirements

        Returns:
            Generation results
        """
        print(f"⚡ Quick generation: {user_prompt}")
        print()

        result = {
            "status": "in_progress",
            "workflow": "quick",
            "timestamp": datetime.now().isoformat()
        }

        try:
            # Convert prompt to minimal spec
            minimal_spec = {
                "format": "prompt",
                "source": "user_input",
                "prompt": user_prompt,
                "requirements": [user_prompt]
            }

            # Generate web prototype from prompt
            print("🌐 Generating web prototype...")
            prototype_result = generate_prototype(minimal_spec)

            if prototype_result["status"] == "success":
                result["prototype_path"] = prototype_result.get("html_path")
                result["prototype_url"] = prototype_result.get("url")
                print(f"   ✅ Prototype: {result['prototype_path']}")

                # Generate Figma UI from prototype
                print("🎨 Generating Figma UI...")
                figma_result = generate_figma_design(
                    html_path=result["prototype_path"],
                    design_spec=minimal_spec
                )

                if figma_result["status"] == "success":
                    result["figma_url"] = figma_result.get("file_url")
                    result["figma_file_key"] = figma_result.get("file_key")
                    print(f"   ✅ Figma: {result['figma_url']}")
                else:
                    print(f"   ⚠️  Figma generation failed: {figma_result.get('message')}")

                result["status"] = "success"
            else:
                raise Exception(f"Prototype generation failed: {prototype_result.get('message')}")

            print()
            print("=" * 60)
            print("✅ Generation complete!")
            print(f"   Workflow: {result.get('workflow', 'unknown')}")
            print(f"   Prototype: {result.get('prototype_path', 'N/A')}")
            print(f"   Figma: {result.get('figma_url', 'N/A')}")
            print("=" * 60)

            return result

        except Exception as e:
            print(f"❌ Error during generation: {e}")
            import traceback
            traceback.print_exc()
            return {
                "status": "error",
                "message": str(e)
            }

    def status(self) -> Dict:
        """
        Check current workflow status

        Returns:
            Current status information
        """
        status = self.bmad.get_handoff_status()

        print("📊 Current Workflow Status")
        print("=" * 60)
        print(f"   Has Handoff: {status.get('has_handoff', False)}")
        print(f"   Design Status: {status.get('design_status', 'N/A')}")
        print(f"   Implementation Status: {status.get('implementation_status', 'N/A')}")
        print(f"   Design Spec: {status.get('design_spec', 'N/A')}")
        print(f"   Owner: {status.get('implementation_owner', 'N/A')}")
        print("=" * 60)

        return status

    def request_clarification(self, questions: list, context: dict = None):
        """
        Request clarification from UX Designer

        Args:
            questions: List of questions
            context: Optional context information
        """
        if context is None:
            context = {
                "design_spec": "Current implementation",
                "status": "In progress",
                "workflow": "Manual"
            }

        self.bmad.request_clarification(questions, context)

        print("✅ Clarification request sent to UX Designer")


# CLI interface
if __name__ == "__main__":
    import sys

    orchestrator = WorkflowOrchestrator()

    if len(sys.argv) < 2:
        print("UI Engineering Agent - Workflow Orchestrator")
        print()
        print("Usage:")
        print("  python orchestrator.py watch              # Watch for BMAD handoffs")
        print("  python orchestrator.py implement <path>   # Manual implementation")
        print("  python orchestrator.py generate <prompt>  # Quick generation")
        print("  python orchestrator.py status             # Check status")
        print()
        print("Examples:")
        print("  python orchestrator.py watch")
        print("  python orchestrator.py implement _bmad-output/ux-design/login-flow.md")
        print("  python orchestrator.py generate 'Build a product dashboard'")
        print("  python orchestrator.py status")
        sys.exit(0)

    command = sys.argv[1].lower()

    if command == "watch":
        # Watch mode
        interval = 30
        if len(sys.argv) > 2:
            try:
                interval = int(sys.argv[2])
            except ValueError:
                print(f"Invalid interval: {sys.argv[2]}, using default 30s")

        orchestrator.watch_for_handoff(interval=interval)

    elif command == "implement":
        # Manual implementation
        if len(sys.argv) < 3:
            print("Error: Please provide design spec path")
            print("Usage: python orchestrator.py implement <path>")
            sys.exit(1)

        design_spec_path = sys.argv[2]
        orchestrator.manual_execution(design_spec_path)

    elif command == "generate":
        # Quick generation
        if len(sys.argv) < 3:
            print("Error: Please provide user prompt")
            print("Usage: python orchestrator.py generate '<prompt>'")
            sys.exit(1)

        user_prompt = " ".join(sys.argv[2:])
        orchestrator.quick_generate(user_prompt)

    elif command == "status":
        # Check status
        orchestrator.status()

    else:
        print(f"Unknown command: {command}")
        print("Run without arguments to see usage")
        sys.exit(1)
