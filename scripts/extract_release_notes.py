import subprocess
import argparse
import os
from typing import List
from datetime import datetime


def get_commits(repo_path: str) -> List[str]:
    """
    Get the commit logs from develop that are not in main.
    Exclude merge commits starting with 'Merge'.
    """
    cmd = [
        "git",
        "log",
        "main..develop",
        "--pretty=format:%s|%an|%ad",
        "--date=short",
        "--no-merges"
    ]
    result = subprocess.run(cmd, cwd=repo_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Git error: {result.stderr.strip()}")

    return result.stdout.strip().splitlines()


def format_commit_message(commit_line: str, repo_path: str, include_date: bool = False, include_author: bool = False) -> str:
    """
    Format a commit message with optional metadata.
    """
    parts = commit_line.split("|")
    if len(parts) < 3:
        return ""

    message = parts[0]
    author = parts[1]
    date = parts[2]

    message_block = f"- **{message}**"
    if include_date:
        message_block += f"\n  - Date: {date}"
    if include_author:
        message_block += f"\n  - Author: {author}"
    
    return message_block


def generate_release_notes(repo_path: str, format: str = "markdown", include_date: bool = False, include_author: bool = False) -> str:
    commits = get_commits(repo_path)
    if not commits:
        return "No new commits found between main and develop."

    messages = []
    for commit in commits:
        if not commit:
            continue
        formatted = format_commit_message(commit, repo_path, include_date, include_author)
        messages.append(formatted)

    return "\n\n".join(messages)


def get_output_path(output_file: str = None) -> str:
    """
    Generate the output file path, creating the outputs directory if needed.
    """
    # Create outputs directory if it doesn't exist
    outputs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "outputs")
    os.makedirs(outputs_dir, exist_ok=True)

    if output_file:
        # If output_file is provided, use it (with or without .md extension)
        if not output_file.endswith('.md'):
            output_file += '.md'
        return os.path.join(outputs_dir, output_file)
    else:
        # Generate default filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(outputs_dir, f"release_notes_{timestamp}.md")


def main():
    parser = argparse.ArgumentParser(description="Generate release notes from develop to main.")
    parser.add_argument("repo", help="Path to the local Git repository")
    parser.add_argument("--format", choices=["markdown", "plaintext"], default="markdown")
    parser.add_argument("--output", help="Optional output file name (will be saved in outputs directory)")
    parser.add_argument("--include-date", action="store_true", help="Include commit dates in the output")
    parser.add_argument("--include-author", action="store_true", help="Include author names in the output")
    args = parser.parse_args()

    if not os.path.exists(args.repo):
        print("❌ Repo path does not exist.")
        return

    try:
        release_notes = generate_release_notes(args.repo, args.format, args.include_date, args.include_author)
        print("\n=== RELEASE NOTES ===\n")
        print(release_notes)

        # Always save to file
        output_path = get_output_path(args.output)
        with open(output_path, "w") as f:
            f.write(release_notes)
        print(f"\n✅ Saved to {output_path}")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
