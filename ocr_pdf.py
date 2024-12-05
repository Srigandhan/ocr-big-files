import logging
import os
import time
from datetime import datetime

from adobe.pdfservices.operation.auth.service_principal_credentials import ServicePrincipalCredentials
from adobe.pdfservices.operation.exception.exceptions import ServiceApiException, ServiceUsageException, SdkException
from adobe.pdfservices.operation.io.cloud_asset import CloudAsset
from adobe.pdfservices.operation.io.stream_asset import StreamAsset
from adobe.pdfservices.operation.pdf_services import PDFServices
from adobe.pdfservices.operation.pdf_services_media_type import PDFServicesMediaType
from adobe.pdfservices.operation.pdfjobs.jobs.ocr_pdf_job import OCRPDFJob
from adobe.pdfservices.operation.pdfjobs.result.ocr_pdf_result import OCRPDFResult

# Initialize the logger
logging.basicConfig(level=logging.INFO)


class OcrPDF(object):
    def __init__(self, input_file_path, output_file_path):
        try:
            file = open(input_file_path, 'rb')
            input_stream = file.read()
            file.close()

            # Initial setup, create credentials instance
            credentials = ServicePrincipalCredentials(
                client_id='6ab51e22352a4c9aa0b17a89b4de9233',
                client_secret='REPLACE_WITH_ACTUAL_PASSWORD'
            )

            # Creates a PDF Services instance
            pdf_services = PDFServices(credentials=credentials)

            # Creates an asset(s) from source file(s) and upload
            input_asset = pdf_services.upload(input_stream=input_stream,
                                              mime_type=PDFServicesMediaType.PDF)

            # Creates a new job instance
            ocr_pdf_job = OCRPDFJob(input_asset=input_asset)

            # Submit the job and gets the job result
            location = pdf_services.submit(ocr_pdf_job)
            pdf_services_response = pdf_services.get_job_result(location, OCRPDFResult)

            # Get content from the resulting asset(s)
            result_asset: CloudAsset = pdf_services_response.get_result().get_asset()
            stream_asset: StreamAsset = pdf_services.get_content(result_asset)

            # Creates an output stream and copy stream asset's content to it
            # output_file_path = self.create_output_file_path()
            with open(output_file_path, "wb") as file:
                file.write(stream_asset.get_input_stream())

        except (ServiceApiException, ServiceUsageException, SdkException) as e:
            logging.exception(f'Exception encountered while executing operation: {e}')
