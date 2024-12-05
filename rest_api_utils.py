import requests

import main


def get_connection_str(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Token file not found at {file_path}.")
        return None

def set_url(new_url):
    return new_url

def set_entity_id(new_entity_id):
    return new_entity_id

def set_portion_size(new_portion_size):
    return new_portion_size

def dispense_portions(portion_size):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    data = {
        "entity_id": entity_id,
        "value": portion_size
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            print("Connectivity test successful! Home Assistant is accessible.")
        else:
            print(f"Error: {response.status_code} - {response.text}")
        return response
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")
        return None

def view_response(response):
    print(f"URL: {response.url}")
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")

# Home Assistant API URL
# url = "http://137.186.88.102:53218/api/services/number/set_value"
# url = "http://192.168.1.200:8123/api/services/number/set_value"
url = main.REST_URL
entity_id = "number.smart_pet_feeder_feed"
token = get_connection_str("token.txt")


# Example usage
if __name__ == "__main__":
    portion_size = 4
    response = dispense_portions(portion_size)
    if response:
        print("Dispense request completed.")
        view_response(response)
    else:
        print("Failed to send dispense request.")
