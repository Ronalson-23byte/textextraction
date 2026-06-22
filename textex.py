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

    # Determine the folder name based on the parent folder of the PDF
    dir_path = os.path.dirname(input_pdf)
    folder_name = os.path.basename(dir_path)
    
    # Fallback just in case there is no parent folder in the path
    if not folder_name:
        folder_name = os.path.splitext(os.path.basename(input_pdf))[0]

    # Create the specific target directory: output_folder/folder_name/
    specific_output_dir = os.path.join(output_folder, folder_name)
    os.makedirs(specific_output_dir, exist_ok=True)

    # Define the final text file path: output_folder/folder_name/english.txt
    output_txt = os.path.join(specific_output_dir, "english.txt")

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
        
        # Join the perfectly formatted pages
        with open(output_txt, "w", encoding="utf-8") as f:
            f.write("\n\n".join(extracted_pages))
                
        print(f"Success! Saved to:\n{output_txt}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# ==========================================
# Run the Code
# ==========================================
if __name__ == "__main__":
    
    # Update to your actual PDF path
    INPUT_PDF_PATH = "import os"
import glob
import pdfplumber
import re

def smart_unwrap_text(raw_text):
    """
    Stitches broken sentences back together, preserves paragraph breaks, 
    and glues stranded list numbers (like '3.1.') to their sentences.
    """
    lines = raw_text.split('\n')
    smoothed_text = ""
    
    exact_marker_pattern = r'^(\d+(\.\d+)*\.?|\([a-zA-Z0-9]+\)|[A-Z]\.)$'
    next_line_start_pattern = r'^(\d+(\.\d+)*\.?|\([a-zA-Z0-9]+\)|[A-Z]\.)(\s|$)'
    
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
            
        smoothed_text += line
        
        if i < len(lines) - 1:
            next_line = lines[i+1].strip()
            
            if re.match(exact_marker_pattern, line):
                smoothed_text += " "
            elif len(line) < 55:
                smoothed_text += "\n\n"
            elif re.match(next_line_start_pattern, next_line):
                smoothed_text += "\n\n"
            else:
                smoothed_text += " "
                
    return smoothed_text

def extract_perfect_pdf(input_pdf: str, output_folder: str, top_margin=75, bottom_margin=60):
    """
    Crops headers/footers and smartly unwraps text for perfect readability.
    """
    dir_path = os.path.dirname(input_pdf)
    folder_name = os.path.basename(dir_path)
    
    if not folder_name:
        folder_name = os.path.splitext(os.path.basename(input_pdf))[0]

    specific_output_dir = os.path.join(output_folder, folder_name)
    os.makedirs(specific_output_dir, exist_ok=True)
    output_txt = os.path.join(specific_output_dir, "english.txt")

    extracted_pages = []

    try:
        with pdfplumber.open(input_pdf) as pdf:
            for page_num, page in enumerate(pdf.pages):
                x0 = 0
                x1 = page.width
                top = 0 if page_num == 0 else top_margin 
                bottom = page.height - bottom_margin
                
                cropped_page = page.crop((x0, top, x1, bottom))
                raw_text = cropped_page.extract_text()
                
                if raw_text:
                    fixed_text = smart_unwrap_text(raw_text)
                    extracted_pages.append(fixed_text)

        with open(output_txt, "w", encoding="utf-8") as f:
            f.write("\n\n".join(extracted_pages))
                
        print(f"  -> Success: Saved to {output_txt}")

    except Exception as e:
        print(f"  -> Error processing {input_pdf}: {e}")

def batch_extract_folder(input_directory: str, output_directory: str, top_margin=75, bottom_margin=60):
    """
    Finds all PDFs in the input_directory (including subfolders) and extracts them.
    """
    if not os.path.exists(input_directory):
        print(f"Error: The directory '{input_directory}' does not exist.")
        return

    # Create a search pattern to find all PDFs recursively
    search_pattern = os.path.join(input_directory, "**", "*.pdf")
    pdf_files = glob.glob(search_pattern, recursive=True)

    if not pdf_files:
        print(f"No PDF files found in '{input_directory}'.")
        return

    print(f"Found {len(pdf_files)} PDF(s). Starting batch extraction...\n" + "-"*50)

    for index, pdf_path in enumerate(pdf_files, start=1):
        print(f"[{index}/{len(pdf_files)}] Processing: {os.path.basename(pdf_path)} (from {os.path.basename(os.path.dirname(pdf_path))})")
        extract_perfect_pdf(pdf_path, output_directory, top_margin, bottom_margin)

    print("-" * 50 + "\nBatch extraction complete!")


# ==========================================
# Run the Code
# ==========================================
if __name__ == "__main__":
    
    # Point this to the root folder containing all your case folders
    INPUT_FOLDER = "2024-volume2_part1" 
    
    # The master folder where all extracted folders will be saved
    OUTPUT_FOLDER = "Text_Extractions" 
    
    batch_extract_folder(INPUT_FOLDER, OUTPUT_FOLDER, top_margin=75, bottom_margin=60)
    OUTPUT_DIRECTORY = "Text_Extractions" 
    
    extract_perfect_pdf(INPUT_PDF_PATH, OUTPUT_DIRECTORY, top_margin=75, bottom_margin=60)
