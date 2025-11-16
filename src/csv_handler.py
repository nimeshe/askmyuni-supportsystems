"""
CSV Handler Module
Responsible for reading, parsing, and validating CSV files.
"""

import csv
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Any

logger = logging.getLogger(__name__)


class CSVHandler:
    """Handles CSV reading, parsing, and format validation."""
    
    REQUIRED_COLUMNS = {'Title', 'Description', 'Type', 'Labels', 'Assignee', 'Milestone'}
    
    def __init__(self, template_columns: set = None):
        """
        Initialize CSV handler.
        
        Args:
            template_columns: Expected column headers (defaults to REQUIRED_COLUMNS)
        """
        self.template_columns = template_columns or self.REQUIRED_COLUMNS
    
    def read_csv(self, filepath: Path) -> Tuple[List[Dict[str, str]], List[Dict[str, Any]]]:
        """
        Read and parse CSV file.
        
        Args:
            filepath: Path to CSV file
            
        Returns:
            Tuple of (rows list, errors list)
            Each row is a dict with column headers as keys
            Errors contain: {"row": int, "field": str, "message": str}
        """
        rows = []
        errors = []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                # Validate headers
                if not reader.fieldnames:
                    errors.append({"row": 0, "field": "headers", "message": "No columns found"})
                    return rows, errors
                
                missing_cols = self.template_columns - set(reader.fieldnames)
                if missing_cols:
                    errors.append({
                        "row": 0,
                        "field": "headers",
                        "message": f"Missing required columns: {', '.join(missing_cols)}"
                    })
                
                # Parse rows
                for row_num, row in enumerate(reader, start=2):
                    if not any(row.values()):  # Skip empty rows
                        continue
                    rows.append(row)
        
        except Exception as e:
            errors.append({"row": 0, "field": "file", "message": f"Failed to read file: {str(e)}"})
        
        return rows, errors
    
    def validate_format(self, rows: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """
        Validate CSV format (headers, data types, required fields).
        
        Args:
            rows: List of row dictionaries
            
        Returns:
            List of error dicts
        """
        errors = []
        
        for row_num, row in enumerate(rows, start=2):
            # Validate required fields
            if not row.get('Title', '').strip():
                errors.append({
                    "row": row_num,
                    "field": "Title",
                    "message": "Title is required"
                })
            
            if row.get('Type') not in {'Epic', 'Task'}:
                errors.append({
                    "row": row_num,
                    "field": "Type",
                    "message": f"Type must be 'Epic' or 'Task', got '{row.get('Type')}'"
                })
        
        return errors
