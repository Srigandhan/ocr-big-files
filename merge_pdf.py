import time
import os
from PyPDF2 import PdfReader, PdfWriter

def merge_pdfs(input_dir, output_file):
    # Create a PdfWriter object for the merged PDF
    writer = PdfWriter()

    # Iterate through all files in the input directory
    for filename in sorted(os.listdir(input_dir)):
        if filename.lower().endswith('.pdf') and "merged_output" not in filename:
            pdf_file_path = os.path.join(input_dir, filename)
            reader = PdfReader(pdf_file_path)
            
            # Add each page of the current PDF to the writer
            for page in reader.pages:
                writer.add_page(page)

            print(f"Added {filename}")

    # Write the merged PDF to the output file
    with open(output_file, 'wb') as output_pdf:
        writer.write(output_pdf)

    print(f"Merged PDF saved as: {output_file}")
