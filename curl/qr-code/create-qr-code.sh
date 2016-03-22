#!/bin/bash
#------------------------------------------------------------------------------
# USE: create-qr-code.sh <DATA> [<SIZE>] [<FILENAME>]
#------------------------------------------------------------------------------
# Uses <https://documentalchemy.com/> to create an image containing a QR code
# encoding the specified DATA.
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# SET UP DEFAULTS
#------------------------------------------------------------------------------
# Set your Document Alchemy API key here (or pass as an env var).
# Sign up at <https://documentalchemy.com/> to get your free API key.
DA_API_KEY=${DA_API_KEY:-"EDs2UQEprGn9aD4vg6HCPhFvgQFDahQgRzzIfocJ"}
DATA=$1
SIZE="400"
OUTFILE="qr.png"

#------------------------------------------------------------------------------
# SOME UTILITY METHODS
#------------------------------------------------------------------------------
# show_help - print a usage message
show_help () {
  echo ""
  echo "Use: create-qr-code.sh <DATA> [<SIZE>] [<FILENAME>]"
  echo ""
  echo "Set DA_API_KEY to your DocumentAlchemy API key value."
  echo "(Currently \"$DA_API_KEY\".)"
  echo ""
  echo "For example:"
  echo "  create-qr-code.sh \"http://example.com/\""
  echo "or"
  echo "  create-qr-code.sh \"http://example.com/\" link.png"
  echo "or"
  echo "  create-qr-code.sh \"http://example.com/\" 100"
  echo "or"
  echo "  create-qr-code.sh \"http://example.com/\" 100 link.png"
  echo "or"
  echo "  DA_API_KEY=MY_API_KEY create-qr-code.sh \"http://example.com/\" 100 link.png"
  echo ""
}
# is_int - returns '1' if $1 is an integer
is_int () {
  RE='^[0-9]+$'
  if ! [[ $1 =~ $RE ]] ; then
    echo 0;
  else
    echo 1;
  fi
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
# PARSE COMMAND LINE ARGUMENTS
#------------------------------------------------------------------------------
if [ "$#" -eq "2" ]; then
  if [ "`is_int $2`" -eq "1" ]; then
    SIZE=$2
  else
    SIZE="200"
    OUTFILE=$2
  fi
elif [ "$#" -gt "2" ]; then
  OUTFILE=$3
fi

#------------------------------------------------------------------------------
# EXECUTE REQUEST
#------------------------------------------------------------------------------
curl --silent \
     -H "Authorization: da.key=$DA_API_KEY" \
     -G https://documentalchemy.com/api/v1/data/-/rendition/qr.png \
     --data-urlencode "data=$DATA" \
     --data-urlencode "size=$SIZE" \
     -o "$OUTFILE"
