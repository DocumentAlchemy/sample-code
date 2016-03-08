## Creating a QR Code in PHP Using DocumentAlchemy

This directory contains a simple example of using the DocumentAlchemy API to
generate and download a PNG image containing a QR code encoding arbitrary data.

To run this example, edit `create-qr-code.php` to set your API key and the value
you'd like to encode in the QR code, then run:

```bash
php create-qr-code.php
```

This will generate a file (in the current working directory) named `qr-code.png`.

See the comments within `create-qr-code.php` or the document for
DocumentAlchemy's "create QR code" API method at
<https://documentalchemy.com/api-doc#!/DocumentAlchemy/get_data_rendition_qr_png>
for more information.
