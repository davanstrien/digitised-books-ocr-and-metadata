# BL Books ALTO to JSONL + metadata processing notebooks

## What?

> 49,455 books (and other resources ) were digitised with funding from Microsoft, equating to 65,227 volumes (over 23 million pages), published largely between the 18th and 19th Century. The books cover a wide range of subject areas including philosophy, history, poetry and literature. 

As part of this project, Optical Character Recognition (OCR) was applied to the collection. OCR produces 'machine readable' text from the images of the pages. 

The OCR from these books have been available via `data.bl.uk` in two formats:
- Analysed Layout and Text Object (ALTO) Extensible Markup Language (XML) format.
- As a set of JavaScript Object Notation (JSON) files.
 
This repository contains notebooks that transform the ALTO version into newline delimited JSON (described more below) and updates and adds new metadata exported from the British Library catalogue. 

## Why?

The original format output by the OCR software is ALTO XML. Whilst this format works well for many applications, it is less suitable for some types of work with this kind of data. For example, the ALTO XML contains coordinates for words. Whilst this information is helpful for some applications, it's isn't necessary for all potential users of the BL books dataset. 

The ALTO format can be less suitable for work that seeks to utilise this collection 'at scale,' i.e. work with large proportions or all of this data. Similarly, the data in the ALTO is less suitable for using this collection for data science and Natural Langage Processing work.

The JSON file current available via data.bl are easier to work with but contain much less metadata than the ALTO XML. The processing notebooks here aim to produce a new version of the BL books dataset that compromises the usability and completeness of the data. 

In particular, this new dataset aims to make it practical for researchers with relatively limited computational resources to be still able to work with the complete collection of resources. This repository is shared to show the processing steps so others can see the lineage of this new dataset and to allow others to check for errors in the processing steps and/or process the collections differently to match their requirements. 

## How?
The processing takes place in the following notebooks: 


## Data documentation 

The collection is broken down into different subcollections based on the year in which the item was published. If the year is unkown for an item then it will be stored under 'unknown'. 

Inside each subcollection directory are the files which contains the digitised books. Each file represents one resource (usually a book) from the collection. For example `1634_003194022.jsonl.gz` represents one item. 

Each line of the `jsonl` file represents a page in the book (more on this format below).

### File naming

The file naming is structured as follows:

 `{year}_{ID}.jsonl`

If the year is unknown, year will be `unknown` instead of a number. 


### Data format

#### JSONL
The data is stored as newline-delimited JSON also referred to as `jsonl`. 

This format contains json objects delimited by a new line. Such as

```
{Animal: "cat", "noise": "meow"}
{Animal: "dog", "noise": "woof"}
```


This format can be useful for working with large amounts of data because it allows for reading data in a streaming manner one line at a time. This means that even very large datasets (i.e. multiple GBs) can be processed with "normal" amounts of memory. This format can also be loaded easily by many common Python Libraries, for example Pandas. 

Each line of JSON has a number of keys and values. The keys are the same across all of the files but the values may not always b present, in this case the value will be `null`.

The fields included in this dataset are:

- "record_id": This is a British Library ID for the item 
- "date":  This is a parsed `year` for the item. i.e. `1850`
- "raw_date": This is the unprocessed version of the data i.e. `1850-`
- "title": This is the title for the book i.e. `Documents connected with the history of South Carolina. Edited by P. C. J. W`
- "place": This is a place of publication i.e. `London`
- "empty_pg": This a boolean value which indicates if the OCR software detected any text on the page i.e. `True` or `False`
- "text": Either this is `null` or contains the OCR text for that page i.e. `It was the best of times...`
- "pg": The page in the resource i.e. `100`
- "mean_wc_ocr": This contains the mean "word confidence" given by the OCR software for each word on the page. i.e. `0.8`
- "std_wc_ocr": This contains the standard deviation of the word confidences i.e. `0.1`
- "Name": This is the first "name" associated with the resource (primiarly the author of the text) i.e. `Mary Shelley` 
- "All names": This is all of the names associated with the book. 
- "Publisher": This is the publisher of the book. 
- "Country of publication 1": The first Country associated with the book i.e. `England` 
- "All Countries of publication": All countries associated with the book 
- "Physical description": The physical descripton of the book/item 
- "Language_1": The first language associated with the book/item 
- "Language_2": The second language associated with the book/item
- "Language_3": The third language associated with the book/item
- "Language_4": The fourth language associated with the book/item
- "multi_language": if the book contains multiple languages i.e. `True` or `False`

An example of one row i.e. one page loaded as a Python Dictionary:

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

##### Compression

The data is compressed at two levels:
- the folder level i.e. each folder containing a group of dates is compressed 
- the file level i.e. each `jsonl` file containing a book from the dataset is compressed

Both of these levels of compression use the `gzip` format to compress the data. The gzip compression format can be used directly by some processing software so it won't always be necessary to fully decompress the data for working with it. For example, it is possible for the `pandas` Python library to read `gzip` compressed files directly. This can be useful for saving space for storing files and can improve performance in some situations since less I/O is required to process each file. 

