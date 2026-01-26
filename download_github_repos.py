#!/usr/bin/env python3
"""
Script to download all repositories from a GitHub account.

Usage:
    python download_github_repos.py <github_username> [--token YOUR_GITHUB_TOKEN] [--output-dir ./repos]

Requirements:
    pip install requests
    
Optional:
    - GitHub Personal Access Token (for higher rate limits and private repos)
    - Create token at: https://github.com/settings/tokens
"""

import os
import sys
import subprocess
import requests
from pathlib import Path
from typing import List, Dict
import argparse


class GitHubDownloader:
    def __init__(self, username: str, token: str = None, output_dir: str = "./repos"):
        """
        Initialize GitHub downloader.
        
        Args:
            username: GitHub username
            token: GitHub Personal Access Token (optional)
            output_dir: Directory to download repositories to
        """
        self.username = username
        self.token = token
        self.output_dir = Path(output_dir)
        self.api_base = "https://api.github.com"
        self.headers = self._get_headers()
        
    def _get_headers(self) -> Dict:
        """Get request headers with authentication if token provided."""
        headers = {"Accept": "application/vnd.github.v3+json"}
        if self.token:
            headers["Authorization"] = f"token {self.token}"
        return headers
    
    def get_repositories(self) -> List[Dict]:
        """
        Fetch all repositories for the user.
        
        Returns:
            List of repository dictionaries
        """
        repos = []
        page = 1
        per_page = 100
        
        while True:
            url = f"{self.api_base}/users/{self.username}/repos"
            params = {
                "per_page": per_page,
                "page": page,
                "sort": "updated",
                "direction": "desc"
            }
            
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            if not data:
                break
            
            repos.extend(data)
            page += 1
            
            # Check if we've got all repos (GitHub returns empty list when no more pages)
            if len(data) < per_page:
                break
        
        return repos
    
    def create_output_directory(self):
        """Create output directory if it doesn't exist."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        print(f"✓ Output directory: {self.output_dir.absolute()}")
    
    def clone_repository(self, repo: Dict) -> bool:
        """
        Clone a single repository.
        
        Args:
            repo: Repository information dictionary
            
        Returns:
            True if successful, False otherwise
        """
        repo_name = repo["name"]
        clone_url = repo["clone_url"]
        repo_path = self.output_dir / repo_name
        
        # Skip if already exists
        if repo_path.exists():
            print(f"⊘ {repo_name} (already exists)")
            return True
        
        try:
            print(f"⋯ Cloning {repo_name}...", end=" ", flush=True)
            subprocess.run(
                ["git", "clone", "--depth", "1", clone_url, str(repo_path)],
                capture_output=True,
                check=True,
                timeout=300
            )
            print("✓")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ (Error: {e.stderr.decode().strip()})")
            return False
        except FileNotFoundError:
            print("✗ (git not found - install git to clone repositories)")
            return False
        except subprocess.TimeoutExpired:
            print("✗ (Timeout)")
            return False
        except Exception as e:
            print(f"✗ ({str(e)})")
            return False
    
    def download_all(self) -> None:
        """Download all repositories for the user."""
        print(f"GitHub Username: {self.username}")
        print(f"Using authentication: {'Yes' if self.token else 'No'}")
        print()
        
        # Create output directory
        self.create_output_directory()
        
        # Fetch repositories
        print("Fetching repositories...", end=" ", flush=True)
        try:
            repos = self.get_repositories()
            print(f"✓ Found {len(repos)} repositories\n")
        except requests.exceptions.HTTPError as e:
            print(f"\n✗ Error fetching repositories: {e}")
            sys.exit(1)
        
        if not repos:
            print("No repositories found.")
            return
        
        # Clone repositories
        print("Cloning repositories:")
        print("-" * 50)
        
        successful = 0
        failed = 0
        
        for i, repo in enumerate(repos, 1):
            if self.clone_repository(repo):
                successful += 1
            else:
                failed += 1
        
        # Print summary
        print("-" * 50)
        print(f"\nDownload Summary:")
        print(f"  Total: {len(repos)}")
        print(f"  Successful: {successful}")
        print(f"  Failed: {failed}")
        print(f"  Already existing: {len(repos) - successful - failed}")
        print(f"\nRepositories saved to: {self.output_dir.absolute()}")


def main():
    parser = argparse.ArgumentParser(
        description="Download all repositories from a GitHub account",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Download public repositories
  python download_github_repos.py username
  
  # Download with authentication (includes private repos)
  python download_github_repos.py username --token ghp_xxxxx
  
  # Specify custom output directory
  python download_github_repos.py username --output-dir /path/to/repos
        """
    )
    
    parser.add_argument("username", help="GitHub username")
    parser.add_argument(
        "--token",
        help="GitHub Personal Access Token (optional, for higher rate limits)",
        default=None
    )
    parser.add_argument(
        "--output-dir",
        default="./repos",
        help="Directory to download repositories to (default: ./repos)"
    )
    
    args = parser.parse_args()
    
    # Create downloader and download repos
    downloader = GitHubDownloader(
        username=args.username,
        token=args.token,
        output_dir=args.output_dir
    )
    
    downloader.download_all()


if __name__ == "__main__":
    main()
