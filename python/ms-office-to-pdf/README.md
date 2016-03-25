## Convert Microsoft Office Documents to PDF with Python

In this example we will demonstrate how to convert Microsoft Word (.doc, .docx),
Microsoft PowerPoint (.ppt,.pptx,.ppsx) and Microsoft Excel (.xls,.xlsx)
documents to PDF using Python and the DocumentAlchemy API.

(In fact, because DocumentAlchemy uses introspection of the documents submitted
to a common endpoint to determine the type of the "source" file, this same
program will also work for other document types such as Markdown or HTML.)

### Installing

(These instructions assume you've already installed Python 2.6+. If you haven't
yet, see <https://python.org/> for details.)

To simplify the task, this example uses the popular
[Requests](http://docs.python-requests.org/en/master/) module. You can install
it via [pip](https://pip.pypa.io/en/stable/) using `pip install requests`.
Otherwise see the [installation instructions for
Requests](http://docs.python-requests.org/en/master/user/install/) for more
detail or other options

### Running

To run this example, you will need:

  1. A DocumentAlchemy API key.  If you don't have one yet, you can obtain one immediately
     by [signing up for DocumentAlchemy](https://documentalchemy.com/pricing?s=ghsc).

  2. A MS Office document to convert.

The general format for running this program is this:

```bash
python ms-office-to-pdf.py <API-KEY> <OFFICE-DOC> [<PDF-DOC>]
```

For example, if your API key value is `HbblCNv7gLN2pasWFK44`, the command:

```bash
python ms-office-to-pdf.py HbblCNv7gLN2pasWFK44 myWord.docx myWord.pdf
```

will create (or overwrite) the file `myWord.pdf` with a PDF rendition of the
Word Document `myWord.docx`.

The name of the PDF file is optional.  When it is missing the generated document
will be named `document.pdf`.

(Note that `ms-office-to-pdf.py` is also directly executable via:

```bash
ms-office-to-pdf.py <API-KEY> <OFFICE-DOC> [<PDF-DOC>]
```

if your shell recognizes the `#!/usr/bin/env python` hash-bang identifier.)

### How it works

Please review the code and comments found in `ms-office-to-pdf.py` for a detailed
explanation of the process.
