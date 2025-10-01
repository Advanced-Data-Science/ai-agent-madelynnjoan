"""
Maddy Smith CS3870
API Call for NORS Data Set
Note: No API key needed
"""

import requests
import json


def load_config(config_file="config.json"):
    """Load config file"""
    with open(config_file, "r") as f:
        return json.load(f)


def main():
    """Main program to call API"""
    config = load_config()
    
    url = config.get("api_endpoint")
    if not url:
        print("Error: 'api_endpoint' not found in config file")
        return

    params = {
        "year": config.get("year"),
        "state": config.get("state")
    }

    # Send GET request
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        print(f"Number of records received: {len(data)}")
        if data:
            print("First record:", data[0])
    else:
        print(f"Failed to retrieve data: {response.status_code}")

if __name__ == "__main__":
    main()
