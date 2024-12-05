# Test version for processing big size pdfs.

Entry Point --> process_pdf.py

Modifications needed:
process_pdf.py --> update the FILE_PATH to the pdf file you want to process.
ocr_pdf.py --> update the client_secret ( will be shared separately )


There were some issues with upload time and ssl CA cert verification with the package. If you are facing that, the source code needs few changes.
