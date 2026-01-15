"""
Table formatting functions for Word documents
"""

from docx.shared import Mm
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


def set_cell_background(cell, color):
    """Set cell background color"""
    shading_elm = OxmlElement('w:shd')
    shading_elm.set(qn('w:fill'), color)
    cell._element.get_or_add_tcPr().append(shading_elm)


def set_cell_margins(cell, margin):
    """Set cell margins"""
    tc = cell._element
    tcPr = tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for margin_name in ['top', 'left', 'bottom', 'right']:
        node = OxmlElement(f'w:{margin_name}')
        node.set(qn('w:w'), str(margin.twips))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)


def set_table_border(table):
    """Set 1pt black border for table"""
    tbl = table._element
    tblPr = tbl.tblPr
    if tblPr is None:
        tblPr = OxmlElement('w:tblPr')
        tbl.insert(0, tblPr)
    
    tblBorders = OxmlElement('w:tblBorders')
    for border_name in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        border = OxmlElement(f'w:{border_name}')
        border.set(qn('w:val'), 'single')
        border.set(qn('w:sz'), '8')  # 1pt = 8 eighths of a point
        border.set(qn('w:color'), '000000')
        border.set(qn('w:space'), '0')
        tblBorders.append(border)
    tblPr.append(tblBorders)


def set_cell_border(cell, borders):
    """Set specific borders for a cell"""
    tc = cell._element
    tcPr = tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    
    for border_name, include in borders.items():
        border = OxmlElement(f'w:{border_name}')
        if include:
            border.set(qn('w:val'), 'single')
            border.set(qn('w:sz'), '8')  # 1pt
            border.set(qn('w:color'), '000000')
        else:
            border.set(qn('w:val'), 'nil')
        border.set(qn('w:space'), '0')
        tcBorders.append(border)
    
    tcPr.append(tcBorders)
