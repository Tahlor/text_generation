import re
from pathlib import Path
import os


text_gen_path = Path(os.path.dirname(os.path.realpath(__file__)))

def load_data(path):
    with Path(text_gen_path / path).open() as f:
        all_text = f.read()
    return all_text

def save_data(path, data):
    with Path(text_gen_path / path).open("w") as f:
        f.write(data)

def clean(all_text):
    all_text = re.sub(r'[^A-Za-z ]+', '', all_text)
    return re.sub("\s\s+", " ", all_text)


all_text = load_data("raw_text_10000.txt")
clean_text = clean(all_text)
save_data("clean_text.txt", clean_text)
