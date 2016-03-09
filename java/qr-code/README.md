## Creating a QR Code in Java using DocumentAlchemy

This directory contains a simple example of using the DocumentAlchemy API to
generate and download a PNG image containing a QR code encoding arbitrary data.

There are no external dependencies (beyond Java and its core libraries).
Assuming you have Java installed you can compile the program via:

```bash
javac CreateQRCode.java
```

and then run the program via:

```bash
java CreateQRCode <API-KEY> <TEXT-TO-ENCODE> [<OUTPUT-FILE-NAME>]
```

For example, if your API key value is `HbblCNv7gLN2pasWFK44`, the command:

```bash
java CreateQRCode HbblCNv7gLN2pasWFK44 "https://documentalchemy.com"
```

will create a file (by default within the current working directory and named
`qr-code.png`) containing a QR code the encodes the URL
`https://documentalchemy.com`.  Scanning that QR code with your smartphone
should open the [DocumentAlchemy home page](https://documentalchemy.com) in
your browser.
