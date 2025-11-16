"""
Issue Mapper Module
Maps CSV rows to GitHub issues and handles data enrichment.
"""

import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class IssueMapper:
    """Maps CSV rows to GitHub issue objects."""
    
    def __init__(self, github_client, config: Dict[str, Any]):
        """
        Initialize mapper.
        
        Args:
            github_client: GitHubClient instance
            config: Configuration dict with field mappings
        """
        self.client = github_client
        self.config = config
    
    def map_row_to_issue(self, row: Dict[str, str], repo: str) -> Dict[str, Any]:
        """
        Convert CSV row to GitHub issue payload.
        
        Args:
            row: CSV row dict
            repo: Target repository
            
        Returns:
            Issue payload dict
        """
        labels = self._parse_labels(row.get('Labels', ''))
        labels.append('ask-myuni')  # Always add project label
        
        return {
            'title': row.get('Title', '').strip(),
            'body': row.get('Description', '').strip(),
            'labels': list(set(labels)),
            'assignee': row.get('Assignee', '').strip() or None,
            'milestone': row.get('Milestone', '').strip() or None,
            'type': row.get('Type', 'Task'),
            'repository': repo
        }
    
    def _parse_labels(self, labels_str: str) -> List[str]:
        """
        Parse semicolon-separated labels.
        
        Args:
            labels_str: Semicolon-separated label string
            
        Returns:
            List of label names
        """
        if not labels_str:
            return []
        
        return [l.strip() for l in labels_str.split(';') if l.strip()]
    
    def enrich_with_github_metadata(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enrich issue with GitHub metadata (validate/create labels, etc).
        
        Args:
            issue: Issue dict
            
        Returns:
            Enriched issue dict
        """
        repo = issue.get('repository')
        
        # Validate and create labels if needed
        enriched_labels = []
        for label in issue.get('labels', []):
            label_obj = self.client.get_label(repo, label)
            if not label_obj:
                # Create label if it doesn't exist
                logger.info(f"Creating label '{label}' in {repo}")
                self.client.create_label(repo, label)
            enriched_labels.append(label)
        
        issue['labels'] = enriched_labels
        return issue
