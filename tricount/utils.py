import requests

def get_exchange_rates(api_key):
    url = f"https://api.exchangerate-api.com/v4/latest/USD"
    response = requests.get(url, headers={"apikey": api_key})
    if response.status_code == 200:
        return response.json()
    else:
        return None
