import os
import pdfplumber
import re

def smart_unwrap_text(raw_text):
    """
    Stitches broken sentences back together, preserves paragraph breaks, 
    and glues stranded list numbers (like '3.1.') to their sentences.
    """
    lines = raw_text.split('\n')
    smoothed_text = ""
    
    # Regex to detect a line that is EXACTLY a list number (e.g., "1.", "3.1.", "(i)", "A.")
    exact_marker_pattern = r'^(\d+(\.\d+)*\.?|\([a-zA-Z0-9]+\)|[A-Z]\.)$'
    
    # Regex to detect if the NEXT line STARTS with a list number
    next_line_start_pattern = r'^(\d+(\.\d+)*\.?|\([a-zA-Z0-9]+\)|[A-Z]\.)(\s|$)'
    
    for i, line in enumerate(lines):
        line = line.strip()
        
        if not line:
            continue # Skip completely empty lines
            
        smoothed_text += line
        
        # Check the next line to decide what comes next: a space or a paragraph break (\n\n)
        if i < len(lines) - 1:
            next_line = lines[i+1].strip()
            
            # RULE 0 (The Fix): If this current line is JUST a number (like "3.1."), 
            # glue it to the next line with a space. Do not break.
            if re.match(exact_marker_pattern, line):
                smoothed_text += " "
                
            # RULE 1: If the line is short, it usually means the paragraph naturally ended early
            elif len(line) < 55:
                smoothed_text += "\n\n"
                
            # RULE 2: If the next line starts with a list marker, start a new paragraph
            elif re.match(next_line_start_pattern, next_line):
                smoothed_text += "\n\n"
                
            # RULE 3: Otherwise, it is a broken sentence. Join them with a single space!
            else:
                smoothed_text += " "
                
    return smoothed_text

