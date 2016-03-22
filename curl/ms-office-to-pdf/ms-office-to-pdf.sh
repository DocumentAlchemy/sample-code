#!/bin/bash
#------------------------------------------------------------------------------
# USE: ms-office-to-pdf.sh <OFFICE-DOC> [<PDF-DOC>]
#------------------------------------------------------------------------------
# Uses <https://documentalchemy.com/> to create convert a Microsoft Office
# document to PDF.
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# SET UP DEFAULTS
#------------------------------------------------------------------------------
# Set your Document Alchemy API key here (or pass as an env var).
# Sign up at <https://documentalchemy.com/> to get your free API key.
DA_API_KEY=${DA_API_KEY:-"EDs2UQEprGn9aD4vg6HCPhFvgQFDahQgRzzIfocJ"}
OFFICE_DOC=$1
PDF_DOC="document.pdf"
if [ "$#" -gt "1" ]; then
  PDF_DOC=$2
fi

# SHOW_HELP - print a usage message
show_help () {
  echo ""
  echo "Use: ms-office-to-pdf.sh <OFFICE-DOC> [<PDF-DOC>]"
  echo ""
  echo "Set DA_API_KEY to your DocumentAlchemy API key value."
  echo "(Currently \"$DA_API_KEY\".)"
  echo ""
  echo "For example:"
  echo "  ms-office-to-pdf.sh MyDocument.docx"
  echo "or"
  echo "  ms-office-to-pdf.sh MyDocument.docx MyDocument.pdf"
  echo "or"
  echo "  DA_API_KEY=MY_API_KEY ms-office-to-pdf.sh MyDocument.docx MyDocument.pdf"
  echo ""
}

#------------------------------------------------------------------------------
# SANITY CHECK
#------------------------------------------------------------------------------
# Check for command line parameters and --help.
if [ "$#" -eq "0" ]; then
  show_help
  exit 1;
elif [[ $1 =~ ^--?(h(elp)?)|\?$ ]]; then
  show_help
  exit 0;
fi


#------------------------------------------------------------------------------
# CONFIRM THAT THE INPUT FILE EXISTS
#------------------------------------------------------------------------------
if ! [ -s "$OFFICE_DOC" ]; then
  echo "File \"$OFFICE_DOC\" not found."
  exit 2
fi

#------------------------------------------------------------------------------
# EXECUTE REQUEST
#------------------------------------------------------------------------------
response=$(curl --silent \
     --write-out %{http_code} \
     -H "Authorization: da.key=$DA_API_KEY" \
     -X POST \
     --form "document=@$OFFICE_DOC" \
      https://documentalchemy.com/api/v1/document/-/rendition/pdf \
     -o "$PDF_DOC")

#------------------------------------------------------------------------------
# CHECK RESPONSE
#------------------------------------------------------------------------------
if ! [ "$response" -eq "200" ]; then
  echo "Warning: Expected a 200 response, found $response instead.";
  exit 3;
fi
