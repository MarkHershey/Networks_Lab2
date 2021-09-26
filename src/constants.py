import json
from pathlib import Path

from puts.logger import logger

SRC_ROOT_DIR: Path = Path(__file__).parent.resolve()
STATIC_DIR: Path = SRC_ROOT_DIR / "static"

transaction_code_fp: Path = STATIC_DIR / "transaction_code.json"
keywords_to_labels_fp: Path = STATIC_DIR / "keywords_to_labels.json"
labels_to_categories_fp: Path = STATIC_DIR / "labels_to_categories.json"

assert transaction_code_fp.is_file()
assert keywords_to_labels_fp.is_file()
assert labels_to_categories_fp.is_file()

CODE = None
KEYWORDS = None
LABELS = None


with transaction_code_fp.open() as codefile:
    CODE = json.load(codefile)

with keywords_to_labels_fp.open() as keywordfile:
    KEYWORDS = json.load(keywordfile)

with labels_to_categories_fp.open() as labelfile:
    LABELS = json.load(labelfile)
