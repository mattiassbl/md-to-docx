"""
Heading formatting functions for Word documents
"""

from docx.shared import Pt, RGBColor


def apply_heading_format(paragraph, heading_config):
    """Apply formatting to a heading paragraph based on config"""
    run = paragraph.runs[0] if paragraph.runs else paragraph.add_run()
    
    # Apply font settings
    run.font.name = heading_config.get('font_name', 'Calibri')
    run.font.size = Pt(heading_config.get('font_size', 12))
    run.font.bold = heading_config.get('bold', True)
    run.font.italic = heading_config.get('italic', False)
    
    # Apply color if specified
    color = heading_config.get('color')
    if color:
        if len(color) == 6:
            r = int(color[0:2], 16)
            g = int(color[2:4], 16)
            b = int(color[4:6], 16)
            run.font.color.rgb = RGBColor(r, g, b)
    
    # Apply spacing
    paragraph.paragraph_format.space_before = Pt(heading_config.get('space_before', 0))
    paragraph.paragraph_format.space_after = Pt(heading_config.get('space_after', 0))
