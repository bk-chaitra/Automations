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
        "service_ids[]": service_id,
        "statuses[]": "acknowledged",
        "since": start_date.isoformat(),
        "until": end_date.isoformat(),
        "limit": 1000,  # Adjust the limit if needed
        "sort_by": "created_at:desc"  # Sort incidents by creation time in descending order
    }
    url = "https://api.pagerduty.com/incidents"
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()["incidents"]
    print("Failed to fetch incidents:", response.text)
    return []

def update_notes(api_token, incident_id, notes):
    headers = {
        "Accept": "application/vnd.pagerduty+json;version=2",
        "Authorization": f"Token token={api_token}",
        "Content-Type": "application/json"
    }
    url = f"https://api.pagerduty.com/incidents/{incident_id}/notes"
    payload = {
        "note": {
            "content": notes,
            "user": {
                "id": "USER_ID",  # Replace USER_ID with the ID of the user who is updating the notes
                "type": "user_reference"
            }
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        print(f"Notes updated for incident {incident_id}")
    else:
        print(f"Failed to update notes for incident {incident_id}: {response.text}")

if __name__ == "__main__":
    api_token = "e+i-GkguAd26VyVUvEXg"#your api token
    services = [
        "service-1","service-2"
    ]
    start_date = datetime(2024, 4, 17 ,12 , 0)  # Start date
    end_date = datetime(2024, 4, 17, 23, 59)    # End date
    notes = "Could you please update the status of the incident. If it's fixed, please resolve it."  # Notes to update for incidents

    for service_name in services:
        service_id = fetch_service_id(api_token, service_name)
        if service_id:
            incidents = fetch_incidents(api_token, service_id, start_date, end_date)
            for incident in incidents:
                incident_id = incident["id"]
                update_notes(api_token, incident_id, notes)
