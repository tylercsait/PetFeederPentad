import requests
import time

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


def check_feeding():
    check_url = f"{main.REST_URL}/states/{feeding_id}"

    try:
        response = requests.get(check_url, headers=headers)
        if response.status_code == 200:
            state = response.json().get('state')
            if state == "on":
                return True
            else:
                return False
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")
        return False


def dispense_portions(portion_size):
    data = {
        "entity_id": entity_id,
        "value": portion_size
    }

    # Check if feeding is active and wait until it is not
    while check_feeding():
        print("Feeding is currently active. Waiting...")
        time.sleep(1)

    with requests.Session() as session:
        try:
            print(f"Sending request to {url} with data: {data}")
            response = session.post(url, headers=headers, json=data)
            print(f"Received response: {response.status_code} - {response.text}")
            if response.status_code == 200:
                print("Connectivity test successful! Home Assistant is accessible.")
                print(f"Dispensing {portion_size} portions.")
            else:
                print(f"Error: {response.status_code} - {response.text}")
                print(f"Response Content: {response.content}")
            return response
        except requests.exceptions.RequestException as e:
            print(f"Connection error: {e}")
            return None

def view_response(response):
    print(f"URL: {response.url}")
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")


# Home Assistant API URL
url = main.REST_URL
entity_id = "number.smart_pet_feeder_feed"
feeding_id = "binary_sensor.smart_pet_feeder_feeding"
token = get_connection_str("token.txt")

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Example usage
if __name__ == "__main__":
    portion_size = 4
    response = dispense_portions(portion_size)
    if response:
        print("Dispense request completed.")
        view_response(response)
    else:
        print("Failed to send dispense request.")
