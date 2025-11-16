"""
GitHub Client Module
Wrapper around GitHub REST API for issue and project operations.
"""

import logging
import os
from typing import Dict, List, Optional, Any
import requests
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()


class GitHubClient:
    """GitHub API client for creating and managing issues."""
    
    API_BASE_URL = os.getenv('GITHUB_API_URL', 'https://api.github.com')
    TOKEN = os.getenv('GITHUB_TOKEN')
    ORG = os.getenv('GITHUB_ORG', 'nimeshe')
    
    def __init__(self, token: str = None, org: str = None):
        """
        Initialize GitHub client.
        
        Args:
            token: GitHub personal access token
            org: GitHub organization
        """
        self.token = token or self.TOKEN
        self.org = org or self.ORG
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Accept': 'application/vnd.github.v3+json',
            'X-GitHub-Api-Version': '2022-11-28'
        }
    
    def create_issue(self, repo: str, title: str, body: str, 
                    labels: List[str] = None, assignee: str = None,
                    milestone: str = None) -> Optional[Dict[str, Any]]:
        """
        Create a new issue in a repository.
        
        Args:
            repo: Repository name
            title: Issue title
            body: Issue body/description
            labels: List of label names
            assignee: GitHub username to assign
            milestone: Milestone name
            
        Returns:
            Issue dict with number and url, or None on failure
        """
        url = f"{self.API_BASE_URL}/repos/{self.org}/{repo}/issues"
        payload = {
            "title": title,
            "body": body,
            "labels": labels or [],
            "assignee": assignee,
            "milestone": milestone
        }
        
        try:
            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to create issue in {repo}: {str(e)}")
            return None
    
    def get_user(self, username: str) -> Optional[Dict[str, Any]]:
        """
        Get GitHub user information.
        
        Args:
            username: GitHub username
            
        Returns:
            User dict or None if not found
        """
        url = f"{self.API_BASE_URL}/users/{username}"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.debug(f"User '{username}' not found: {str(e)}")
            return None
    
    def get_label(self, repo: str, label_name: str) -> Optional[Dict[str, Any]]:
        """
        Get label from repository.
        
        Args:
            repo: Repository name
            label_name: Label name
            
        Returns:
            Label dict or None if not found
        """
        url = f"{self.API_BASE_URL}/repos/{self.org}/{repo}/labels/{label_name}"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.debug(f"Label '{label_name}' not found in {repo}: {str(e)}")
            return None
    
    def create_label(self, repo: str, name: str, color: str = "cccccc",
                    description: str = "") -> Optional[Dict[str, Any]]:
        """
        Create a new label in repository.
        
        Args:
            repo: Repository name
            name: Label name
            color: Hex color code (without #)
            description: Label description
            
        Returns:
            Label dict or None on failure
        """
        url = f"{self.API_BASE_URL}/repos/{self.org}/{repo}/labels"
        payload = {
            "name": name,
            "color": color,
            "description": description
        }
        
        try:
            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to create label '{name}' in {repo}: {str(e)}")
            return None
    
    def get_project(self, project_id: int) -> Optional[Dict[str, Any]]:
        """
        Get GitHub project information.
        
        Args:
            project_id: Project ID
            
        Returns:
            Project dict or None if not found
        """
        url = f"{self.API_BASE_URL}/projects/{project_id}"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get project {project_id}: {str(e)}")
            return None
