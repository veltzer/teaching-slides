#!/usr/bin/env python

"""
This script checks md files
"""

import re
import os
import sys
from pathlib import Path
from typing import List, Tuple, Dict
import argparse

class MarkdownLinkChecker:
    """
    This class does most of the lifting
    """
    def __init__(self, base_path: Path=Path(".")):
        """
        Initialize the link checker with an optional base path for relative links.

        Args:
            base_path (Path): Base directory path for resolving relative links
        """
        self.base_path = base_path or Path.cwd()
        # Regular expression for matching markdown links
        self.link_pattern = re.compile(r'^\[([^\]]+)\]\(([^)]+)\)')

    def is_local_link(self, link: str) -> bool:
        """
        Check if a link is local (not web URL).

        Args:
            link (str): The link to check

        Returns:
            bool: True if link is local, False otherwise
        """
        return not (link.startswith('http://') or
                   link.startswith('https://') or
                   link.startswith('ftp://') or
                   link.startswith('mailto:'))

    def validate_link(self, link: str, file_path: Path) -> bool:
        """
        Validate if a local link points to an existing file.

        Args:
            link (str): The link to validate
            file_path (Path): Path of the markdown file containing the link

        Returns:
            bool: True if link is valid, False otherwise
        """
        # Remove anchor tags from links
        link = link.split('#')[0]
        if not link:  # Empty link after removing anchor
            return True

        # Handle absolute and relative paths
        if os.path.isabs(link):
            target_path = Path(link)
        else:
            # Resolve relative to the markdown file's location
            target_path = (file_path.parent / link).resolve()

        return target_path.exists()

    def remove_code_blocks(self, content: str) -> str:
        """
        Remove code blocks from markdown content.

        Args:
            content (str): Original markdown content

        Returns:
            str: Content with code blocks removed
        """
        # Remove code blocks with triple backticks
        return re.sub(r'```[^`]*```', '', content, flags=re.DOTALL)

    def check_file(self, file_path: Path) -> List[Tuple[str, str, bool]]:
        """
        Check all local links in a markdown file.

        Args:
            file_path (Path): Path to the markdown file

        Returns:
            List[Tuple[str, str, bool]]: List of (link_text, link_target, is_valid) tuples
        """
        results = []
        content = file_path.read_text(encoding='utf-8')
        # Remove code blocks before checking links
        content = self.remove_code_blocks(content)
        matches = self.link_pattern.finditer(content)

        for match in matches:
            text, link = match.groups()
            if self.is_local_link(link):
                is_valid = self.validate_link(link, file_path)
                results.append((text, link, is_valid))
        return results

    def check_directory(self, directory: Path) -> Dict[Path, List[Tuple[str, str, bool]]]:
        """
        Check all markdown files in a directory.

        Args:
            directory (Path): Directory path to check

        Returns:
            Dict[Path, List[Tuple[str, str, bool]]]: Dictionary mapping files to
            their link check results
        """
        results = {}
        for md_file in directory.rglob('*.md'):
            results[md_file] = self.check_file(md_file)
        return results

def main():
    """ main entry point """
    parser = argparse.ArgumentParser(description='Validate local links in markdown files')
    parser.add_argument('paths', nargs='+', help='Markdown files or directories to check')
    parser.add_argument('--quiet', '-q', action='store_true', help='Only show invalid links')
    args = parser.parse_args()

    checker = MarkdownLinkChecker()
    exit_code = 0

    for path_str in args.paths:
        path = Path(path_str)
        if path.is_file():
            results = {path: checker.check_file(path)}
        elif path.is_dir():
            results = checker.check_directory(path)
        else:
            print(f"Error: Path not found: {path}", file=sys.stderr)
            exit_code = 1
            continue

        # Print results
        for file_path, file_results in results.items():
            if file_results:
                if not args.quiet:
                    print(f"\nChecking {file_path}:")
                for text, link, is_valid in file_results:
                    if not args.quiet and is_valid:
                        status = "✓" if is_valid else "✗"
                        print(f"{status} [{text}]({link})", file=sys.stdout)
                    if not is_valid:
                        status = "✓" if is_valid else "✗"
                        print(f"{status} [{text}]({link})", file=sys.stderr)
                        exit_code = 1

    sys.exit(exit_code)

if __name__ == '__main__':
    main()
