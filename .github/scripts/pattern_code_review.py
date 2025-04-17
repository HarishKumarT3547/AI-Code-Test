import os
import re
from pathlib import Path
from typing import List, Dict, Tuple
import requests
import difflib
from dataclasses import dataclass

@dataclass
class CodePattern:
    name: str
    pattern: str
    description: str
    suggestion: str
    severity: str = "warning"

class PatternAnalyzer:
    def __init__(self):
        self.patterns = self._load_patterns()

    def _load_patterns(self) -> List[CodePattern]:
        patterns = []
        rules_dir = Path('.ai-code-rules')
        
        if not rules_dir.exists():
            return patterns
            
        for rule_file in rules_dir.glob('*.md'):
            with open(rule_file, 'r') as f:
                content = f.read()
                # Extract patterns from markdown files
                # Format: ```pattern
                # PATTERN_REGEX
                # ```
                pattern_blocks = re.findall(r'```pattern\n(.*?)\n```', content, re.DOTALL)
                for block in pattern_blocks:
                    lines = block.strip().split('\n')
                    if len(lines) >= 3:
                        name = lines[0]
                        pattern = lines[1]
                        description = lines[2]
                        suggestion = '\n'.join(lines[3:]) if len(lines) > 3 else ""
                        patterns.append(CodePattern(
                            name=name,
                            pattern=pattern,
                            description=description,
                            suggestion=suggestion
                        ))
        return patterns

    def analyze_diff(self, diff: str) -> List[Dict]:
        violations = []
        current_file = None
        line_number = 0

        for line in diff.split('\n'):
            # Track file changes
            if line.startswith('+++ b/'):
                current_file = line[6:]
                continue

            # Track line numbers
            if line.startswith('@@'):
                match = re.match(r'@@ -\d+,\d+ \+(\d+),\d+ @@', line)
                if match:
                    line_number = int(match.group(1))
                continue

            # Only analyze added lines
            if line.startswith('+') and not line.startswith('+++'):
                line_content = line[1:]
                for pattern in self.patterns:
                    if re.search(pattern.pattern, line_content):
                        violations.append({
                            'file': current_file,
                            'line': line_number,
                            'pattern': pattern.name,
                            'description': pattern.description,
                            'suggestion': pattern.suggestion,
                            'severity': pattern.severity
                        })
            line_number += 1

        return violations

def get_pr_diff() -> str:
    """Get the diff of the PR from GitHub API."""
    token = os.getenv('GITHUB_TOKEN')
    repo = os.getenv('GITHUB_REPOSITORY')
    pr_number = os.getenv('GITHUB_PR_NUMBER')

    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3.diff'
    }
    url = f'https://api.github.com/repos/{repo}/pulls/{pr_number}'
    response = requests.get(url, headers=headers)
    return response.text

def create_github_annotation(violation: Dict):
    """Create a GitHub annotation for the violation."""
    print(f"::{violation['severity']} file={violation['file']},line={violation['line']}::"
          f"{violation['description']}\n\n"
          f"Suggestion: {violation['suggestion']}")

def main():
    analyzer = PatternAnalyzer()
    diff = get_pr_diff()
    violations = analyzer.analyze_diff(diff)
    
    for violation in violations:
        create_github_annotation(violation)

if __name__ == "__main__":
    main() 