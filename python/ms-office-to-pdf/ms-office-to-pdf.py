#!/usr/bin/env python

# Converts a Microsoft Office document to PDF in Python using the DocumentAlchemy API.
# python ms-office-to-pdf.py <API-KEY> <OFFICE-DOC> [<PDF-DOC>]
# See the README or visit:
#  https://documentalchemy.com/api-doc
# for more information.

# IMPORTS

import sys       # used to read command line arguments and set exit codes
import requests  # used for actual HTTP(S) transcations
import shutil    # used for easily writing files to disk
import os.path   # used to check if a file exists

# CONFIGURATION PARAMETERS

# See the DocumentAlchemy API documentation at
#   https://documentalchemy.com/api-doc
# for more information about these methods and
# their parameters.

# URLs - here are the URLs we'll be visiting during the
#        execution of this program.  The `{FOO}` tokens
#        are placeholders that we'll replace below.
URL_BASE            = "https://documentalchemy.com/api/v1"
CONVERT_TO_PDF_PATH = "/document/-/rendition/pdf"


VERBOSE = True

# CONVERT_TO_PDF

# Using the specified `api_key`, submit a request to the DocumentAlchemy API
# that creates (and returns) a PDF rendition of the provided `office_doc`. The
# file is saved in a local file as specified by `pdf_doc` (which may be `None`).
# Returns the `pdf_doc` value. Raises an exception if a problem occurs with the
# HTTP request.
def convert_to_pdf(api_key, office_doc, pdf_doc):
  if pdf_doc is None:
    pdf_doc = "document.pdf"
  url = URL_BASE + CONVERT_TO_PDF_PATH;
  headers = { "Authorization":"da.key="+api_key }
  office_doc_data = open( office_doc, "rb" )
  files = [("document",(office_doc,office_doc_data))]
  res = requests.post( url, headers=headers, files=files, stream=True)
  res.raise_for_status()
  with open(pdf_doc, 'wb') as f:
      res.raw.decode_content = True
      shutil.copyfileobj(res.raw, f)
  return pdf_doc

# SANITY CHECK

# If we don't have all of the command line parameters, print a
# usage message and exit...
if len(sys.argv) < 3:
  print "USE: <API-KEY> <OFFICE-DOC> [<PDF-DOC>]"
  sys.exit(1)
else:

# ...otherwise continue.

  # READ COMMAND-LINE PARAMETERS
  api_key    = sys.argv[1]
  office_doc = sys.argv[2]
  if len(sys.argv) > 3:
    pdf_doc  = sys.argv[3]
  else:
    pdf_doc  = None # let `convert_to_pdf` determine the name

  # CONFIRM THAT THE INPUT FILE exists
  if not (os.path.isfile(office_doc)):
    print "File " + office_doc + " not found. Aborting."
    sys.exit(2)

  else:
    # EXECUTE REQUEST
    if VERBOSE:
      print "Submitting " + office_doc + " for conversion to PDF..."
    pdf_doc = convert_to_pdf(api_key, office_doc, pdf_doc)
    if VERBOSE:
      print "...Success! Generated PDF saved as " + pdf_doc + "."
    sys.exit(0)
