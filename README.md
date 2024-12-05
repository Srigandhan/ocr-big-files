# Test version for processing big size pdfs.


## Python 3.10 Mandatory for using adobe api.  
  
  
## Installations:
```
pip install PyPDF2
pip install pdfservices-sdk
```

  
## Usage:
`python process_pdf.py`  
  
Modifications needed: Please do the below modification before running the script.  

```
process_pdf.py --> update the FILE_PATH to the pdf file you want to process.
ocr_pdf.py     --> update the client_secret ( will be shared separately )
```

  
## What it does:
* Splits the bigger pdf into smaller pdfs of almost equal size ( capped at 50 MB ). pypdf2 is used.
* Perform ocr on each of the small pdf using adobe api. The api gives us the texts embedded pdf to download and they have given proper python sdk for it with samples.
* Merge the ocred pdfs into one. pypdf2 is used.  
  
  
## Observations:
I have tested in windows with 16 GB ram. I have tested by processing 360 MB file. 
* The splitting is very fast within 2 3 secs.
* The ocr took about 1 to 1.5 minutes for each split and overall about 12 minutes. The returned ocred file size 10% of whats sent to the adobe api.
* The final merge completes less than a second as the file size got reduced. Te final size is about 30 MB.

The quality of the pdf looks good. OCR seems decent. We can compare the results against Azure OCR results for the same pdf. Although we dont want to replace Azure ocr at this time, this results tells us we should do compression of the image. The resultant size is so small. It will avoid any problem whatsover in downstream modules.  
  
### **Note**: I have not checked the quality and ocr for each page. So someone can spend some time to check it out and see if its good enough for using just for searchable pdfs.
  
Do try this out and let me know, if you need any help in running this. I used ACC file which was shared to me in the morning.
  
  

## Troubleshooting:
There were some issues with upload time and ssl CA cert verification with the package. If you are facing that, the source code needs few changes.  

```
File: <relative_path>\lib\site-packages\adobe\pdfservices\operation\internal\http\http_client.py
_execute_request function 
1. Change timeout = (http_request.connect_timeout, http_request.read_timeout) ->- timeout = (None, None) ( upload timeout issue )
2. Change all verify=True --> verify=False ( ssl CA not available in local system issue )
```

  
## Appendix:
I have tried to minimize the usage of the adobe api, as we need to upload and download large amount of data and we need to use paid version if we are implement this. So try out other things as per need.
  
In case you want to learn more or try out different things with adobe api for free. You can create your own credentials and use the samples they have provided.
https://developer.adobe.com/document-services/docs/overview/pdf-services-api/quickstarts/python/
https://github.com/adobe/pdfservices-python-sdk
https://github.com/adobe/pdfservices-python-sdk-samples
