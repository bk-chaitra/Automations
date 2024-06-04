import requests

def fetch_services(api_token, params=None):
    headers = {
        "Accept": "application/vnd.pagerduty+json;version=2",
        "Authorization": f"Token token={api_token}"
    }
    url = "https://api.pagerduty.com/services"
    
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if "services" in data:
            return [service["name"] for service in data["services"]]
    print("Failed to fetch services:", response.text)
    return []

# Example usage:
if __name__ == "__main__":
    api_token = "e+i-GkguAd26VyVUvEXg" # your api token
    params = {"limit": 100}  # Example parameters (you can add more as needed)
    service_names = fetch_services(api_token, params=params)
    print("Service Names:")
    for service_name in service_names:
        print(service_name)
