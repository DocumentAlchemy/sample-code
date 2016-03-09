## Creating a QR Code in PHP Using DocumentAlchemy

This directory contains a simple example of using the DocumentAlchemy API to
generate and download a PNG image containing a QR code encoding arbitrary data.

There are no external dependencies (beyond PHP and its core libraries). Assuming
you have PHP installed you can run the program via:

```bash
php create-qr-code.php <API-KEY> <TEXT-TO-ENCODE> [<OUTPUT-FILE-NAME>]
```

For example, if your API key value is `HbblCNv7gLN2pasWFK44`, the command:

```bash
php create-qr-code.php HbblCNv7gLN2pasWFK44 "https://documentalchemy.com"
```
will create a file (by default within the current working directory and named
`qr-code.png`) containing a QR code the encodes the URL
`https://documentalchemy.com`.  Scanning that QR code with your smartphone
should open the [DocumentAlchemy home page](https://documentalchemy.com) in
your browser.


See the comments within `create-qr-code.php` or the documentation for
DocumentAlchemy's "create QR code" API method at
<https://documentalchemy.com/api-doc#!/DocumentAlchemy/get_data_rendition_qr_png>
for more information.
