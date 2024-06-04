import requests
from datetime import datetime, timedelta

def fetch_service_id(api_token, service_name):
    headers = {
        "Accept": "application/vnd.pagerduty+json;version=2",
        "Authorization": f"Token token={api_token}"
    }
    url = "https://api.pagerduty.com/services"
    params = {
        "query": service_name
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        services = response.json()["services"]
        if services:
            return services[0]["id"]
    print(f"Service '{service_name}' not found.")
    return None

def fetch_incidents(api_token, service_id, start_date, end_date):
    headers = {
        "Accept": "application/vnd.pagerduty+json;version=2",
        "Authorization": f"Token token={api_token}"
    }
    params = {
        "since": start_date.isoformat(),
        "until": end_date.isoformat(),
        "service_ids[]": service_id,
        "limit": 1000  # Increase limit to fetch all incidents
    }
    url = "https://api.pagerduty.com/incidents"
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()["incidents"]
    print("Failed to fetch incidents:", response.text)
    return []

def update_priority(api_token, incident_id, priority_id):
    headers = {
        "Accept": "application/vnd.pagerduty+json;version=2",
        "Authorization": f"Token token={api_token}",
        "Content-Type": "application/json"
    }
    url = f"https://api.pagerduty.com/incidents/{incident_id}"
    payload = {
        "incident": {
            "type": "incident_reference",
            "priority": {
                "id": priority_id,
                "type": "priority"
            }
        }
    }
    response = requests.put(url, headers=headers, json=payload)
    if response.status_code == 200:
        print(f"Priority updated for incident {incident_id}")
    else:
        print(f"Failed to update priority for incident {incident_id}: {response.text}")

def check_and_update_priority(api_token, incident):
    keywords_priority_map = {
        "P1": ["[prod][Synthetics Test]", "Pod Restarting", "Pod CrashloopBackOff"]
    }
    incident_title = incident["title"]
    priority_id = "PDPH1Z9"  # Default to P2 priority ID
    for priority, keywords in keywords_priority_map.items():
        if any(keyword in incident_title for keyword in keywords):
            priority_id = "PGM52OZ"  # P1 priority ID
            break
    update_priority(api_token, incident["id"], priority_id)

if __name__ == "__main__":
    api_token = "e+i-GkguAd26VyVUvEXg"  # your api token
    service_name = "user-and-resource-management-events"  # your service name
    start_date = datetime(2024, 5, 28, 0, 0)  # Start date with time
    end_date = datetime(2024, 6, 3, 23, 59)  # End date with time
    
    service_id = fetch_service_id(api_token, service_name)
    if service_id:
        incidents = fetch_incidents(api_token, service_id, start_date, end_date)
        for incident in incidents:
            check_and_update_priority(api_token, incident)
