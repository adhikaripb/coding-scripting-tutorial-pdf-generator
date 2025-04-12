from fpdf import FPDF
import re
import os
from datetime import datetime

def improved_clean_text_for_pdf(text):
    replacements = {
        "’": "'",
        "‘": "'",
        "“": '"',
        "”": '"',
        "–": "-",
        "—": "-",
        "…": "...",
        "•": "-",
        "→": "->"
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def parse_custom_protocol(file_path):
    with open(file_path, "r") as f:
        title_line = f.readline().strip()
        subtitle_line = f"{f.readline().strip()}_{datetime.today().strftime('%d %b, %Y')}"
        lines = [line.rstrip() for line in f]

    steps = []
    current_title = ""
    substeps = []
    current_instruction = ""
    inside_script = False
    script_block = []

    for line in lines:
        if line.lower().startswith("step"):
            if current_instruction:
                substeps.append({"instruction": current_instruction})
                current_instruction = ""
            if current_title:
                steps.append((current_title, substeps))
            current_title = line
            substeps = []
        elif line.strip() == '"""':
            if not inside_script:
                script_block = []
            else:
                substeps.append({"instruction": current_instruction, "script": "\n".join(script_block)})
                current_instruction = ""
            inside_script = not inside_script
        elif inside_script:
            if len(line) <= 72:
                script_block.append(line)
            else:
                words = line.strip().split()
                current_line = ""
                for word in words:
                    if len(current_line) + len(word) + 1 > 72:
                        script_block.append(current_line.strip())
                        current_line = word + " "
                    else:
                        current_line += word + " "
                if current_line:
                    script_block.append("..... " + current_line.strip())
        elif line.startswith("-"):
            if current_instruction:
                substeps.append({"instruction": current_instruction})
            current_instruction = line
    if current_instruction:
        substeps.append({"instruction": current_instruction})
    if current_title:
        steps.append((current_title, substeps))
    return title_line, subtitle_line, steps

# Rebuild the PDF with proper y-position tracking and distinct script blocks
class FixedStyledScriptPDF(FPDF):
    def header(self):
        if hasattr(self, 'document_title'):
            self.set_font("Helvetica", "B", 16)
            self.set_text_color(30, 80, 160)
            self.cell(0, 10, self.document_title, ln=True, align="C")
        if hasattr(self, 'document_subtitle'):
            self.set_font("Helvetica", "I", 10)
            self.set_text_color(100, 100, 100)
            self.cell(0, 6, self.document_subtitle, ln=True, align="R")
        self.ln(8)

    def add_step(self, title, substeps, color=(0, 0, 0)):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(0, 128, 128)
        self.ln(6)  # More spacing before next step
        self.multi_cell(0, 6, improved_clean_text_for_pdf(title))

        for sub in substeps:
            self.set_font("Helvetica", "", 11)
            self.set_text_color(0, 0, 0)
            self.multi_cell(0, 6, improved_clean_text_for_pdf(sub["instruction"]))
            self.ln(1)
            if "script" in sub:
                self.add_separated_script_block(sub["script"].strip().split("\n"))

    def add_separated_script_block(self, lines):
        self.set_font("Courier", "", 10)
        self.set_fill_color(30, 30, 30)

        block_width = self.w - self.l_margin * 2 - 10
        block_height = 6 * len(lines)
        x_start = self.l_margin + 5
        y_start = self.get_y()
        if y_start + block_height > self.page_break_trigger:
            self.add_page()
            y_start = self.get_y()
        self.rect(x_start, y_start, block_width, block_height, 'F')

        for line in lines:
            self.set_y(y_start)
            self.set_x(x_start + 1)
            self.write_colored_tokens(line)
            y_start += 6
            self.set_y(y_start)

        self.ln(2)

    def wrap_colored_tokens(self, line, max_width):
        if len(line) <= 72:
            return [line.strip()]

        words = line.strip().split()
        lines = []
        current_line = ""

        for word in words:
            if len(current_line) + len(word) + 1 > 72:
                lines.append(current_line.strip())
                current_line = "AAAA" + word + " "
            else:
                current_line += word + " "

        if current_line:
            print(f"current_line: {current_line}")
            lines.append(current_line.strip())

        return lines

    def write_colored_tokens(self, line):
        tokens = re.split(r'(\s+)', line)
        for token in tokens:
            if token.startswith("$"):
                self.set_text_color(0, 255, 0)
            elif token.startswith("git"):
                self.set_text_color(135, 206, 250)
            elif "http" in token:
                self.set_text_color(255, 105, 180)
            elif token.startswith("-"):
                self.set_text_color(255, 165, 0)
            elif '"' in token or "'" in token:
                self.set_text_color(255, 255, 255)
            else:
                self.set_text_color(200, 200, 200)
            self.cell(self.get_string_width(token), 6, token, ln=0)

colors = [
    (220, 20, 60), (0, 128, 0), (0, 102, 204), (153, 51, 255),
    (255, 128, 0), (102, 0, 204), (0, 153, 153), (255, 51, 102),
    (0, 102, 102), (128, 0, 0)
]

# Prompt the user to input the path to the .txt file
input_txt_path = input("Enter the full path to your input .txt file: ").strip()
title_line, subtitle_line, parsed_steps = parse_custom_protocol(input_txt_path)

# Generate the new fixed version of the PDF
pdf = FixedStyledScriptPDF()
pdf.document_title = title_line.replace("Title: ", "").strip()
pdf.document_subtitle = subtitle_line.strip()
pdf.set_left_margin(20)
pdf.set_right_margin(20)
pdf.add_page()

for i, (title, substeps) in enumerate(parsed_steps):
    color = colors[i % len(colors)]
    pdf.add_step(title, substeps, color=color)

output_dir = os.path.dirname(input_txt_path)
fixed_pdf_path = os.path.join(output_dir, f'{pdf.document_title}.pdf')
pdf.output(fixed_pdf_path)
