# How to Convert Markdown to Word Using md-to-docx.py

## 1. Get Your Markdown File
- When you have received the answer you want and are ready to export it, ask the chatbot to export the last answer to a Markdown file for download.
- Download the `.md` file to your computer.

## 2. Run the Conversion Script
- Open your terminal or command prompt.
- Use the following command to convert Markdown to Word:

```bash
python md-to-docx.py input.md output.docx
```

Replace `input.md` with your Markdown file name and `output.docx` with the desired Word file name.

### Optional: Prevent Auto-Opening
Add `--no-show` if you do not want the Word file to open automatically:

```bash
python md-to-docx.py input.md output.docx --no-show
```

---

## Appendix: Install Python and Required Packages
Before running the script, make sure you have saved the provided Python script as `md-to-docx.py`.

### Installation Using requirements.txt (Recommended)
Install all dependencies at once:

```bash
pip install -r requirements.txt
```

### Manual Installation
Alternatively, install packages individually:

```bash
pip install python-docx markdown beautifulsoup4
```

### Dependencies
- python-docx
- markdown
- beautifulsoup4
