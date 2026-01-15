"""
Configuration loading and management
"""

import os
import json


def load_config():
    """Load configuration from config.json or use defaults"""
    default_config = {
        "headings": {
            "h1": {
                "font_name": "Calibri",
                "font_size": 16,
                "bold": True,
                "italic": False,
                "color": "2E75B6",
                "space_before": 12,
                "space_after": 6
            },
            "h2": {
                "font_name": "Calibri",
                "font_size": 14,
                "bold": True,
                "italic": False,
                "color": "000000",
                "space_before": 10,
                "space_after": 4
            },
            "h3": {
                "font_name": "Calibri",
                "font_size": 12,
                "bold": True,
                "italic": False,
                "color": "000000",
                "space_before": 8,
                "space_after": 3
            },
            "h4": {
                "font_name": "Calibri",
                "font_size": 11,
                "bold": True,
                "italic": False,
                "color": "000000",
                "space_before": 6,
                "space_after": 2
            }
        },
        "codeblock": {
            "font_name": "Courier New",
            "font_size": 10,
            "background_color": "F2F2F2",
            "cell_margin": 3,
            "line_spacing": 1.0
        },
        "paragraph": {
            "font_name": "Calibri",
            "font_size": 11,
            "bold": False,
            "italic": False,
            "color": "000000",
            "space_before": 0,
            "space_after": 8,
            "line_spacing": 1.15
        },
        "table": {
            "header": {
                "font_name": "Calibri",
                "font_size": 10,
                "bold": True,
                "uppercase": True,
                "vertical_alignment": "bottom"
            },
            "data": {
                "font_name": "Calibri"
            }
        }
    }
    
    # Look for config.json in the script's directory
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load config.json ({e}), using defaults")
            return default_config
    return default_config
