"""
Formatters for Word document elements
"""

from .table import set_cell_background, set_cell_margins, set_table_border, set_cell_border
from .heading import apply_heading_format

__all__ = [
    'set_cell_background',
    'set_cell_margins',
    'set_table_border',
    'set_cell_border',
    'apply_heading_format'
]
