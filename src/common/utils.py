import os
import json

# === HELPER FUNCTIONS ===
def save_json(tokens, filepath):
    with open(filepath, "w") as f:
        json.dump(tokens, f, indent=2)

def load_json(filepath):
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return json.load(f)
    return None