## Watermarking a PDF document with a QR code

In this example we will follow a two-step process to first create (and store) an
image of a QR code and then use that image to watermark a PDF document.

This example demonstrates several features of the Document Alchemy API:

  1. How to create a QR code image.

  2. How to create a document directly within the Document Alchemy file-store.

  3. How to use a stored document within another API call.

  4. How to watermark a PDF document (using a stored image and an uploaded PDF file).

  5. How to delete a file from the Document Alchemy file-store.

### Installing

(These instructions assume you've already installed a modern version of
Node.js/IO.js.  If you haven't yet, see <https://nodejs.org/> for details.)

To simplify the task, this example uses the popular
[request](https://www.npmjs.com/package/request) module (on GitHub at
[request/request](https://github.com/request/request)).

To install the module, simply run:

```bash
npm install
```

from within this directory (the one containing `package.json` and this README
file).  This will download and install all of the necessary third-party
libraries.

### Running

To run this example, you will need:

  1. A DocumentAlchemy API key.  If you don't have one yet, you can obtain one immediately
     by [signing up for DocumentAlchemy](https://documentalchemy.com/pricing?s=ghsc).

  2. A PDF document to watermark.

The general format for running this program is this:

```bash
node qr-watermark.js <API-KEY> <TEXT-TO-ENCODE> <PDF-TO-WATERMARK> [<OUTPUT-FILE-NAME>]
```

For example, if your API key value is `HbblCNv7gLN2pasWFK44`, the command:

```bash
node qr-watermark.js HbblCNv7gLN2pasWFK44 "http://www.example.com/" myDocument.pdf watermarkedDocument.pdf
```

will create (or overwrite) the file `watermarkedDocument.pdf`, containing a copy
of `myDocument.pdf` with a QR code (pointing to www.example.com) stamped on
every page.

The output of the program may look something like this:

```
Creating the QR code...
...Success! Created and stored QR code as document ID "8cxwka1gbjoflxrqi2ux2z2".
Watermarking the PDF document using that stored image...
...Success! Watermarked PDF document saved at "watermarkedDocument.pdf".
Deleting the QR code...
...Success! Stored document deleted from the server.
```

(Note that `qr-watermark.js` is also directly executable via:

```bash
qr-watermark.js <API-KEY> <TEXT-TO-ENCODE> <PDF-TO-WATERMARK> [<OUTPUT-FILE-NAME>]
```

if your shell recognizes the `#!/usr/bin/env node` hash-bang identifier.)

### How it works

Please review the code and comments found in `qr-watermark.js` for a detailed
explanation of the process.
