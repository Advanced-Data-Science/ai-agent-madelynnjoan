import requests

def get_public_holidays(country_code="US", year=2024):
    """
    Get public holidays for a specific country and year
    Uses Nager.Date API (free, no key required)
    """
    url = f"https://date.nager.at/api/v3/PublicHolidays/{year}/{country_code}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an exception for bad status codes
        
        holidays = response.json()
        return holidays
    
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

# Test with 3 different countries
countries = ['US', 'CA', 'GB']
holiday_summary = {}

for country in countries:
    holidays = get_public_holidays(country)
    if holidays:
        print(f"\n{country} Public Holidays in 2024:")
        for h in holidays:
            print(f"{h['date']}: {h['localName']}")
        
        holiday_summary[country] = len(holidays)

# Summary comparison
print("Holiday Count Summary for 2024")
for country, count in holiday_summary.items():
    print(f"{country}: {count} holidays")