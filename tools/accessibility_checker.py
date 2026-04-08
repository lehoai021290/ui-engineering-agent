"""
Accessibility Checker

Validates UI implementation against WCAG 2.1 AA standards
"""

from pathlib import Path
from typing import Dict, List
import re


class AccessibilityChecker:
    """
    Check accessibility compliance for HTML prototypes
    """

    def __init__(self, wcag_level: str = "AA"):
        self.wcag_level = wcag_level

    def audit(self, html_file_path: str) -> Dict:
        """
        Perform accessibility audit on HTML file

        Args:
            html_file_path: Path to HTML file to audit

        Returns:
            Audit report with issues and recommendations
        """
        path = Path(html_file_path)

        if not path.exists():
            return {
                "status": "error",
                "message": f"File not found: {html_file_path}"
            }

        with open(path, 'r') as f:
            html_content = f.read()

        issues = []

        # Check for basic accessibility issues
        issues.extend(self._check_alt_text(html_content))
        issues.extend(self._check_labels(html_content))
        issues.extend(self._check_headings(html_content))
        issues.extend(self._check_aria(html_content))
        issues.extend(self._check_semantic_html(html_content))

        report = {
            "wcag_level": self.wcag_level,
            "file": str(path),
            "issues": issues,
            "issues_count": len(issues),
            "status": "✅ Passed" if len(issues) == 0 else f"⚠️ {len(issues)} issues found",
            "recommendations": self._generate_recommendations(issues)
        }

        return report

    def _check_alt_text(self, html: str) -> List[str]:
        """Check for missing alt text on images"""
        issues = []

        # Find img tags without alt attribute
        img_tags = re.findall(r'<img[^>]*>', html, re.IGNORECASE)
        for tag in img_tags:
            if 'alt=' not in tag.lower():
                issues.append("Image missing alt text")

        return issues

    def _check_labels(self, html: str) -> List[str]:
        """Check for form inputs without labels"""
        issues = []

        # Find input tags without associated labels
        input_tags = re.findall(r'<input[^>]*type=["\']?(text|email|password|number|tel)["\']?[^>]*>', html, re.IGNORECASE)

        # Simple check: if there are inputs but no labels, flag it
        label_count = len(re.findall(r'<label[^>]*>', html, re.IGNORECASE))

        if len(input_tags) > label_count:
            issues.append(f"Potential unlabeled form inputs ({len(input_tags)} inputs, {label_count} labels)")

        return issues

    def _check_headings(self, html: str) -> List[str]:
        """Check heading hierarchy"""
        issues = []

        # Check if h1 exists
        if not re.search(r'<h1[^>]*>', html, re.IGNORECASE):
            issues.append("Missing h1 heading (page should have one h1)")

        # Check for heading level skips (basic check)
        headings = re.findall(r'<h([1-6])[^>]*>', html, re.IGNORECASE)
        if headings:
            levels = [int(h) for h in headings]
            for i in range(len(levels) - 1):
                if levels[i+1] - levels[i] > 1:
                    issues.append(f"Heading hierarchy skip detected (h{levels[i]} to h{levels[i+1]})")
                    break

        return issues

    def _check_aria(self, html: str) -> List[str]:
        """Check for ARIA attributes where needed"""
        issues = []

        # Check for buttons without aria-label if text is not obvious
        buttons = re.findall(r'<button[^>]*>(.*?)</button>', html, re.IGNORECASE | re.DOTALL)
        for button_content in buttons:
            # If button has icon or image but no text or aria-label
            if re.search(r'<(img|svg|i class=)', button_content, re.IGNORECASE):
                if 'aria-label' not in button_content.lower():
                    issues.append("Icon button may need aria-label")
                    break

        return issues

    def _check_semantic_html(self, html: str) -> List[str]:
        """Check for semantic HTML usage"""
        issues = []

        # Check if semantic elements are used
        has_semantic = any([
            re.search(r'<(nav|header|main|footer|article|section)[^>]*>', html, re.IGNORECASE)
        ])

        # If HTML is substantial but has no semantic elements
        if len(html) > 1000 and not has_semantic:
            issues.append("Consider using semantic HTML elements (nav, header, main, footer, article, section)")

        return issues

    def _generate_recommendations(self, issues: List[str]) -> List[str]:
        """Generate recommendations based on issues"""
        recommendations = []

        if any('alt text' in issue.lower() for issue in issues):
            recommendations.append("Add descriptive alt text to all images")

        if any('label' in issue.lower() for issue in issues):
            recommendations.append("Ensure all form inputs have associated labels")

        if any('heading' in issue.lower() for issue in issues):
            recommendations.append("Follow proper heading hierarchy (h1 -> h2 -> h3, no skipping)")

        if any('aria' in issue.lower() for issue in issues):
            recommendations.append("Add aria-label to icon-only buttons and interactive elements")

        if any('semantic' in issue.lower() for issue in issues):
            recommendations.append("Use semantic HTML5 elements for better accessibility")

        if not recommendations:
            recommendations.append("Great job! No major accessibility issues detected.")

        return recommendations


# Standalone function for tool integration
def audit_accessibility(html_file_path: str, wcag_level: str = "AA") -> Dict:
    """
    Audit HTML file for accessibility compliance

    Args:
        html_file_path: Path to HTML file
        wcag_level: WCAG compliance level (A, AA, AAA)

    Returns:
        Accessibility audit report
    """
    checker = AccessibilityChecker(wcag_level=wcag_level)
    return checker.audit(html_file_path)
