#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import json


from pathlib import Path

import rethink.preprocessors as preprocessors


def main():
    pdf_path = "data/Elasticsearch - The Definitive Guide.pdf"
    output_file = Path(pdf_path).parent / "parsed.json"

    parsed_data = json.loads(output_file.read_text()) if output_file.exists() else None

    if not parsed_data:
        parsed_data = preprocessors.pdf2txt.PDF(pdf_path).result()
        output_file.write_text(json.dumps(parsed_data, indent=2))

    print(parsed_data)


if __name__ == "__main__":
    main()
