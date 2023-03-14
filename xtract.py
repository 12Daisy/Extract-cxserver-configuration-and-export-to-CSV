import os
import csv
import yaml


supported_pairs = []

for file_name in os.listdir("config"):
    if not file_name.endswith(".yaml") or file_name in {"MWPageLoader.yaml", "languages.yaml", "JsonDict.yaml", "Dictd.yaml", "mt-defaults.wikimedia.yaml"}:
        continue
    
    with open(os.path.join("config", file_name), "r") as f:
        data = yaml.safe_load(f)
        
        if "handler" in data and data["handler"] != "base":
            continue
        
        if "servicePairs" in data:
            for pair in data["servicePairs"]:
                source = pair["source"]
                for target in pair["targets"]:
                    supported_pairs.append({
                        "source language": source,
                        "target language": target,
                        "translation engine": file_name[:-5], # remove ".yaml" extension
                        "is preferred engine?": pair.get("preferred", False)
                    })
        else:
            for source, targets in data.items():
                for target in targets:
                    supported_pairs.append({
                        "source language": source,
                        "target language": target,
                        "translation engine": file_name[:-5], # remove ".yaml" extension
                        "is preferred engine?": False
                    })

# Write to CSV file
with open("supported_language_pairs.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["source language", "target language", "translation engine", "is preferred engine?"])
    writer.writeheader()
    writer.writerows(supported_pairs)
