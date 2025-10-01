"""
Maddy Smith CS3870
AI Agent, Web Scraping
"""

import requests
import json
import logging

"""Set up logging"""
logging.basicConfig(
    filename="cat_agent.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Make your first API call to get a random cat fact
def get_cat_fact():
    url = "https://catfact.ninja/fact"
    
    try:
        # Send GET request to the API
        response = requests.get(url, timeout = 5)
        
        # Check if request was successful
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()
            logging.info("Successfully retrieved a cat fact.")
            return data['fact']
        else:
            logging.error(f"API returned status code {response.status_code}")
            return None
    
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        return None
    except Exception as e:
        logging.exception("Unexpected error occurred.")
        return None

# Test your function
"""cat_fact = get_cat_fact()
print(f"Cat fact: {cat_fact}")"""

#getting 5 cat facts
facts = []
for i in range(5):
    fact = get_cat_fact()
    if fact:
        facts.append(fact)
    else: logging.warning(f"Failed to get a fact #{i + 1}")

#saving to JSON file
try:
    with open("cat_facts.json", "w") as f:
        json.dump(facts, f, indent=4)
    logging.info("Saved cat facts to cat_facts.json")
except Exception as e:
    logging.error(f"Failed to save cat facts: {e}")

