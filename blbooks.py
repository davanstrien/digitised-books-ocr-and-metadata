mport json
import os
from sys import version
from typing import List, Optional, Tuple, Union
import datasets
from pathlib import Path
from dataclasses import dataclass
import gzip
import datasets

_CITATION = """\
@misc{TODO,
  author = {British Library Labs},
  title = {Digitised Books. c. 1510 - c. 1900},
  year = {2021},
  publisher = {British Library},
  howpublished={\\url{TODO},
}
"""




_DESCRIPTION = """\
The dataset comprises text created by OCR from the 49,455 digitised books, equating to 65,227 volumes (25+ million pages), published between c. 1510 - c. 1900. The books cover a wide range of subject areas including philosophy, history, poetry and literature. 
"""

_URL = "https://transfer.sh/7VWOPd/"
_URLS = {
    "1500_1600": "https://transfer.sh/get/7VWOPd/1510_1699.tar.gz",
    "1700_1799": "https://transfer.sh/get/6lHtHY/1700_1799.tar.gz",
}

features = datasets.Features(
    {
        "record_id": datasets.Value("string"),
        "date": datasets.Value("int32"),
        "raw_date": datasets.Value("string"),
        "title": datasets.Value("string"),
        "place": datasets.Value("string"),
        "empty_pg": datasets.Value("bool"),
        "text": datasets.Value("string"),
        "pg": datasets.Value("int32"),
        "mean_wc_ocr": datasets.Value("float32"),
        "std_wc_ocr": datasets.Value("float64"),
        "Name": datasets.Value("string"),
        "All names": datasets.Value("string"),
        "Publisher": datasets.Value("string"),
        "Country of publication 1": datasets.Value("string"),
        "All Countries of publication": datasets.Value("string"),
        "Physical description": datasets.Value("string"),
        "Language_1": datasets.Value("string"),
        "Language_2": datasets.Value("string"),
        "Language_3": datasets.Value("string"),
        "Language_4": datasets.Value("string"),
        "multi_language": datasets.Value("bool"),
    }
)


class BritishLibraryBooksConfig(datasets.BuilderConfig):
    """BuilderConfig for BritishLibraryBooks."""

    def __init__(self, data_url, citation, url, **kwargs):
        """BuilderConfig for BritishLibraryBooks.

        Args:
        data_url: `string`, url to download the zip file from.
        citation: `string`, citation for the data set.
        url: `string`, url for information about the data set.
        skip_empty_pages: `bool`, whether to skip empty pages.
        min_ocr_threshold: Optional `float`, minimum threshold for OCR.
        english_only: `bool`, whether to only use english.
        **kwargs: keyword arguments forwarded to super.
        """

        super(BritishLibraryBooksConfig, self).__init__(
            version=datasets.Version("1.0.2"), **kwargs
        )
        self.data_url = data_url
        self.citation = citation
        self.url = url
        self.skip_empty: bool = False
        self.min_ocr_threshold: Optional[float] = None
        self.english_only = False


class BritishLibraryBooks(datasets.GeneratorBasedBuilder):
    """The BritishLibraryBooks dataset."""

    BUILDER_CONFIGS = [
        BritishLibraryBooksConfig(
            name="all",
            description="TODO",
            data_url=_URLS,
            citation=_CITATION,
            url="TODO",
        ),
        BritishLibraryBooksConfig(
            name="1500_1600",
            description="TODO",
            data_url=_URLS["1500_1600"],
            citation=_CITATION,
            url="TODO",
        ),
        BritishLibraryBooksConfig(
            name="1700_1799",
            description="TODO",
            data_url=_URLS["1700_1799"],
            citation=_CITATION,
            url="TODO",
        ),
    ]
    DEFAULT_CONFIG_NAME = "all"

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage="https://",
            citation=_CITATION,
        )

    def _split_generators(
        self, dl_manager: datasets.DownloadManager
    ) -> List[datasets.SplitGenerator]:
        urls_to_download = self.config.data_url

        downloaded_files = dl_manager.download_and_extract(urls_to_download)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN, gen_kwargs={"data_dirs": downloaded_files}
            )
        ]

    def _generate_examples(self, data_dirs):
        skip_empty = self.config.skip_empty
        min_ocr_threshold = self.config.min_ocr_threshold
        english_only = self.config.english_only
        id_ = 0
        for data_dir in data_dirs.values():
            for file in Path(data_dir).rglob("*.jsonl.gz"):
                with gzip.open(file, "rb") as json_l:
                    for row in json_l:
                        data = json.loads(row)
                        record_id = data["record_id"]
                        date = data["date"]
                        raw_date = data["raw_date"]
                        title = data["title"]
                        place = data["place"]
                        if place:
                            place = str(place)
                        empty_pg = data["empty_pg"]
                        text = data["text"]
                        pg = data["pg"]
                        mean_wc_ocr = data["mean_wc_ocr"]
                        mean_wc_ocr = float(mean_wc_ocr) if mean_wc_ocr else 0.0
                        std_wc_ocr = data["std_wc_ocr"]
                        std_wc_ocr = float(data["std_wc_ocr"]) if std_wc_ocr else 0.0
                        Name = data["Name"]
                        All_names = data["All names"]
                        publisher = data["Publisher"]
                        country_of_publication_1 = data["Country of publication 1"]
                        All_Countries_of_publication = data[
                            "All Countries of publication"
                        ]
                        Physical_description = data["Physical description"]
                        Language_1 = data["Language_1"]
                        Language_2 = data["Language_2"]
                        Language_3 = data["Language_3"]
                        Language_4 = data["Language_4"]
                        multi_language = data["multi_language"]
                        if skip_empty and empty_pg:
                            continue
                        if min_ocr_threshold and min_ocr_threshold < mean_wc_ocr:
                            continue
                        if english_only and multi_language:
                            continue
                        if (
                            english_only
                            and ((Language_1 or Language_2 or Language_3 or Language_4))
                            != "English"
                        ):
                            continue
                        id_ += 1
                        yield id_, {
                            "record_id": record_id,
                            "date": date,
                            "raw_date": raw_date,
                            "title": title,
                            "place": place,
                            "empty_pg": empty_pg,
                            "text": text,
                            "pg": pg,
                            "mean_wc_ocr": mean_wc_ocr,
                            "std_wc_ocr": std_wc_ocr,
                            "Name": Name,
                            "All names": All_names,
                            "Publisher": publisher,
                            "Country of publication 1": country_of_publication_1,
                            "All Countries of publication": All_Countries_of_publication,
                            "Physical description": Physical_description,
                            "Language_1": Language_1,
                            "Language_2": Language_2,
                            "Language_3": Language_3,
                            "Language_4": Language_4,
                            "multi_language": multi_language,
                        }
