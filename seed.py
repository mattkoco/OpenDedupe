import requests
import time
import json

API_URL = "http://localhost:8000"

# Updated to use 'subject' and 'body'
tickets = [
    {"subject": "Cannot access email", "body": "I am getting a 401 error when opening Outlook."},
    {"subject": "Outlook is down", "body": "My inbox won't load and says unauthorized."},
    {"subject": "Email login failing", "body": "Can't get into my webmail since this morning."},
    {"subject": "Printer on 2nd floor jammed", "body": "The HP printer in the breakroom is chewing up paper."},
    {"subject": "Paper jam", "body": "2nd floor printer needs maintenance, paper is stuck."},
    {"subject": "Need new mouse", "body": "The scroll wheel on my Bluetooth mouse is broken."},
    {"subject": "VPN connection dropping", "body": "My VPN disconnects every 5 minutes."}
]

def main():
    print("firing test tickets at the ingestion endpoint\n")
    
    for ticket in tickets:
        print(f"Submitting: {ticket['subject']}")
        response = requests.post(f"{API_URL}/tickets", json=ticket)
        
        if response.status_code == 200:
            data = response.json()
            print(f"Success! Assigned to Cluster ID: {data['cluster_id']}\n")
        else:
            print(f"Error: {response.text}\n")
            
        time.sleep(0.5)

    print("Fetching the final clustered groups\n")
    response = requests.get(f"{API_URL}/clusters")
    
    if response.status_code == 200:
        clusters = response.json()
        print(json.dumps(clusters, indent=2))
    else:
        print("Failed to fetch clusters.")

if __name__ == "__main__":
    main()