#!/usr/bin/env python

# Stamps a QR code on every page of a PDF document.
# USAGE: python qr-watermark.py <API-KEY> <TEXT-TO-ENCODE> <PDF-TO-WATERMARK> [<OUTPUT-FILE-NAME>]
# See the README or visit:
#  https://documentalchemy.com/api-doc
# for more information.

# IMPORTS

import sys       # used to read command line arguments and set exit codes
import requests  # used for actual HTTP(S) transcations
import shutil    # used for easily writing files to disk

# CONFIGURATION PARAMETERS

# See the DocumentAlchemy API documentation at
#   https://documentalchemy.com/api-doc
# for more information about these methods and
# their parameters.

# URLs - here are the URLs we'll be visiting during the
#        execution of this program.  The `{FOO}` tokens
#        are placeholders that we'll replace below.
URL_BASE          = "https://documentalchemy.com/api/v1"
QR_PATH           = "/data/-/rendition/qr.png"
WATERMARK_PATH    = "/document/-/watermark/{WATERMARK_DOC_ID}/rendition/pdf"
DELETE_FILE_PATH  = "/document/{DOC_ID}"

# QR_* - here are a couple of parameters to configure the
#        QR code generation.
QR_SIZE           = 400
QR_TTL            = 20*60; # 20 minutes

# WATERMARK_* - here are a few parameters that specify the
#               size, placement and opacity of the watermark
WATERMARK_OPACITY = "0.8"
WATERMARK_GRAVITY = "sw"
WATERMARK_MARGIN  = 150
WATERMARK_SIZE    = 20
WATERMARK_UNIT    = "percent"

# METHODS

# CREATE_QR_CODE
# Using the specified `api_key`, submit a request to the DocumentAlchemy API
# that creates (and stores) a QR code encoding the given `data`. (The size of
# the QR code is determined by the `QR_SIZE` variable defined above.)
# Returns the document identifier assigned to the QR code image.
def create_qr_code(api_key, data):
  url = URL_BASE + QR_PATH;
  qs = { "data":data, "size":str(QR_SIZE), "store":True, "ttl":str(QR_TTL) }
  headers = { "Authorization":"da.key="+api_key }
  res = requests.get( url, headers=headers, params=qs)
  res.raise_for_status() # raise an exception if the response wasn't a 2XX code
  json = res.json()
  return json["document"]["id"]


# WATERMARK_PDF
# Using the specified `api_key`, submit a request to the DocumentAlchemy API
# that creates (and returns) a rendition of the provided `pdf_file` with the
# image specified by `watermark_doc_id` stamped on every page. (The size,
# placement and opacity of the watermark image are determined by the
# `WATERMARK_*` attributes defined above.) The file is saved in a local file as
# specified by `output_file`. Returns the `output_file` value.
def watermark_pdf(api_key, watermark_doc_id, pdf_file, output_file):
  url = URL_BASE + WATERMARK_PATH;
  url = url.replace( "{WATERMARK_DOC_ID}", watermark_doc_id )
  headers = { "Authorization":"da.key="+api_key }
  pdf_data = open( pdf_file, "rb" )
  files = [("document",(pdf_file,pdf_data,"application/pdf"))]
  params = {
    "gravity": WATERMARK_GRAVITY,
    "margin":  WATERMARK_MARGIN,
    "opacity": WATERMARK_OPACITY,
    "w":       WATERMARK_SIZE,
    "unit":    WATERMARK_UNIT
    }
  res = requests.post( url, headers=headers, files=files, params=params, stream=True)
  res.raise_for_status()
  with open(output_file, 'wb') as f:
      res.raw.decode_content = True
      shutil.copyfileobj(res.raw, f)
  return output_file

# DELETE_STORED_DOCUMENT
# Using the specified `api_key`, submit a request to the DocumentAlchemy API x#
# that removes the document (file) specified by `doc_id` from the
# DocumentAlchemy file store.
def delete_stored_document(api_key, doc_id):
  url = URL_BASE + DELETE_FILE_PATH;
  url = url.replace( "{DOC_ID}", doc_id )
  headers = { "Authorization":"da.key="+api_key }
  res = requests.delete( url, headers=headers)
  res.raise_for_status()


# A "main" method that encapsulates the core driver of this program.
def main():

  # SANITY CHECK

  # If we don't have all of the command line parameters, print a
  # usage message and exit...
  if len(sys.argv) < 4:
    print "USE: <API-KEY> <TEXT-TO-ENCODE> <PDF-TO-WATERMARK> [<OUTPUT-FILE-NAME>]"
    sys.exit(1)

  else:

    # OTHERWISE CONTINUE WITH THE PRIMARY LOGIC

    # READ COMMAND-LINE PARAMETERS
    api_key    = sys.argv[1]
    data       = sys.argv[2]
    pdf        = sys.argv[3]
    if len(sys.argv) > 4:
      out_file = sys.argv[4]
    else:
      out_file = "watermarked.pdf"

    # GENERATE THE QR CODE
    print "Creating the QR code..."
    watermark_doc_id = create_qr_code(api_key,data)
    print "...Success! Created and stored QR code as document ID \"" + watermark_doc_id + "\"."

    # UPLOAD AND WATERMARK THE PDF DOCUMENT
    print "Watermarking the PDF document using that stored image..."
    output = watermark_pdf(api_key, watermark_doc_id, pdf, out_file)
    print "...Success! Watermarked PDF document saved locally at \"" + output + "\"."

    # DELETE THE STORED QR CODE
    # (This last step isn't strictly necessary. The file will be automatically
    # erased after `QR_TTL` seconds. But since we're done with the file we may as
    # well delete it now.)
    print "Deleting the stored QR code..."
    delete_stored_document(api_key,watermark_doc_id)
    print "...Success! Stored document deleted from the server."
    sys.exit(0)

# run it
main()
