"""
Command-line Interface for CSV Import Pipeline
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import Dict, Any
import yaml
from dotenv import load_dotenv

from csv_handler import CSVHandler
from validators import GitHubValidator
from github_client import GitHubClient
from issue_mapper import IssueMapper

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
load_dotenv()


class ImportPipeline:
    """Orchestrates the three-stage import workflow."""
    
    def __init__(self, config_path: Path = None):
        """
        Initialize pipeline.
        
        Args:
            config_path: Path to configuration file
        """
        self.config = self._load_config(config_path)
        self.github_client = GitHubClient()
        self.csv_handler = CSVHandler()
        self.validator = GitHubValidator(self.github_client)
        self.mapper = IssueMapper(self.github_client, self.config)
    
    def _load_config(self, config_path: Path) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        if not config_path:
            config_path = Path('config/mappings.yaml')
        
        if config_path.exists():
            with open(config_path) as f:
                return yaml.safe_load(f) or {}
        
        return {}
    
    def validate(self, csv_path: Path, dry_run: bool = True) -> Dict[str, Any]:
        """
        Stage 1: Read and validate CSV.
        
        Args:
            csv_path: Path to CSV file
            dry_run: If True, don't proceed to import
            
        Returns:
            Validation result dict with errors/warnings
        """
        logger.info(f"Stage 1: Reading and validating CSV from {csv_path}")
        
        # Read CSV
        rows, errors = self.csv_handler.read_csv(csv_path)
        
        # Validate format
        format_errors = self.csv_handler.validate_format(rows)
        errors.extend(format_errors)
        
        result = {
            'valid': len(errors) == 0,
            'rows_count': len(rows),
            'errors': errors,
            'warnings': [],
            'data': rows
        }
        
        logger.info(f"CSV validation complete: {result['rows_count']} rows, {len(errors)} errors")
        
        return result
    
    def enrich(self, validation_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Stage 2: Enrich and validate against GitHub.
        
        Args:
            validation_result: Result from validate()
            
        Returns:
            Enrichment result with warnings/errors
        """
        if not validation_result['valid']:
            logger.error("Cannot proceed with enrichment: CSV validation failed")
            return validation_result
        
        logger.info("Stage 2: Enriching and validating against GitHub")
        
        rows = validation_result['data']
        
        # Validate assignees
        validation_result['warnings'].extend(self.validator.validate_assignees(rows))
        
        # Validate labels
        for repo in [self.config.get('repository_rules', {}).get('primary'),
                     self.config.get('repository_rules', {}).get('secondary')]:
            if repo:
                validation_result['warnings'].extend(self.validator.validate_labels(rows, repo))
        
        logger.info(f"Enrichment complete: {len(validation_result['warnings'])} warnings")
        
        return validation_result
    
    def import_to_github(self, enrichment_result: Dict[str, Any], confirm: bool = False) -> Dict[str, Any]:
        """
        Stage 3: Import to GitHub.
        
        Args:
            enrichment_result: Result from enrich()
            confirm: If True, proceed with import (no confirmation prompt)
            
        Returns:
            Import result with created issues
        """
        if not enrichment_result['valid']:
            logger.error("Cannot proceed with import: validation failed")
            return enrichment_result
        
        logger.info("Stage 3: Importing to GitHub")
        
        rows = enrichment_result['data']
        created_issues = []
        errors = []
        
        for row in rows:
            try:
                # Determine repository
                repo = row.get('Repository') or self.config.get('repository_rules', {}).get('default')
                
                # Map row to issue
                issue = self.mapper.map_row_to_issue(row, repo)
                
                # Enrich issue
                issue = self.mapper.enrich_with_github_metadata(issue)
                
                # Create in GitHub
                logger.info(f"Creating issue: {issue['title']} in {repo}")
                created = self.github_client.create_issue(
                    repo,
                    issue['title'],
                    issue['body'],
                    issue['labels'],
                    issue['assignee'],
                    issue['milestone']
                )
                
                if created:
                    created_issues.append(created)
                    logger.info(f"Created issue #{created.get('number')} in {repo}")
                else:
                    errors.append({
                        "row_title": row.get('Title'),
                        "message": "Failed to create issue"
                    })
            
            except Exception as e:
                logger.error(f"Error processing row '{row.get('Title')}': {str(e)}")
                errors.append({
                    "row_title": row.get('Title'),
                    "message": str(e)
                })
        
        return {
            'valid': len(errors) == 0,
            'created_issues': created_issues,
            'errors': errors,
            'total_created': len(created_issues)
        }
    
    def preview(self, validation_result: Dict[str, Any]) -> None:
        """Preview issues that will be created."""
        if not validation_result['valid']:
            logger.error("Cannot preview: validation failed")
            return
        
        rows = validation_result['data']
        
        print("\n=== Import Preview ===")
        print(f"Total items to import: {len(rows)}\n")
        
        for row in rows:
            repo = row.get('Repository') or self.config.get('repository_rules', {}).get('default')
            print(f"[{row.get('Type')}] {row.get('Title')}")
            print(f"  Repository: {repo}")
            print(f"  Assignee: {row.get('Assignee') or 'Unassigned'}")
            print(f"  Labels: {row.get('Labels') or 'None'}")
            print()


def main():
    """Command-line entry point."""
    parser = argparse.ArgumentParser(
        description='CSV Import Pipeline for GitHub Issues and Epics'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate CSV file')
    validate_parser.add_argument('--csv', type=Path, required=True, help='Path to CSV file')
    validate_parser.add_argument('--dry-run', action='store_true', help='Dry run mode')
    
    # Import command
    import_parser = subparsers.add_parser('import', help='Import CSV to GitHub')
    import_parser.add_argument('--csv', type=Path, required=True, help='Path to CSV file')
    import_parser.add_argument('--confirm', action='store_true', help='Skip confirmation prompt')
    
    # Preview command
    preview_parser = subparsers.add_parser('preview', help='Preview import')
    preview_parser.add_argument('--csv', type=Path, required=True, help='Path to CSV file')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    pipeline = ImportPipeline()
    
    if args.command == 'validate':
        result = pipeline.validate(args.csv, dry_run=args.dry_run)
        print_result(result)
    
    elif args.command == 'import':
        validate_result = pipeline.validate(args.csv, dry_run=False)
        if not validate_result['valid']:
            print_result(validate_result)
            sys.exit(1)
        
        enrich_result = pipeline.enrich(validate_result)
        print_result(enrich_result)
        
        if not args.confirm:
            response = input("\nProceed with import? (yes/no): ")
            if response.lower() != 'yes':
                logger.info("Import cancelled")
                sys.exit(0)
        
        import_result = pipeline.import_to_github(enrich_result, confirm=args.confirm)
        print_result(import_result)
    
    elif args.command == 'preview':
        result = pipeline.validate(args.csv, dry_run=True)
        pipeline.preview(result)


def print_result(result: Dict[str, Any]) -> None:
    """Pretty-print result dict."""
    import json
    print(json.dumps(result, indent=2, default=str))


if __name__ == '__main__':
    main()
