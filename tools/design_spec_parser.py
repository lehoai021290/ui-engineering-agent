"""
Design Specification Parser with Input Flexibility

Handles multiple input formats:
- Full design handoff (wireframes + specs)
- Partial handoff (specs only)
- Requirements only (plain text)
- Direct user prompts (minimal input)
"""

import re
import yaml
import json
from pathlib import Path
from typing import Dict, List, Optional


class DesignSpecParser:
    """
    Parse design specifications from multiple input formats
    Handles: Full handoff, requirements-only, direct user input
    """

    def parse(self, input_source: str, input_type: str = "auto") -> dict:
        """
        Parse design input from various sources

        Args:
            input_source: File path, text requirements, or user prompt
            input_type: "auto", "markdown", "yaml", "json", "requirements", "prompt"

        Returns:
            Structured design specification dictionary
        """
        # Auto-detect input type
        if input_type == "auto":
            input_type = self._detect_input_type(input_source)

        if input_type == "markdown":
            return self._parse_markdown(Path(input_source))
        elif input_type == "yaml":
            return self._parse_yaml(Path(input_source))
        elif input_type == "json":
            return self._parse_json(Path(input_source))
        elif input_type == "requirements":
            return self._parse_requirements_text(input_source)
        elif input_type == "prompt":
            return self._parse_user_prompt(input_source)
        else:
            raise ValueError(f"Unknown input type: {input_type}")

    def _detect_input_type(self, input_source: str) -> str:
        """Auto-detect input type"""
        path = Path(input_source)

        # If it's a file path that exists
        if path.exists():
            if path.suffix == '.md':
                return "markdown"
            elif path.suffix in ['.yaml', '.yml']:
                return "yaml"
            elif path.suffix == '.json':
                return "json"

        # If it contains multiple lines, treat as requirements text
        if '\n' in input_source and len(input_source) > 100:
            return "requirements"

        # Otherwise, treat as user prompt
        return "prompt"

    def _parse_markdown(self, path: Path) -> dict:
        """Parse markdown design specification"""
        with open(path, 'r') as f:
            content = f.read()

        spec = {
            "source": str(path),
            "format": "markdown",
            "requirements": self._extract_requirements(content),
            "components": self._extract_components(content),
            "interactions": self._extract_interactions(content),
            "design_system_refs": self._extract_design_system_refs(content),
            "accessibility": self._extract_accessibility_reqs(content),
            "wireframe_refs": self._extract_wireframe_refs(content),
            "completeness": "complete" if self._has_wireframes(content) else "partial"
        }

        return spec

    def _parse_requirements_text(self, text: str) -> dict:
        """
        Parse plain text requirements
        Example: User story format, bullet points, or natural language
        """
        spec = {
            "source": "requirements_text",
            "format": "requirements",
            "requirements": [],
            "components": [],
            "interactions": [],
            "design_system_refs": {},
            "accessibility": {"wcag_level": "AA", "requirements": []},
            "wireframe_refs": [],
            "completeness": "minimal"
        }

        # Extract requirements from text
        lines = [line.strip() for line in text.split('\n') if line.strip()]

        for line in lines:
            # Bullet points or numbered lists
            if line.startswith(('-', '*', '•')) or (line[0].isdigit() and '. ' in line):
                cleaned = re.sub(r'^[-*•\d]+[.)\s]+', '', line)
                spec['requirements'].append(cleaned)
            else:
                spec['requirements'].append(line)

        # Try to infer components mentioned
        spec['components'] = self._infer_components_from_text(text)
        spec['interactions'] = self._infer_interactions_from_text(text)

        return spec

    def _parse_user_prompt(self, prompt: str) -> dict:
        """
        Parse direct user prompt (minimal input)
        Example: "Build a login page with email and password"
        """
        spec = {
            "source": "user_prompt",
            "format": "prompt",
            "requirements": [prompt],
            "components": self._infer_components_from_text(prompt),
            "interactions": self._infer_interactions_from_text(prompt),
            "design_system_refs": {},
            "accessibility": {"wcag_level": "AA", "requirements": []},
            "wireframe_refs": [],
            "completeness": "minimal",
            "needs_design_decisions": True
        }

        return spec

    def _extract_requirements(self, content: str) -> List[str]:
        """Extract requirements from markdown"""
        requirements = []

        # Look for "Requirements" or "User Flow" sections
        req_section = re.search(
            r'##\s*(?:Requirements?|User Flow|Acceptance Criteria)\s*\n(.*?)(?=\n##|\Z)',
            content,
            re.DOTALL | re.IGNORECASE
        )

        if req_section:
            # Extract bullet points or numbered lists
            items = re.findall(r'[-*•]\s+(.+)', req_section.group(1))
            requirements.extend(items)

        return requirements

    def _extract_components(self, content: str) -> List[Dict]:
        """Extract component requirements"""
        components = []

        comp_section = re.search(
            r'##\s*(?:Components?|Component Requirements?)\s*\n(.*?)(?=\n##|\Z)',
            content,
            re.DOTALL | re.IGNORECASE
        )

        if comp_section:
            # Extract component mentions with variants
            # Format: "- Use Button (variant: primary) for CTAs"
            comp_matches = re.findall(
                r'[-*•]\s+Use\s+(\w+)(?:\s*\(([^)]+)\))?\s+for\s+(.+)',
                comp_section.group(1),
                re.IGNORECASE
            )

            for comp_name, variants, usage in comp_matches:
                components.append({
                    "name": comp_name,
                    "variants": variants if variants else "default",
                    "usage": usage.strip()
                })

        # If no explicit components section, try to infer from content
        if not components:
            components = self._infer_components_from_text(content)

        return components

    def _extract_interactions(self, content: str) -> List[str]:
        """Extract interaction patterns"""
        interactions = []

        int_section = re.search(
            r'##\s*(?:Interactions?|Interaction Patterns?)\s*\n(.*?)(?=\n##|\Z)',
            content,
            re.DOTALL | re.IGNORECASE
        )

        if int_section:
            items = re.findall(r'[-*•]\s+(.+)', int_section.group(1))
            interactions.extend(items)

        # If no explicit interactions section, try to infer
        if not interactions:
            interactions = self._infer_interactions_from_text(content)

        return interactions

    def _extract_design_system_refs(self, content: str) -> Dict:
        """Extract design system references"""
        refs = {
            "components": [],
            "tokens": [],
            "guidelines": []
        }

        # Extract inline component references
        comp_refs = re.findall(r'`(\w+)`\s*component', content, re.IGNORECASE)
        refs["components"] = list(set(comp_refs))

        return refs

    def _extract_accessibility_reqs(self, content: str) -> Dict:
        """Extract accessibility requirements"""
        accessibility = {
            "wcag_level": "AA",  # Default
            "requirements": []
        }

        acc_section = re.search(
            r'##\s*Accessibility\s*\n(.*?)(?=\n##|\Z)',
            content,
            re.DOTALL | re.IGNORECASE
        )

        if acc_section:
            items = re.findall(r'[-*•]\s+(.+)', acc_section.group(1))
            accessibility["requirements"] = items

            # Check for WCAG level mention
            wcag_match = re.search(r'WCAG\s+\d+\.\d+\s+(A{1,3})', acc_section.group(1))
            if wcag_match:
                accessibility["wcag_level"] = wcag_match.group(1)

        return accessibility

    def _extract_wireframe_refs(self, content: str) -> List[Dict]:
        """Extract wireframe file references"""
        refs = []

        # Look for file paths or URLs
        file_refs = re.findall(r'\[([^\]]+)\]\(([^)]+\.excalidraw)\)', content)
        refs.extend([{"name": name, "path": path} for name, path in file_refs])

        # Also look for Figma links
        figma_refs = re.findall(r'\[([^\]]+)\]\((https://(?:www\.)?figma\.com/[^)]+)\)', content)
        refs.extend([{"name": name, "path": url} for name, url in figma_refs])

        return refs

    def _has_wireframes(self, content: str) -> bool:
        """Check if content references wireframes"""
        wireframe_indicators = [
            'wireframe', 'mockup', 'prototype', 'figma', 'excalidraw',
            '.fig', '.excalidraw'
        ]
        content_lower = content.lower()
        return any(indicator in content_lower for indicator in wireframe_indicators)

    def _infer_components_from_text(self, text: str) -> List[Dict]:
        """
        Infer UI components from natural language
        """
        components = []

        # Common component keywords
        component_keywords = {
            'button': {'name': 'Button', 'variants': 'default'},
            'input': {'name': 'Input', 'variants': 'default'},
            'text field': {'name': 'Input', 'variants': 'default'},
            'form': {'name': 'Form', 'variants': 'default'},
            'card': {'name': 'Card', 'variants': 'default'},
            'modal': {'name': 'Dialog', 'variants': 'default'},
            'dialog': {'name': 'Dialog', 'variants': 'default'},
            'popup': {'name': 'Dialog', 'variants': 'default'},
            'table': {'name': 'Table', 'variants': 'default'},
            'list': {'name': 'List', 'variants': 'default'},
            'nav': {'name': 'Navigation', 'variants': 'default'},
            'navigation': {'name': 'Navigation', 'variants': 'default'},
            'menu': {'name': 'Menu', 'variants': 'default'},
            'dropdown': {'name': 'Select', 'variants': 'default'},
            'select': {'name': 'Select', 'variants': 'default'},
            'checkbox': {'name': 'Checkbox', 'variants': 'default'},
            'radio': {'name': 'Radio', 'variants': 'default'},
            'toggle': {'name': 'Switch', 'variants': 'default'},
            'switch': {'name': 'Switch', 'variants': 'default'},
            'tab': {'name': 'Tabs', 'variants': 'default'},
            'accordion': {'name': 'Accordion', 'variants': 'default'},
            'badge': {'name': 'Badge', 'variants': 'default'},
            'avatar': {'name': 'Avatar', 'variants': 'default'},
            'alert': {'name': 'Alert', 'variants': 'default'},
            'notification': {'name': 'Alert', 'variants': 'default'},
        }

        text_lower = text.lower()
        seen_components = set()

        for keyword, comp_info in component_keywords.items():
            if keyword in text_lower:
                comp_key = comp_info['name']
                if comp_key not in seen_components:
                    components.append({
                        "name": comp_info['name'],
                        "variants": comp_info['variants'],
                        "usage": f"Inferred from text mention of '{keyword}'"
                    })
                    seen_components.add(comp_key)

        return components

    def _infer_interactions_from_text(self, text: str) -> List[str]:
        """
        Infer interaction patterns from natural language
        """
        interactions = []

        interaction_patterns = {
            'click': 'Click interaction',
            'submit': 'Form submission',
            'validate': 'Form validation',
            'hover': 'Hover state',
            'drag': 'Drag and drop',
            'scroll': 'Scroll interaction',
            'search': 'Search functionality',
            'filter': 'Filtering',
            'sort': 'Sorting',
            'expand': 'Expand/collapse interaction',
            'collapse': 'Expand/collapse interaction',
            'upload': 'File upload',
            'download': 'File download',
            'animation': 'Animated transitions',
            'transition': 'Animated transitions',
        }

        text_lower = text.lower()
        seen_interactions = set()

        for keyword, pattern in interaction_patterns.items():
            if keyword in text_lower and pattern not in seen_interactions:
                interactions.append(pattern)
                seen_interactions.add(pattern)

        return interactions

    def _parse_yaml(self, path: Path) -> dict:
        """Parse YAML design specification"""
        with open(path, 'r') as f:
            spec = yaml.safe_load(f)

        spec["source"] = str(path)
        spec["format"] = "yaml"

        # Ensure required fields exist
        if "completeness" not in spec:
            spec["completeness"] = "partial"

        return spec

    def _parse_json(self, path: Path) -> dict:
        """Parse JSON design specification"""
        with open(path, 'r') as f:
            spec = json.load(f)

        spec["source"] = str(path)
        spec["format"] = "json"

        # Ensure required fields exist
        if "completeness" not in spec:
            spec["completeness"] = "partial"

        return spec

    def assess_completeness(self, spec: dict) -> dict:
        """
        Assess completeness of design specification
        Determine if agent can proceed or needs more input
        """
        assessment = {
            "completeness_level": "unknown",
            "can_proceed": False,
            "missing_elements": [],
            "recommendations": [],
            "autonomous_decisions_needed": []
        }

        # Check what's available
        has_requirements = len(spec.get('requirements', [])) > 0
        has_components = len(spec.get('components', [])) > 0
        has_interactions = len(spec.get('interactions', [])) > 0
        has_wireframes = len(spec.get('wireframe_refs', [])) > 0
        has_design_system = bool(spec.get('design_system_refs', {}).get('components'))

        # Determine completeness level
        if has_wireframes and has_components and has_interactions:
            assessment['completeness_level'] = "complete"
            assessment['can_proceed'] = True
        elif has_requirements and has_components:
            assessment['completeness_level'] = "partial"
            assessment['can_proceed'] = True
            assessment['missing_elements'] = ['wireframes', 'detailed_interactions']
            assessment['recommendations'] = [
                "Generate layout structure from component specs",
                "Infer interaction patterns from component usage"
            ]
            assessment['autonomous_decisions_needed'] = [
                "Layout and spacing",
                "Component positioning",
                "Responsive behavior"
            ]
        elif has_requirements:
            assessment['completeness_level'] = "minimal"
            assessment['can_proceed'] = True
            assessment['missing_elements'] = ['components', 'wireframes', 'interactions', 'design_system']
            assessment['recommendations'] = [
                "Make autonomous design decisions based on best practices",
                "Generate complete prototype from requirements",
                "Consider consulting UX Designer for strategic decisions"
            ]
            assessment['autonomous_decisions_needed'] = [
                "Component selection",
                "Layout and spacing",
                "Interaction patterns",
                "Visual hierarchy",
                "Responsive breakpoints"
            ]
        else:
            assessment['completeness_level'] = "insufficient"
            assessment['can_proceed'] = False
            assessment['missing_elements'] = ['requirements']
            assessment['recommendations'] = [
                "Request user requirements or description",
                "Cannot proceed without minimal input"
            ]

        return assessment


# Standalone function for tool integration
def parse_spec(input_source: str, input_type: str = "auto") -> dict:
    """
    Parse design specification file or text

    Args:
        input_source: File path, requirements text, or user prompt
        input_type: "auto", "markdown", "yaml", "json", "requirements", "prompt"

    Returns:
        Structured design specification dictionary
    """
    parser = DesignSpecParser()
    return parser.parse(input_source, input_type)
