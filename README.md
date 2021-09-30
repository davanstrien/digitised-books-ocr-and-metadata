# Digitised Books c. 1510 - c. 1900 : JSONL (OCR derived text & metadata)

<img align="left" src="https://user-images.githubusercontent.com/8995957/135487545-fa1508a8-6408-45a5-97fd-4234ca034c8b.jpg">

> In partnership with Microsoft, the British Library has digitized, and made freely available under Public Domain Mark, over 60,000 volumes (around 25 million pages) of out of copyright 18th & 19th century texts. Items within this collection cover a wide range of subject areas including geography, philosophy, history, poetry and literature and are published in a variety of languages.  - [source](https://www.bl.uk/collection-guides/digitised-printed-books)

As part of this process, [Optical Character Recognition](https://en.wikipedia.org/wiki/Optical_character_recognition) (OCR) was applied to the collection. OCR produces 'machine readable' text from the images of the pages. 

The OCR from these books have been available via [data.bl.uk](https://data.bl.uk/) in two formats:
- [Analysed Layout and Text Object](https://www.loc.gov/standards/alto/) (ALTO) [Extensible Markup Language](https://en.wikipedia.org/wiki/XML) (XML) format.
- As a set of [JavaScript Object Notation](https://en.wikipedia.org/wiki/JSON) (JSON) files.
 
This repository contains two things:
Notebooks transform the ALTO version into newline delimited JSON (described more below) and update and add new metadata exported from the British Library catalogue. 
- documentation for this new dataset. 

Since you might not be interested in the process of creating the dataset, we start with the data documentation. 

## Data documentation 

The structure of the data looks like this:

```
1510_1699/
    1634_003194022.jsonl.gz
    1634_003194023.jsonl.gz
    ...
```


The collection is broken down into different subcollections based on the year in which the item was published. If the year is unknown for an item, then it will be stored under 'unknown'. 

Inside each sub-collection directory are the files which contain the digitized books. Each file represents one resource (usually a book) from the collection. For example, `1634_003194022.jsonl.gz` represents one item. 

Each line of the `jsonl` file represents a page in the book (more on this format below).

### File naming

The file naming is structured as follows:

 `{year}_{ID}.jsonl`

If the year is unknown, the year will be `unknown` instead of a number. i.e.  `{unkown}_{ID}.jsonl` 

### Data format

This section explains how each file is organized in more detail. 

#### JSONL
The data is stored as [newline-delimited JSON](https://jsonlines.org/), also referred to as `jsonl`. 

This format contains `JSON` objects delimited by a new line. Such as

```
{Animal: "cat", "noise": "meow"}
{Animal: "dog", "noise": "woof"}
```

This format can help work with large amounts of data because it allows for reading data in a streaming manner, one line at a time. Reading text one line at a time means that you can process even large datasets (i.e. multiple GBs)  with "normal" amounts of memory. This format can also be loaded easily by many standard software libraries, which researchers commonly use, for example, the Python library pandas. 

Each line of `JSON` has several keys and values. The keys are the same across all files, but the values may not always be present. In this case, the value will be `null`.

The fields included in this dataset are:

- "record_id": This is a British Library ID for the item 
- "date":  This is a parsed `year` for the item. i.e. `1850`
- "raw_date": This is the unprocessed version of the data, i.e. `1850-`
- "title": This is the title for the book, i.e. `Documents connected with the history of South Carolina. Edited by P. C. J. W`
- "place": This is a place of publication, i.e. `London`
- "empty_pg": This is a boolean value that indicates if the OCR software detected any text on the page, i.e. `True` or `False.`
- "text": Either this is `null` or contains the OCR text for that page, i.e. `It was the best of times...`
- "pg": The page in the resource, i.e. `100`.
- "mean_wc_ocr": This contains the mean "word confidence" given by the OCR software for each word on the page. i.e. `0.8`
- "std_wc_ocr": This contains the standard deviation of the word confidences, i.e. `0.1`.
- "Name": This is the first "name" associated with the resource (primarily the author of the text), i.e. `Mary Shelley` 
- "All names": This is all of the names associated with the book. 
- "Publisher": This is the publisher of the book. 
- "Country of publication 1": The first Country associated with the book, i.e. `England`.
- "All Countries of publication": All countries associated with the book 
- "Physical description": The physical description of the book/item 
- "Language_1": The first language associated with the book/item 
- "Language_2": The second language associated with the book/item
- "Language_3": The third language associated with the book/item
- "Language_4": The fourth language associated with the book/item
- "multi_language": if the book contains multiple languages, i.e. `True` or `False`.

An example of one row, i.e. one page loaded as a Python Dictionary:

```python
{'record_id': '003898176',
 'date': '1856',
 'raw_date': '1856',
 'title': 'Documents connected with the history of South Carolina. Edited by P. C. J. W',
 'place': 'London',
 'empty_pg': True,
 'text': None,
 'pg': 1,
 'mean_wc_ocr': None,
 'std_wc_ocr': None,
 'Name': 'Weston, Plowden Charles Jennett',
 'All names': 'Weston, Plowden Charles Jennett [person]',
 'Publisher': None,
 'Country of publication 1': 'England',
 'All Countries of publication': 'England',
 'Physical description': None,
 'Language_1': 'English',
 'Language_2': None,
 'Language_3': None,
 'Language_4': None,
 'multi_language': False}
```

#### Compression

The data has been compressed at two levels:
- the folder level, i.e. each folder containing a group of dates, is compressed 
- the file level, i.e. each `jsonl` file containing a book from the dataset is compressed

Both of these levels of compression use the `gzip` format to compress the data. Some processing software can use the gzip compression format directly, so it won't always be necessary to decompress the data entirely to work with it. For example, the `pandas` Python library can read `gzip` compressed files directly. Keeping the files compressed saves space for storing files and improves performance in some situations since less I/O is required to process each file. 

#### A note on OCR quality 

The data contains two fields related to OCR quality: `mean_wc_ocr`, and `std_wc_ocr`. These fields are included to help give users of the data *some* sense of the quality of the OCR. However, these measures should be treated with some scepticism. There are some potential challenges both to the OCR quality itself and the scores because of several features of the data:

- the data contains non-English text: some languages may be parsed more poorly by OCR software.
- the data covers a broad time period: 
    - the original pages may have damage to them, resulting in OCR errors
    - the language (including English) may be different from contemporary languages for which most OCR engines are optimized. 
- some of the books may include images, tables, or other challenging layouts, which can cause issues for the quality of OCR. 

---

# Background information 

This section contains more background information on how and why this new version of the data was created.

## Why create this new version of the dataset? 

The original format output by the OCR software is ALTO XML. Whilst this format works well for many applications, it is less suitable for some types of work with this kind of data. For example, the ALTO XML contains coordinates for words. Whilst this information is helpful for some applications; it's isn't necessary for all potential users of the BL books dataset. 

The ALTO format can be less suitable for work that seeks to use this collection 'at scale,' i.e. work with large proportions or all of this data. Similarly, the data in the ALTO is less suitable for using this collection for data science and Natural Langage Processing work.

A JSON version of the data is currently available via the British Library Research Repository [https://doi.org/10.21250/db14](). This JSON version is easier to work with but contains less metadata than the ALTO XML. The processing notebooks here aim to produce a new version of the BL books dataset that offers compromises the usability and completeness of the data.

In particular, this new dataset aims to make it practical for researchers with relatively limited computational resources to be still able to work with the complete collection of resources. This repository is shared to show the processing steps so others can see the lineage of this new dataset and to allow others to check for errors in the processing steps and/or process the collections differently to match their requirements. 

## How was the dataset created?
The processing takes place in a series of notebooks: 

- [00_download_process_alto.ipynb]() covers the process of downloading and parsing text and some metadata from the ALTO XML files and creating the initial JSONL version of the dataset. 
- [01_metadata_exploration.ipynb]() explores metadata available for these books from the British Library catalogue and identifies metadata fields to add/update in the JSONL dataset
- [02_update_metadata.ipynb]() does the actual update of the existing metadata and prepares the dataset for upload to the British Library repository. 



---
Image source: [flickr](https://flic.kr/p/i18QFb) 
