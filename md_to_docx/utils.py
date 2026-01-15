"""
Utility functions for Markdown preprocessing
"""

import re


def fix_markdown_tables(content):
    """Remove blank lines between table rows to ensure proper parsing"""
    # This function processes markdown content to fix tables that have blank lines
    # between rows, which can break markdown table parsing
    
    lines = content.split('\n')
    result = []
    in_table = False
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Detect table start (line with pipes)
        if '|' in stripped and stripped.count('|') >= 2:
            # Check if this is a separator line (---)
            is_separator = bool(re.match(r'^[\s\-:|]+$', stripped.replace('|', '')))
            
            # Check if previous line was also table content
            if i > 0 and in_table and not result[-1].strip():
                # Remove blank line before table row
                result.pop()
            
            in_table = True
            result.append(line)
        else:
            # Not a table line
            if stripped:  # Non-empty line
                in_table = False
            result.append(line)
    
    return '\n'.join(result)
