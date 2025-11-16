"""
Validators Module
Responsible for business rule validation and GitHub metadata enrichment.
"""

import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class GitHubValidator:
    """Validates data against GitHub business rules and constraints."""
    
    def __init__(self, github_client):
        """
        Initialize validator with GitHub client.
        
        Args:
            github_client: GitHubClient instance for API calls
        """
        self.client = github_client
    
    def validate_assignees(self, rows: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """
        Validate assignee field against GitHub users.
        
        Args:
            rows: List of row dictionaries
            
        Returns:
            List of error/warning dicts
        """
        errors = []
        
        for row_num, row in enumerate(rows, start=2):
            assignee = row.get('Assignee', '').strip()
            if not assignee:
                continue
            
            # Validate user exists
            try:
                user = self.client.get_user(assignee)
                if not user:
                    errors.append({
                        "row": row_num,
                        "field": "Assignee",
                        "message": f"User '{assignee}' not found in GitHub",
                        "severity": "warn"
                    })
            except Exception as e:
                errors.append({
                    "row": row_num,
                    "field": "Assignee",
                    "message": f"Failed to validate user '{assignee}': {str(e)}",
                    "severity": "warn"
                })
        
        return errors
    
    def validate_labels(self, rows: List[Dict[str, str]], repo: str) -> List[Dict[str, Any]]:
        """
        Validate labels exist in repository.
        
        Args:
            rows: List of row dictionaries
            repo: Repository name
            
        Returns:
            List of error/warning dicts
        """
        errors = []
        
        for row_num, row in enumerate(rows, start=2):
            labels_str = row.get('Labels', '').strip()
            if not labels_str:
                continue
            
            labels = [l.strip() for l in labels_str.split(';')]
            for label in labels:
                # Validate label exists
                try:
                    label_obj = self.client.get_label(repo, label)
                    if not label_obj:
                        errors.append({
                            "row": row_num,
                            "field": "Labels",
                            "message": f"Label '{label}' not found in {repo}, will create",
                            "severity": "info"
                        })
                except Exception as e:
                    errors.append({
                        "row": row_num,
                        "field": "Labels",
                        "message": f"Failed to validate label '{label}': {str(e)}",
                        "severity": "warn"
                    })
        
        return errors
    
    def validate_parent_child_relationships(self, rows: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """
        Validate Epic-Task relationships.
        
        Args:
            rows: List of row dictionaries
            
        Returns:
            List of error dicts
        """
        errors = []
        
        # Group by Epic (Type == 'Epic')
        epics = set()
        for row in rows:
            if row.get('Type') == 'Epic':
                epics.add(row.get('Title'))
        
        # Validate tasks reference valid epics
        for row_num, row in enumerate(rows, start=2):
            if row.get('Type') == 'Task':
                # Note: Current CSV doesn't have Epic parent reference
                # Adjust logic if parent Epic column is added
                pass
        
        return errors
