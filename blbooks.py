"""Allocine Dataset: A Large-Scale French Movie Reviews Dataset."""


import json
import os
from datetime import datetime
from re import U
from sys import version
from typing import Tuple, Union
import datasets
from datasets.tasks import TextClassification
from pathlib import Path
from dataclasses import dataclass

_CITATION = """\
@misc{blard2019allocine,
  author = {TODO},
  title = {TODO},
  year = {2020},
  publisher = {British Library Labs},
  journal = {British Library},
  howpublished={\\url{TODO},
}
"""

_DESCRIPTION = """\
British Library books dataset
TODO
"""
_URLs = {
    "1550": "https://transfer.sh/get/1reSmss/1550.tar.bz2",
    "1570": "https://transfer.sh/get/1YcjXq4/1570.tar.bz2",
    "1520": "https://transfer.sh/get/1UlQu3r/1520.tar.bz2",
}

# class BritishLibaryBooksConfig(datasets.BuilderConfig):
#     """BuilderConfig for Allocine."""

#     def __init__(self, **kwargs):
#         """BuilderConfig for Allocine.

#         Args:
#           **kwargs: keyword arguments forwarded to super.
#         """
#         super(BritishLibaryBooksConfig, self).__init__(**kwargs)


@dataclass
class BritishLibraryBooksConfig(datasets.BuilderConfig):
    """BuilderConfig for CSV."""

    skip_empty: bool = False
    min_ocr_confidence: Union[bool, float] = False


class BritishLibraryBooks(datasets.GeneratorBasedBuilder):
    """TODO"""

    BUILDER_CONFIG_CLASS = BritishLibraryBooksConfig
    _BASE_DIR = "blbooks"
    _1600_DIR = "1600"
    datasets.DatasetBuilder.DEFAULT_CONFIG_NAME = "default"
    BUILDER_CONFIGS = [
        BritishLibraryBooksConfig(
            name="default",
            version=datasets.Version("1.0.0"),
            description="TODO",
            skip_empty=False,
            min_ocr_confidence=False,
        ),
        BritishLibraryBooksConfig(
            name="skip_empty",
            version=datasets.Version("1.0.0"),
            description="A version of BL books which contains books published in the 1600s",
            skip_empty=True,
            min_ocr_confidence=False,
        ),
        BritishLibraryBooksConfig(
            name="1500",
            version=datasets.Version("1.0.0"),
            description="Allocine Dataset: A Large-Scale French Movie Reviews Dataset",
            skip_empty=False,
            min_ocr_confidence=False,
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "date": datasets.Value("string"),
                    "title": datasets.Value("string"),
                    "place": datasets.Value("string"),
                    "record_id": datasets.Value("uint32"),
                    "pg": datasets.Value("uint16"),
                    "text": datasets.Value("string"),
                    "blank_pg": datasets.Value("bool"),
                }
            ),
            supervised_keys=None,
            homepage="https://github.com/TheophileBlard/french-sentiment-analysis-with-bert",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        download_folders = dl_manager.download_and_extract(_URLs)
        skip_empty = self.config.skip_empty
        return [
            datasets.SplitGenerator(
                name="1550",
                gen_kwargs={
                    "dirpath": download_folders["1550"],
                    "skip_empty": skip_empty,
                },
            ),
            datasets.SplitGenerator(
                name="1570",
                gen_kwargs={
                    "dirpath": download_folders["1570"],
                    "skip_empty": skip_empty,
                },
            ),
            datasets.SplitGenerator(
                "1520",
                gen_kwargs={
                    "dirpath": download_folders["1520"],
                    "skip_empty": skip_empty,
                },
            ),
        ]

    def _generate_examples(self, dirpath, skip_empty):
        """Generate Allocine examples."""
        for file in Path("blbooks/1600").glob("*.json"):
            with open(file, "r") as json_l:
                for line in json_l:
                    data = json.loads(line)
                    date = data["date"]
                    title = data["title"]
                    place = data["place"]
                    text = data["text"]
                    blank_pg = data["blank_pg"]
                    record_id = int(data["record_id"])
                    pg = int(data["pg"])
                    id_ = f"{record_id}_{pg}"
                    if skip_empty:
                        if not blank_pg:
                            yield id_, {
                                "date": date,
                                "title": title,
                                "place": place,
                                "record_id": record_id,
                                "pg": pg,
                                "text": text,
                                "blank_pg": blank_pg,
                            }
                        else:
                            continue
                    if not skip_empty:
                        yield id_, {
                            "date": date,
                            "title": title,
                            "place": place,
                            "record_id": record_id,
                            "pg": pg,
                            "text": text,
                            "blank_pg": blank_pg,
                        }
