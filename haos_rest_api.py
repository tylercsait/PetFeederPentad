"""
This program uses the REST api to control the petfeeder
"""
import requests

# Home Assistant API URL
#url = "http://137.186.88.102:53218/api/services/number/set_value"
url = "http://192.168.1.200:8123/api/services/number/set_value"

entity_id = "number.chong_wu_wei_shi_qi_sdk_feed"

def get_connection_str(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()

token = get_connection_str("token.txt")


# Headers
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

def set_portion_size():
    portion_size =
portion_size = 1
data = {
    "entity_id": f"{entity_id}",
    "value": portion_size
}

try:
    # Send a GET request to the API
    #response = requests.get(url, headers=headers)
    response = requests.post(url, headers=headers, json=data)
    # Check the response
    if response.status_code == 200:
        print("Connectivity test successful! Home Assistant is accessible.")
    else:
        print(f"Error: {response.status_code} - {response.text}")

except requests.exceptions.RequestException as e:
    print(f"Connection error: {e}")

print(f"URL: {url}")
print(f"Headers: {headers}")
print(f"Data: {data}")
print(f"Response Status Code: {response.status_code}")
print(f"Response Text: {response.text}")
