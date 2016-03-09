## Creating a QR Code in Node.js using DocumentAlchemy

This directory contains a simple example of using the DocumentAlchemy API to
generate and download a PNG image containing a QR code encoding arbitrary data.

There are no external dependencies (beyond Node itself).  Assuming you have
Node.js installed you can run the program via:

```bash
node create-qr-code.js <API-KEY> <TEXT-TO-ENCODE> [<OUTPUT-FILE-NAME>]
```

For example, if your API key value is `HbblCNv7gLN2pasWFK44`, the command:

```bash
node create-qr-code.js HbblCNv7gLN2pasWFK44 "https://documentalchemy.com"
```

will create a file (by default within the current working directory and named
`qr-code.png`) containing a QR code the encodes the URL
`https://documentalchemy.com`.  Scanning that QR code with your smartphone
should open the [DocumentAlchemy home page](https://documentalchemy.com) in
your browser.


(Note that `create-qr-code.js` is also directly executable via:

```bash
create-qr-code.js <API-KEY> <TEXT-TO-ENCODE> [<OUTPUT-FILE-NAME>]
```

if your shell recognizes the `#!/usr/bin/env node` hash-bang identifier.)
