import os
import sys
import json
import openai
from pathlib import Path
from typing import List, Dict
import requests
from dotenv import load_dotenv

load_dotenv()

# GitHub API setup
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_REPOSITORY = os.getenv('GITHUB_REPOSITORY')
GITHUB_PR_NUMBER = os.getenv('GITHUB_PR_NUMBER')

def get_pr_diff() -> str:
    """Get the diff of the PR from GitHub API."""
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3.diff'
    }
    url = f'https://api.github.com/repos/{GITHUB_REPOSITORY}/pulls/{GITHUB_PR_NUMBER}'
    response = requests.get(url, headers=headers)
    return response.text

def get_rules() -> List[Dict]:
    """Read all markdown files from .ai-code-rules directory."""
    rules = []
    rules_dir = Path('.ai-code-rules')
    
    if not rules_dir.exists():
        return rules
        
    for rule_file in rules_dir.glob('*.md'):
        with open(rule_file, 'r') as f:
            content = f.read()
            rules.append({
                'file': str(rule_file),
                'content': content
            })
    return rules

def analyze_code_with_ai(diff: str, rules: List[Dict]) -> List[Dict]:
    """Use OpenAI to analyze the code against the rules."""
    openai.api_key = os.getenv('OPENAI_API_KEY')
    
    annotations = []
    for rule in rules:
        prompt = f"""
        Analyze the following code changes against this rule:
        
        Rule from {rule['file']}:
        {rule['content']}
        
        Code changes:
        {diff}
        
        For each line that violates this rule:
        1. Identify the file and line number
        2. Explain why it violates the rule
        3. Suggest a fix
        
        Format the response as JSON with the following structure:
        {{
            "violations": [
                {{
                    "file": "path/to/file",
                    "line": 123,
                    "explanation": "Why this violates the rule",
                    "suggestion": "How to fix it"
                }}
            ]
        }}
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a code review assistant that helps identify code that violates specific rules."},
                {"role": "user", "content": prompt}
            ]
        )
        
        try:
            result = json.loads(response.choices[0].message.content)
            for violation in result.get('violations', []):
                violation['rule_file'] = rule['file']
                annotations.append(violation)
        except json.JSONDecodeError:
            print("Failed to parse AI response as JSON")
    
    return annotations

def create_github_annotation(annotation: Dict):
    """Create a GitHub annotation for the violation."""
    print(f"::warning file={annotation['file']},line={annotation['line']}::"
          f"{annotation['explanation']}\n\n"
          f"Suggestion: {annotation['suggestion']}\n"
          f"Rule source: {annotation['rule_file']}")

def main():
    diff = get_pr_diff()
    rules = get_rules()
    
    if not rules:
        print("No rules found in .ai-code-rules directory")
        return
    
    annotations = analyze_code_with_ai(diff, rules)
    
    for annotation in annotations:
        create_github_annotation(annotation)

if __name__ == "__main__":
    main() 