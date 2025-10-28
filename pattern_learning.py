import json

def learn_patterns(json_files):
    patterns = []
    for file in json_files:
        with open(file, "r") as f:
            actions = json.load(f)
        # Placeholder: detect repetitive sequences
        patterns.append({"file": file, "pattern_count": len(actions)})
    return patterns
