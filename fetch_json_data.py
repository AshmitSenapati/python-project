import json

def fetch_data_from_json(filepath):
    try:
        with open(filepath, "r") as file:
            data = json.load(file)
        return data
    except Exception as e:
        print("Error reading JSON file:", e)
        return []
