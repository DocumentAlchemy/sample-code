#!/usr/bin/env node

// IMPORTS

var fs                = require('fs');      // (a standard module)
var request           = require('request'); // (via https://www.npmjs.com/package/request)


// CONFIGURATION PARAMETERS

// See the DocumentAlchemy API documentation at
//   https://documentalchemy.com/api-doc#!/DocumentAlchemy
// for more information about these methods and
// their parameters.

var URL_BASE          = "https://documentalchemy.com/api/v1";
var QR_PATH           = "/data/-/rendition/qr.png";
var WATERMARK_PATH    = "/document/-/watermark/{WATERMARK_DOC_ID}/rendition/pdf";
var DELETE_FILE_PATH  = "/document/{DOC_ID}";

var QR_SIZE           = 400;
var QR_TTL            = 20*60; // 20 minutes

var WATERMARK_OPACITY = "0.8"
var WATERMARK_GRAVITY = "sw"
var WATERMARK_MARGIN  = 150
var WATERMARK_SIZE    = 20
var WATERMARK_UNIT    = "percent"


// METHODS

// **createQRCode**
// Use the given `apiKey` to create a QR code image encoding the given `data`.
// The image will be stored in the DocumentAlchemy file-store. When processing
// is complete, the `callback` method is invoked. The callback method should
// have the signature `(err,doc)` where `err` contains an error or exception
// that was encountered (if any) and `doc` contains a DocumentAlchemy document
// identifier object describing the stored file.
function createQR(apiKey, data, callback) {

  // Assemble the URL.
  var url = URL_BASE + QR_PATH;
  url += "?data=" + encodeURIComponent(data);
  url += "&size=" + QR_SIZE;
  url += "&store=true"
  url += "&ttl=" + QR_TTL;

  // Configure the params to send to `request`. Note that we're submitting the
  // given `apiKey` in an HTTP request header.  Here we use the form:
  //      Authorization: da.key=<API-KEY>
  // but we could also use (the OAuth2 access-token syntax):
  //      Authorization: Bearer <API-KEY>
  // or, we could include the API key in a query string parameter named
  // `da.key` instead.
  var params = {
    url: url,
    headers: { "Authorization": "da.key="+apiKey },
    json: true
  };

  // Execute the request, handling the response in callback.  If the request is
  // successful, we expect an HTTP 201 response. In that case we parse and
  // return the document identifier from the response body. If the request is
  // NOT successful, we'll callback with an error describing the response.
  var req = request.get(params, function(err,response,body) {
    if (err) {
      callback(err);
    } else if (response.statusCode == '201') {

      // If the body isn't already an object, parse it now. (This method isn't
      // technically necessary because the `json:true` parameter passed to
      // request will force the response body to be interpreted as a JSON
      // document, but it's a good defenisve programming step so we'll do it
      // anyway.)
      if(body && typeof body === 'string') {
        body = JSON.parse(body);
      }
      callback(null, body);

    } else {
      callback(new Error("Expected HTTP 201, found "+response.statusCode+"."));
    }
  });
  req.end();
}


// **watermarkPDF**
// Use the given `apiKey` to submit a request to DocumentAlchemy to create a
// watermarked document from the specified `watermarkDocId` (already stored on
// the server) and the specified (local) `pdfFile`.  Save the returned document
// at `outputFile` When processing is complete, the `callback` method is
// invoked. The callback method should have the signature `(err,outputFile)`
// where `err` contains an error or exception that was encountered (if any) and
// `outputFile` describes the file to which the generated document was saved.
function watermarkPDF(apiKey, watermarkDocId, pdfFile, outputFile, callback) {

  // Assemble the URL.
  var url = URL_BASE + WATERMARK_PATH;
  // Replace the `{WATERMARK_DOC_ID}` token with the actual document id.
  url = url.replace("{WATERMARK_DOC_ID}",watermarkDocId);
  url += "?gravity="+WATERMARK_GRAVITY;
  url += "&margin="+WATERMARK_MARGIN;
  url += "&opacity="+WATERMARK_OPACITY;
  url += "&w="+WATERMARK_SIZE;
  url += "&unit="+WATERMARK_UNIT;

  // Configure the params to send to `request`. Note that once again we submit
  // the `apiKey` as an HTTP request header. Also note that we're using
  // `request`'s `formData` parameter to upload the PDF file (within the body of
  // the HTTP request), under the name `document`.
  var params = {
    url: url,
    headers: { "Authorization": "da.key="+apiKey },
    formData: {
      document: fs.createReadStream(pdfFile),
    }
  };

  // Create an output stream to write to.
  var out = fs.createWriteStream(outputFile);

  // Submit the request and pipe the results to the file.
  var req = request.post(params)
  req.pipe(out);
  // Finally callback with the name of the newly created file.
  req.on('end',function(){
    callback(null,outputFile);
  });
}


