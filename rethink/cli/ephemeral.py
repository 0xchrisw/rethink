#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import json

from pathlib import Path

import rethink.preprocessors as preprocessors


pdf_path = "data/document.pdf"
output_file = Path(pdf_path).parent / "parsed.json"
train_file = Path(pdf_path).parent / "train.json"

parsed_data = json.loads(output_file.read_text()) if output_file.exists() else None
if not parsed_data:
    parsed_data = preprocessors.pdf2txt.PDF(pdf_path).result()
    output_file.write_text(json.dumps(parsed_data, indent=2))


text = [" ".join(parsed_data[key]) for key in list(parsed_data.keys())[25:50]]
train_file.write_text(json.dumps(text, indent=2))


import textgenrnn

textgen = textgenrnn.textgenrnn()
textgen.train_from_file(str(train_file.as_posix()), num_epochs=1)

textgen.save('textgenrnn_weights.hdf5')
# textgen.load('textgenrnn_weights.hdf5')

textgen.generate()
textgen.generate(3, temperature=1.0)
# textgen.generate_to_file('output.txt', n=3, temperature=1.0)


def main():
    ...

if __name__ == "__main__":
    main()
