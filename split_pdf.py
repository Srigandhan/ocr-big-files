import os
import time
from PyPDF2 import PdfReader, PdfWriter

def split_pdf(file_name, target_size_mb=45):
    # Get the directory and base name of the input file
    input_dir = os.path.dirname(file_name)
    base_name = os.path.splitext(os.path.basename(file_name))[0]  # Get the base file name
    
    # Create a folder named after the input file (without extension)
    output_folder = os.path.join(input_dir, base_name)
    os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist

    # Read the PDF file
    reader = PdfReader(file_name)
    total_pages = len(reader.pages)

    part_number = 1
    writer = PdfWriter()
    current_size = 0  # Current size of the output PDF in bytes

    for page_index in range(total_pages):
        # Add page to the writer
        writer.add_page(reader.pages[page_index])
        
        # Write the current part to disk
        output_file = os.path.join(output_folder, f"{base_name}-{part_number}.pdf")
        with open(output_file, 'wb') as output_pdf:
            writer.write(output_pdf)
        
        # Get the size of the written file
        current_size = os.path.getsize(output_file)

        # Check if we have reached the size limit
        if current_size / (1024 * 1024) >= target_size_mb:
            print(f"Saved: {output_file} ({current_size / (1024 * 1024):.2f} MB)")
            part_number += 1
            writer = PdfWriter()  # Reset writer for the next part

    # Save any remaining pages
    if len(writer.pages) > 0:
        output_file = os.path.join(output_folder, f"{base_name}-{part_number}.pdf")
        with open(output_file, 'wb') as output_pdf:
            writer.write(output_pdf)
        current_size = os.path.getsize(output_file)
        print(f"Saved: {output_file} ({current_size / (1024 * 1024):.2f} MB)")

    print(f"PDF split into {part_number} parts, saved in '{output_folder}'.")
