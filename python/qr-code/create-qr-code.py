#!/usr/bin/env python
# Generates a PNG image containing a QR code encoding arbitrary data.
# USAGE: python create-qr-code.py <API-KEY> <DATA> [<FILENAME>]
# See the README or visit:
#    https://documentalchemy.com/api-doc
# for more information.

# IMPORTS

import sys
import urllib2

# SANITY CHECK

# If we don't have all of the command line parameters, print a
# usage message and exit...

if len(sys.argv) < 3:
  print "USE: <API-KEY> <TEXT-TO-ENCODE> [<OUTPUT-FILE-NAME>]"
  sys.exit(1)
else:

    # DEFINE "CONSTANTS"
    # First let's define some "constants" that we may want to change from time to
    # time, but that we won't expose as command line paramters. See
    # https://documentalchemy.com/api-doc#!/DocumentAlchemy/get_data_rendition_qr_png
    # for detailed documenation of the "GET QR Code" method we're using here.
    URL_BASE    = "https://documentalchemy.com/api/v1"
    REST_METHOD = "/data/-/rendition/qr.png"
    SIZE        = 100  # Image size in pixels - note that `400` is the default.
    ECL         = "L"  # Error correction level (the amount of redundancy in
                    #   the encoded image), one of `L`, `M`, `Q`, `H`.
                    #   The default is `H`

    # READ COMMAND-LINE PARAMETERS
    api_key    = sys.argv[1]
    data       = sys.argv[2]
    if len(sys.argv) > 3:
      out_file = sys.argv[3]
    else:
      out_file = "qr-code.png"

    # SET UP REQUEST PARAMETERS
    url = URL_BASE + REST_METHOD
    url = url + "?size=" + str(SIZE)
    url = url + "&ecl=" + ECL
    url = url + "&data=" + urllib2.quote(data.encode("utf-8"))
    headers = [("Authorization","da.key=" + api_key)]

    # EXECUTE REQUEST
    opener = urllib2.build_opener()
    opener.addheaders = headers
    res = None
    f = None
    try:
      res = opener.open(url)
      if res.getcode() != 200:
        print "ERROR: Expected a 200 response, found " + res.getcode() + "."
        sys.exit(2)
      else:
        # READ DATA
        data = res.read()
        # WRITE DATA TO FILE
        f = open(out_file,"wb")
        f.write(data)
    except urllib2.HTTPError as e:
      print "ERROR: Unexpected HTTPError: " + str(e)
      sys.exit(3)
    finally:
      if res is not None:
        res.close()
        opener.close()
      if f is not None:
        f.close()
