import os
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
    Finds all PDFs in the input_directory, but only processes those 
    containing 'english' in the filename.
    """
    if not os.path.exists(input_directory):
        print(f"Error: The directory '{input_directory}' does not exist.")
        return

    # Create a search pattern to find all PDFs recursively
    search_pattern = os.path.join(input_directory, "**", "*.pdf")
    pdf_files = glob.glob(search_pattern, recursive=True)

    # FILTER: Only keep files that have 'english' in their name (case-insensitive)
    english_pdfs = [f for f in pdf_files if "english" in f.lower()]

    if not english_pdfs:
        print(f"No 'english' PDF files found in '{input_directory}'.")
        return

    print(f"Found {len(english_pdfs)} English PDF(s). Starting extraction...\n" + "-"*50)

    for index, pdf_path in enumerate(english_pdfs, start=1):
        print(f"[{index}/{len(english_pdfs)}] Processing: {os.path.basename(pdf_path)}")
        extract_perfect_pdf(pdf_path, output_directory, top_margin, bottom_margin)

    print("-" * 50 + "\nBatch extraction complete!")


# ==========================================
# Run the Code
# ==========================================
if __name__ == "__main__":
    
    # Point this to the ROOT folder containing all your case folders
    # NOTE: Be sure to use double backslashes (\\) or forward slashes (/) for Windows paths
    INPUT_FOLDER = "2023-volume3_part1"  # <--- UPDATE THIS TO YOUR ACTUAL FOLDER PATH
    
    # The master folder where all extracted folders will be saved
    OUTPUT_FOLDER = "text-extraction2023_volume3_part1" 
    
    # Run the batch extraction
    batch_extract_folder(INPUT_FOLDER, OUTPUT_FOLDER, top_margin=75, bottom_margin=60)
