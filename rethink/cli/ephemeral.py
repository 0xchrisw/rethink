#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import json


from pathlib import Path

import rethink.preprocessors as preprocessors


def main():
    pdf_path = "data/Elasticsearch - The Definitive Guide.pdf"
    # text = preprocessors.pdf2txt.PDF(pdf_path).result()
    # print(text)

    # output_file = Path(pdf_path).parent / "parsed.json"
    print(Path(pdf_path).parent / "parsed.json")


if __name__ == "__main__":
    main()
