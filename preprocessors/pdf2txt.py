#!/usr/bin/env python3

#!/usr/bin/env python3
#-*- coding:utf-8 -*-
import sys; sys.dont_write_bytecode = True;

import io
import re
import string
import json

from pathlib import Path

import pdfplumber
from nltk.tokenize import sent_tokenize


# class PDFPreProcessor(PreProcessor):
#     def __init__(self, data):
#         super().__init__(data)

#     def _process(self):
#       pdf_path = Path(pdf_path).resolve()
#       if not pdf_path.exists(): raise FileNotFoundError(f"{pdf_path} does not exist")

#       self.path   = pdf_path
#       self.data   = io.BytesIO(self.path.read_bytes())
#       self.reader = pdfplumber.open(self.data)
#       self.pages  = self.reader.pages
#       self.parsed_pages = self.parse()
#       self.write_content(self.parsed_pages)


class PDF:
  def __init__(self, pdf_path):
    pdf_path = Path(pdf_path).resolve()
    if not pdf_path.exists(): raise FileNotFoundError(f"{pdf_path} does not exist")

    self.path   = pdf_path
    self.data   = io.BytesIO(self.path.read_bytes())
    self.reader = pdfplumber.open(self.data)
    self.pages  = self.reader.pages
    self.parsed_pages = self.parse()
    self.write_content(self.parsed_pages)


  def result(self):
    return self.parsed_pages


  def write_content(self, content):
    content_file = Path(self.path.parent / "parsed.json")
    if content_file.exists(): content_file.unlink()
    content_file.write_text(json.dumps(content))


  def parse(self):
    parsed_pages = {}
    page_number  = 0
    min_text_length = 100
    for page in self.pages:
      page_number += 1
      if hasattr(page, 'extract_text'):
        page_text = self.clean_text(page.extract_text())
        if len(str(page_text)) > min_text_length:
          sentences = sent_tokenize(page_text)
          if len(sentences):
            parsed_pages[page_number] = sentences
    return parsed_pages


  def clean_text(self, text):
    # Fix encoding
    text = text.encode('ascii', errors='ignore').strip().decode(errors='ignore')
    # Normalize
    text = text.lower()
    # Remove Embedded Font Mapped Character Codes; e.g. (cid:0) - (cid:XXXX)
    text = re.sub(re.compile(r'\(cid:[0-9]*\)'), '', text)
    # Remove extra periods
    text = re.sub("[\.]{2,}", "", text)
    # Tokenize
    tokens = text.split("\n")
    # Strip extra whitespace & remove blank lines
    text = [line.strip() for line in tokens]
    text = [line for line in tokens if line]
    # Remove multiple spaces
    text = " ".join(text)
    return re.sub(' +', ' ', text)
