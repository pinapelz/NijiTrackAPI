import json

def get_login():
    # read login from config.json
    with open("config.json", "r") as f:
        config = json.load(f)
    return config["hostname"], config["username"], config["password"], config["database_name"]
