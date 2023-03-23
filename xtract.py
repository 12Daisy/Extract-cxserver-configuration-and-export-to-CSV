import os
import yaml
import csv

# Define the directory containing the YAML files
CONFIG_DIR = "config/"

# Define the list of YAML files to exclude
EXCLUDE_FILES = [
    "MWPageLoader.yaml",
    "languages.yaml",
    "JsonDict.yaml",
    "Dictd.yaml",
    "mt-defaults.wikimedia.yaml",
]

# Define the output CSV file name
OUTPUT_FILE = "supported_language_pairs.csv"

# Define the CSV fieldnames
FIELDNAMES = ["source language", "target language", "translation engine", "is preferred engine?"]


def parse_yaml_file(filename):
    """Parse a YAML file and return a list of supported language pairs"""
    with open(filename, "r") as f:
        data = yaml.safe_load(f)
        if "handler" in data and data["handler"] == "transform.js":
            # Handle the special case where data["handler"] == "transform.js"
            # In this case, the "languages" list is expanded by its self-cross-product
            # with a few exclusions
            langs = data["languages"]
            exclusions = ["be-tarask", "zh-classical", "zh-min-nan"]
            pairs = [(s, t) for s in langs for t in langs if s != t and t not in exclusions]
        else:
            # Handle the common case where the source language is the top-level key
            source_lang = list(data.keys())[0]
            target_langs = data[source_lang]
            pairs = [(source_lang, t) for t in target_langs]
        return pairs


def parse_yaml_files():
    """Parse all the YAML files and return a flat list of supported language pairs"""
    pairs = []
    for filename in os.listdir(CONFIG_DIR):
        if filename.endswith(".yaml") and filename not in EXCLUDE_FILES:
            filepath = os.path.join(CONFIG_DIR, filename)
            pairs.extend(parse_yaml_file(filepath))
    return pairs


def create_csv_file(pairs):
    """Create a CSV file with the supported language pairs"""
    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for pair in pairs:
            writer.writerow({
                "source language": pair[0],
                "target language": pair[1],
                "translation engine": "Content Translation",
                "is preferred engine?": True,
            })


if __name__ == "__main__":
    pairs = parse_yaml_files()
    create_csv_file(pairs)