def extract_perfect_pdf(input_pdf: str, output_folder: str, top_margin=75, bottom_margin=60):
    """
    Crops headers/footers and smartly unwraps text for perfect readability.
    """
    if not os.path.exists(input_pdf):
        print(f"Error: Could not find the file: {input_pdf}")
        return

    # Dynamic File Naming
    dir_path = os.path.dirname(input_pdf)
    folder_name = os.path.basename(dir_path)
    if not folder_name:
        folder_name = os.path.splitext(os.path.basename(input_pdf))[0]

    os.makedirs(output_folder, exist_ok=True)
    output_txt = os.path.join(output_folder, f"{folder_name}.txt")

    extracted_pages = []

    try:
        print(f"Opening '{input_pdf}' for smart extraction...")
        
        with pdfplumber.open(input_pdf) as pdf:
            for page_num, page in enumerate(pdf.pages):
                
                # Define safe reading zone to crop out headers/footers
                x0 = 0
                x1 = page.width
                top = 0 if page_num == 0 else top_margin 
                bottom = page.height - bottom_margin
                
                cropped_page = page.crop((x0, top, x1, bottom))
                raw_text = cropped_page.extract_text()
                
                if raw_text:
                    # Pass the raw chopped text through our new Smart Unwrapper
                    fixed_text = smart_unwrap_text(raw_text)
                    extracted_pages.append(fixed_text)

        print(f"Saving beautifully formatted text to '{output_txt}'...")
        
        # Join the perfectly formatted pages. I removed the \f so it flows cleanly for Excel
        with open(output_txt, "w", encoding="utf-8") as f:
            f.write("\n\n".join(extracted_pages))
                
        print(f"Success! Saved to: {output_txt}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# ==========================================
# Run the Code
# ==========================================
if __name__ == "__main__":
    
    # Update to your actual PDF path
    INPUT_PDF_PATH = INPUT_PDF_PATH = "2023_Volume_2_Part_1/Dr. Jangala Suresh Babu v. The Manipur Lokayukta & Ors/English.pdf"
import pdfplumber
import re

def smart_unwrap_text(raw_text):
    """
    Stitches broken sentences back together, preserves paragraph breaks, 
    and glues stranded list numbers (like '3.1.') to their sentences.
    """
    lines = raw_text.split('\n')
    smoothed_text = ""
    
    # Regex to detect a line that is EXACTLY a list number (e.g., "1.", "3.1.", "(i)", "A.")
    exact_marker_pattern = r'^(\d+(\.\d+)*\.?|\([a-zA-Z0-9]+\)|[A-Z]\.)$'
    
    # Regex to detect if the NEXT line STARTS with a list number
    next_line_start_pattern = r'^(\d+(\.\d+)*\.?|\([a-zA-Z0-9]+\)|[A-Z]\.)(\s|$)'
    
    for i, line in enumerate(lines):
        line = line.strip()
        
        if not line:
            continue # Skip completely empty lines
            
        smoothed_text += line
        
        # Check the next line to decide what comes next: a space or a paragraph break (\n\n)
        if i < len(lines) - 1:
            next_line = lines[i+1].strip()
            
            # RULE 0 (The Fix): If this current line is JUST a number (like "3.1."), 
            # glue it to the next line with a space. Do not break.
            if re.match(exact_marker_pattern, line):
                smoothed_text += " "
                
            # RULE 1: If the line is short, it usually means the paragraph naturally ended early
            elif len(line) < 55:
                smoothed_text += "\n\n"
                
            # RULE 2: If the next line starts with a list marker, start a new paragraph
            elif re.match(next_line_start_pattern, next_line):
                smoothed_text += "\n\n"
                
            # RULE 3: Otherwise, it is a broken sentence. Join them with a single space!
            else:
                smoothed_text += " "
                
    return smoothed_text

def extract_perfect_pdf(input_pdf: str, output_folder: str, top_margin=75, bottom_margin=60):
    """
    Crops headers/footers and smartly unwraps text for perfect readability.
    """
    if not os.path.exists(input_pdf):
        print(f"Error: Could not find the file: {input_pdf}")
        return

    # Dynamic File Naming
    dir_path = os.path.dirname(input_pdf)
    folder_name = os.path.basename(dir_path)
    if not folder_name:
        folder_name = os.path.splitext(os.path.basename(input_pdf))[0]

    os.makedirs(output_folder, exist_ok=True)
    output_txt = os.path.join(output_folder, f"{folder_name}.txt")

    extracted_pages = []

    try:
        print(f"Opening '{input_pdf}' for smart extraction...")
        
        with pdfplumber.open(input_pdf) as pdf:
            for page_num, page in enumerate(pdf.pages):
                
                # Define safe reading zone to crop out headers/footers
                x0 = 0
                x1 = page.width
                top = 0 if page_num == 0 else top_margin 
                bottom = page.height - bottom_margin
                
                cropped_page = page.crop((x0, top, x1, bottom))
                raw_text = cropped_page.extract_text()
                
                if raw_text:
                    # Pass the raw chopped text through our new Smart Unwrapper
                    fixed_text = smart_unwrap_text(raw_text)
                    extracted_pages.append(fixed_text)

        print(f"Saving beautifully formatted text to '{output_txt}'...")
        
        # Join the perfectly formatted pages. I removed the \f so it flows cleanly for Excel
        with open(output_txt, "w", encoding="utf-8") as f:
            f.write("\n\n".join(extracted_pages))
                
        print(f"Success! Saved to: {output_txt}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# ==========================================
# Run the Code
# ==========================================
if __name__ == "__main__":
    
    # Update to your actual PDF path
    INPUT_PDF_PATH = "2024-volume2_part1/Angomjambam Bike Singh v. The State Of Manipur & Ors/English.pdf" 
    OUTPUT_DIRECTORY = "Text_Extractions" 
    
    extract_perfect_pdf(INPUT_PDF_PATH, OUTPUT_DIRECTORY, top_margin=75, bottom_margin=60) 
    OUTPUT_DIRECTORY = "Text_Extractions" 
    
    extract_perfect_pdf(INPUT_PDF_PATH, OUTPUT_DIRECTORY, top_margin=75, bottom_margin=60)