// **deleteStoredFile**
// Use the given `apiKey` to delete the (previously stored) document with the
// specified `docId`. When processing is complete, the `callback`
// method is invoked. The callback method should have the signature `(err)`
// where `err` contains an error or exception that was encountered (if any).
function deleteStoredFile(apiKey, docId, callback) {

  // Assemble the URL.
  var url = URL_BASE + DELETE_FILE_PATH;
  // Replace the `{WATERMARK_DOC_ID}` token with the actual document id.
  url = url.replace("{DOC_ID}",docId);

  // Configure the params to send to `request`. Note that once again we submit
  // the `apiKey` as an HTTP request header.
  var params = {
    url: url,
    headers: { "Authorization": "da.key="+apiKey },
  };

  // Submit the request and callback (with the error if any).
  request.del(params,function (err,response,body) {
    callback(err);
  });
}


// MAIN
// This is the "main" method that is invoked when this file is executed.

if (process.argv.length < 4) {

  // First we perform a sanity check to make sure we have all of the command
  // line parameters we'll need.
  console.error("USE: <API-KEY> <TEXT-TO-ENCODE> <PDF-TO-WATERMARK> [<OUTPUT-FILE-NAME>]");
  process.exit(1);

} else {

  // Next we parse the command line parameters (and fill in default values
  // if needed.)
  var qrCodeDocument = null;
  var apiKey         = process.argv[2];
  var data           = process.argv[3];
  var inputFile      = process.argv[4];
  var outputFile     = "watermarked.pdf"
  if (process.argv.length > 5) {
    outputFile = process.argv[5];
  }

  // Then we create the QR code using the `createQR` method described above.
  // The id of the stored file is stored in `qrCodeDocument`.
  console.log("Creating the QR code...");
  createQR(apiKey, data, function(err,json) {
    if (err) {
      console.error("ERROR while processing createQRCode:",err)
      process.exit(2)
    } else {
      qrCodeDocument = json;
      console.log("...Success! Created and stored QR code as document ID \""+qrCodeDocument.document.id+"\".");
      console.log("Watermarking the PDF document using that stored image...");

      // Next we submit the PDF document to watermark, using the `watermarkPDF`
      // method described above.
      watermarkPDF(apiKey,qrCodeDocument.document.id, inputFile, outputFile, function(err,outfile) {
        if (err) {
          console.error("ERROR while processing watermarkPDF:",err);
          process.exit(3);
        } else {
          console.log("...Success! Watermarked PDF document saved at \""+outfile+"\".");

          // Finally we delete the QR code image we stored above. We don't
          // technically need to do this. The stored document will expire on its
          // own after `QR_TTL` seconds, but we're done with the image so we
          // might as well delete it.
          console.log("Deleting the QR code...");
          deleteStoredFile(apiKey, qrCodeDocument.document.id, function(err) {
            if (err) {
              console.error("ERROR while processing deleteStoredFile:",err);
              process.exit(4);
            } else {
              console.log("...Success! Stored document deleted from the server.");
            }
          }); // end of the deleteStoredFile callback

        }
      }); // end of the watermarkPDF callback

    }
  }); // end of the createQR callback

} // end of the "sanity check" else block
