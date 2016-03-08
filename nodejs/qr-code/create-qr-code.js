#!/usr/bin/env node

// Generates a PNG image containing a QR code encoding arbitrary data.
// USAGE: node create-qr-code.js <API-KEY> <DATA> [<FILENAME>]
// See the README or visit:
// https://documentalchemy.com/api-doc#!/DocumentAlchemy/get_data_rendition_qr_png
// for more information.

// IMPORTS
var fs = require('fs');       // Used to read and write files.
var https = require('https'); // Used to interact with the server.


// SANITY CHECK

// If we don't have all of the command line parameters, print a usage message
// and exit...
if (process.argv.length < 4) {
  console.error("USE: <API-KEY> <TEXT-TO-ENCODE> [<OUTPUT-FILE-NAME>]");
  process.exit(1);
// ...otherwise we perform the real work of the script.
} else {

  // "CONSTANTS"
  // First let's define some "constants" that we may want to change from time to
  // time, but that we won't expose as command line paramters. See
  // https://documentalchemy.com/api-doc#!/DocumentAlchemy/get_data_rendition_qr_png
  // for detailed documenation of the "GET QR Code" method we're using here.

  var HOST = "documentalchemy.com";
  var PORT = 443;
  var PATH = "/api/v1/data/-/rendition/qr.png";
  var SIZE = 100; // Image size in pixels - note that `400` is the default.
  var ECL  = 'L'; //   Error correction level (the amount of redundancy in
                  //   the encoded image), one of `L`, `M`, `Q`, `H`.
                  //   The default is `H`


  // COMMAND-LINE PARAMETERS
  var apiKey   = process.argv[2];
  var data     = process.argv[3];
  var fileName = null;
  if (process.argv[4]) {
    fileName   = process.argv[4];
  } else {
    fileName   = "qr-code.png";
  }

  // GENERATE THE REQUEST "OPTIONS" OBJECT
  // Now we have all the information we need to generate the request. Note that
  // we include our API Key value as an HTTP request header.
  url = PATH
  url += "?data=" + encodeURIComponent(data)
  url += "&size=" + SIZE
  url += "&ecl=" + ECL
  var options = {
    host: HOST,
    path: url,
    port: PORT,
    headers: { "Authorization": "da.key="+apiKey }
  };

  // EXECUTE THE REQUEST
  // Finally we execute the request, piping the response to a file (or reporting
  // an error if one is encountered).
  var req = https.get(options, function(res) {
    if (res.statusCode == '200') {
      var outputFile = fs.createWriteStream(fileName);
      res.pipe(outputFile);
      console.log("QR code image saved as \""+fileName+"\".");
    } else {
      console.error("Expected HTTP 200, found "+res.statusCode+".");
      process.exit(2);
    }
  });
  req.end();

}
