# bl_books_datasets

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
