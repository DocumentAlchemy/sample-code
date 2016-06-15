## Counting Words in a Microsoft Word or PDF Document in PHP

This directory contains a simple example of using the DocumentAlchemy API
to obtain a word count for a PDF or Word document.

There are no external dependencies (beyond PHP and its core libraries). Assuming
you have PHP installed you can run the program via:

```bash
php count-words.php <API-KEY> <FILE-TO-COUNT>
```

where `<API-KEY>` is your DocumentAlchemy API key (which you can obtain by
registering for DocumentAlchemy at https://documentalchemy.com/) and
`<FILE-TO-COUNT>` is the PDF or Word document you want to count the number
of words in.

For example, if your API key value is `HbblCNv7gLN2pasWFK44`, the command:

```bash
php count-words.php HbblCNv7gLN2pasWFK44 example.docx
```

will respond with the number of words in `example.docx`

See the comments within `count-words.php` or the [documentation for
DocumentAlchemy's API](https://documentalchemy.com/api-doc)
for more information.
