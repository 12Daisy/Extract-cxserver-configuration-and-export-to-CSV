import os
import yaml

ALLOWED_FILES = ["Apertium.yaml", "Azure.yaml", "Google.yaml", "Microsoft.yaml"]

supported_pairs = []

for file in os.listdir("config"):
    if file.endswith(".yaml") and file not in ["MWPageLoader.yaml", "languages.yaml", "JsonDict.yaml", "Dictd.yaml", "mt-defaults.wikimedia.yaml"] and file in ALLOWED_FILES:
        engine = file.replace(".yaml", "")
        with open(os.path.join("config", file), "r") as f:
            data = yaml.safe_load(f)
            for source_lang, target_langs in data.items():
                if source_lang == "handler":
                    continue
                for target_lang in target_langs:
                    supported_pairs.append({
                        "source language": source_lang,
                        "target language": target_lang,
                        "translation engine": engine,
                        "is preferred engine?": False
                    })

# Add preferred engines for some language pairs
preferred_pairs = [
    {"source language": "en", "target language": "fr", "translation engine": "DeepL", "is preferred engine?": True},
    {"source language": "fr", "target language": "en", "translation engine": "DeepL", "is preferred engine?": True},
    {"source language": "en", "target language": "ja", "translation engine": "Google", "is preferred engine?": True},
    {"source language": "ja", "target language": "en", "translation engine": "Google", "is preferred engine?": True},
]

for pair in preferred_pairs:
    if pair not in supported_pairs:
        supported_pairs.append(pair)

# Export as CSV
import csv

with open("supported_pairs.csv", "w") as f:
    writer = csv.DictWriter(f, fieldnames=["source language", "target language", "translation engine", "is preferred engine?"])
    writer.writeheader()
    writer.writerows(supported_pairs)
