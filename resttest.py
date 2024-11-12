import requests

# Home Assistant API URL
url = "http://137.186.88.102:53218/api/"

def get_connection_str(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()

token = get_connection_str("token.txt")

# API token

# Headers
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

try:
    # Send a GET request to the API
    response = requests.get(url, headers=headers)

    # Check the response
    if response.status_code == 200:
        print("Connectivity test successful! Home Assistant is accessible.")
    else:
        print(f"Error: {response.status_code} - {response.text}")

except requests.exceptions.RequestException as e:
    print(f"Connection error: {e}")
