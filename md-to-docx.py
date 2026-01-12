
import sys
import os
import argparse
import markdown
from docx import Document
from docx.shared import Pt, Mm, RGBColor
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from bs4 import BeautifulSoup, Tag

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Convert Markdown to Word document')
parser.add_argument('input_md', help='Input Markdown file')
parser.add_argument('output_docx', help='Output Word document file')
parser.add_argument('--no-show', action='store_true', help='Do not open the file after creation')
args = parser.parse_args()

input_md = args.input_md
output_docx = args.output_docx

# Check if input file exists
if not os.path.exists(input_md):
    print(f"Error: Input file '{input_md}' not found.")
    sys.exit(1)

# Check if output file exists
if os.path.exists(output_docx):
    response = input(f"{output_docx} already exists. Delete and overwrite? (y/n): ")
    if response.lower() != 'y':
        print("Operation cancelled.")
        sys.exit(0)
    try:
        os.remove(output_docx)
    except PermissionError:
        print(f"Error: Cannot delete {output_docx}. The file may be open in another program.")
        print("Please close the file and try again.")
        sys.exit(1)

# Load Markdown content, "tables"
with open(input_md, "r", encoding="utf-8") as f:
    md_content = f.read()

# Convert Markdown to HTML
html = markdown.markdown(md_content, extensions=["fenced_code", "tables"])

# Parse HTML
soup = BeautifulSoup(html, "html.parser")

# Create Word document
doc = Document()

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

for element in soup.children:
    if isinstance(element, Tag):
        if element.name == "p":
            doc.add_paragraph(element.get_text())
        elif element.name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
            # Add headers with appropriate style
            level = int(element.name[1])  # Extract number from h1, h2, etc.
            doc.add_heading(element.get_text(), level=level)
        elif element.name == "pre":
            code_text = element.get_text().rstrip('\n')
            # Create a table with one cell for the code block
            table = doc.add_table(rows=1, cols=1)
            cell = table.cell(0, 0)
            
            # Add code text with monospace font
            paragraph = cell.paragraphs[0]
            run = paragraph.add_run(code_text)
            run.font.name = 'Courier New'
            run.font.size = Pt(10)
            
            # Remove paragraph spacing
            paragraph.paragraph_format.space_after = Pt(0)
            paragraph.paragraph_format.space_before = Pt(0)
            paragraph.paragraph_format.line_spacing = 1.0
            
            # Set cell margins to 3mm
            set_cell_margins(cell, Mm(3))
            
            # Set cell background to #F2F2F2
            set_cell_background(cell, 'F2F2F2')
            
            # Set 1pt black border
            set_table_border(table)
            
            # Add empty paragraph after table for spacing
            doc.add_paragraph()
        elif element.name == "ul":
            # Handle unordered lists
            for li in element.find_all("li", recursive=False):
                doc.add_paragraph(li.get_text(), style='List Bullet')
        elif element.name == "ol":
            # Handle ordered lists
            for li in element.find_all("li", recursive=False):
                doc.add_paragraph(li.get_text(), style='List Number')
        elif element.name == "table":
            # Handle tables
            rows = element.find_all("tr")
            if not rows:
                continue
                
            # Count maximum columns
            max_cols = 0
            for row in rows:
                cols = len(row.find_all(["th", "td"]))
                max_cols = max(max_cols, cols)
            
            if max_cols == 0:
                continue
                
            # Create Word table
            table = doc.add_table(rows=len(rows), cols=max_cols)
            
            # Process each row
            for row_idx, row in enumerate(rows):
                cells = row.find_all(["th", "td"])
                for col_idx, cell in enumerate(cells):
                    if col_idx < max_cols:
                        word_cell = table.cell(row_idx, col_idx)
                        cell_text = cell.get_text().strip()
                        word_cell.text = cell_text
                        
                        # Make header row bold
                        if row_idx == 0 or cell.name == "th":
                            # Clear the existing paragraph and add a new bold run
                            word_cell.paragraphs[0].clear()
                            run = word_cell.paragraphs[0].add_run(cell_text)
                            run.font.bold = True
            
            # Set table borders
            set_table_border(table)
            
            # Add empty paragraph after table for spacing
            doc.add_paragraph()

try:
    doc.save(output_docx)
    print(f"Successfully created {output_docx}")
    
    # Open the file unless --no-show is specified
    if not args.no_show:
        os.startfile(output_docx)
except PermissionError:
    print(f"Error: Cannot save {output_docx}. The file may be open in another program.")
    print("Please close the file and try again.")
    sys.exit(1)
except Exception as e:
    print(f"Error saving file: {e}")
    sys.exit(1)
