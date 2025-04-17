import os
import json
from openai import OpenAI
from pathlib import Path
from typing import Dict, List
import requests
from dotenv import load_dotenv

load_dotenv()

# GitHub API setup
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_REPOSITORY = os.getenv('GITHUB_REPOSITORY')
GITHUB_PR_NUMBER = os.getenv('GITHUB_PR_NUMBER')

def get_uncovered_lines() -> Dict[str, List[int]]:
    """Get uncovered lines from coverage.json."""
    with open('coverage.json', 'r') as f:
        coverage_data = json.load(f)
    
    uncovered = {}
    for file_path, file_data in coverage_data['files'].items():
        missing_lines = file_data['missing_lines']
        if missing_lines:
            uncovered[file_path] = missing_lines
    return uncovered

def get_file_content(file_path: str) -> str:
    """Get the content of a file."""
    with open(file_path, 'r') as f:
        return f.read()

def generate_test_with_ai(file_path: str, lines: List[int], content: str) -> str:
    """Use OpenAI to generate tests for uncovered lines."""
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    prompt = f"""
    Generate a test for the following code. The test should cover lines {lines} in the file {file_path}.
    
    Code:
    {content}
    
    Requirements:
    1. The test should be in pytest format
    2. Include necessary imports
    3. Include docstrings explaining the test
    4. Cover all edge cases
    5. Use meaningful test names
    
    Return only the test code, no explanations.
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a test writing assistant that generates comprehensive test cases."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content

def create_test_file(file_path: str, test_content: str):
    """Create a test file for the given file path."""
    test_dir = Path('tests')
    test_dir.mkdir(exist_ok=True)
    
    test_file = test_dir / f"test_{Path(file_path).stem}.py"
    with open(test_file, 'w') as f:
        f.write(test_content)

def create_github_comment(file_path: str, lines: List[int], test_content: str):
    """Create a GitHub comment with the test suggestion."""
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    url = f'https://api.github.com/repos/{GITHUB_REPOSITORY}/issues/{GITHUB_PR_NUMBER}/comments'
    
    comment = f"""
    Lines {lines} in {file_path} are not covered by tests. Here's a suggested test:

    ```python
    {test_content}
    ```
    """
    
    data = {
        'body': comment
    }
    
    requests.post(url, headers=headers, json=data)

def main():
    uncovered = get_uncovered_lines()
    
    for file_path, lines in uncovered.items():
        try:
            content = get_file_content(file_path)
            test_content = generate_test_with_ai(file_path, lines, content)
            
            # Try to create a test file
            try:
                create_test_file(file_path, test_content)
                print(f"Created test file for {file_path}")
            except Exception as e:
                print(f"Could not create test file: {e}")
                # If we can't create the test file, create a comment instead
                create_github_comment(file_path, lines, test_content)
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

if __name__ == "__main__":
    main() 