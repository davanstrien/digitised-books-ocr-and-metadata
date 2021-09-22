# BL Books ALTO to JSONL + metadata processing notebooks

## What?

> 49,455 books were digitised with funding from Microsoft, equating to 65,227 volumes (over 23 million pages), published largely between the 18th and 19th Century. The books cover a wide range of subject areas including philosophy, history, poetry and literature. 

As part of this project Optical Chracter Recogniton (OCR) was applied to the collections. This produces 'machine readable' text from the images of the pages. 

The OCR from these books have been available via `data.bl.uk` in two formats:
- Analysed Layout and Text Object (ALTO) Extensible Markup Language (XML) format.
- As a set of JavaScript Object Notation (JSON) files.
 
This repository contains notebooks which transform the ALTO version of these files into newline delimited JSON (described more below) and updates and adds new metadata exported from the British Library catalogue. 

## Why?


## How?


## Data structure

- what?

Organization of data.

Each file contains is one book from the collection. Each line of the jsonl file represents a page in the book (more on this format below).

### File naming
- `{year}_{ID}.jsonl`

If year is unkown this will be `unk`


### Data format

#### JSONL
The data is stored as newline-delimited JSON also referred to as `jsonl`. 

This format contains json objects delimited by a new line. Such as

```
{Animal: "cat", "noise": "meow"}
{Animal: "dog", "noise": "woof"}
```


This format can be useful for working with large amounts of data because it allows for reading data in a streaming manner one line at a time. This means that even very large datasets (i.e. multiple GBs) can be processed with "normal" amounts of memory.  


##### Compression
The data is compressed at two levels:
- the folder level i.e. each folder containing a group of dates is compressed 
- the file level i.e. each `jsonl` file containing a book from the dataset is compressed

Both of these levels of compression use the `gzip` format to compress the data. The gzip compression format can be used directly by some processing software so it won't always be necessary to fully decompress the data for working with it. For example, it is possible for the `Pandas` Python library to read `gzip` compressed files directly. This can be useful for saving space for storing files and can improve performance in some situations since less I/O is required. 



## Processing notebook
from alto to jsonl format
