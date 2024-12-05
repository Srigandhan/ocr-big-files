"""
 Test version for processing big size pdfs.
"""

import os
import time
from split_pdf import split_pdf
from ocr_pdf import OcrPDF
from merge_pdf import merge_pdfs


def calculate_time_taken(start_time, message):
    """
    Print the time taken for a particular task / overall processing of the pdf
    """
    end_time = time.time()  # Record the end time
    total_time = end_time - start_time
    print(message, " Check Below Stats")
    print(f"The function took {total_time:.2f} seconds to execute.")
    print(f"That's {total_time / 60:.2f} minutes overall.")
    print("##"*100)

def process_pdf(input_file_path):
    """
    Splits, perform ocr, merge pdfs
    """
    overall_start_time = time.time()

    input_dir = os.path.splitext(input_file_path)[0]
    output_dir = os.path.join(input_dir,"ocred")
    output_file = os.path.join(output_dir, 'merged_output.pdf')

    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # split the pdfs into smaller chunks of less than 50 mb each.
    print("##"*100)
    start_time = time.time()
    split_pdf(input_file_path)
    calculate_time_taken(start_time, "Splitting pdfs to smaller chunks is completed.")


    # perform adobe ocr on all of the split files
    pdf_files  = [file for file in os.listdir(input_dir) if file.lower().endswith('.pdf')]
    print(pdf_files)
    print("##"*100)
    start_time = time.time()
    for f in pdf_files:
        input_file_path = os.path.join(input_dir, f)
        output_file_path = os.path.join(output_dir, f)
        # print(input_file_path, output_file_path)
        OcrPDF(input_file_path, output_file_path)
    calculate_time_taken(start_time, "OCR Processing of all the splited pdfs are completed.")


    # merge all the ocred results into one pdf.
    print("##"*100)
    start_time = time.time()
    merge_pdfs(output_dir, output_file)
    calculate_time_taken(start_time, "Merging ocred pdfs to one file is completed.")

    calculate_time_taken(overall_start_time, "Overall Split, OCR and Merge Completed.")

if __name__ == "__main__":
    FILE_PATH = "./input/output-5.pdf"
    process_pdf(FILE_PATH)
