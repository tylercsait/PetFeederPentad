import requests
import time

def get_connection_str(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Token file not found at {file_path}.")
        return None

def set_url(new_url):
    global url
    url = new_url

def set_entity_id(new_entity_id):
    global entity_id
    entity_id = new_entity_id

def set_portion_size(new_portion_size):
    global portion_size
    portion_size = new_portion_size

def dispense_portions(portions):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    data = {
        "entity_id": entity_id,
        "value": portions
    }

    try:
        print(f"Sending request to Home Assistant API to dispense {portions} portions.")
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            print("Dispense command sent successfully.")
            # 检查响应内容，确认喂食命令已被执行
            print(f"Response: {response.text}")
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

# 配置部分
# 从文件中读取令牌
token = get_connection_str("token.txt")
if not token:
    print("Token is not available. Please ensure 'token.txt' exists and contains the token.")
    # 可以选择在此终止程序或抛出异常

# 设置 Home Assistant API 的 URL 和实体 ID
url = "http://192.168.1.200:8123/api/services/number/set_value"  # 请根据您的实际情况修改
entity_id = "number.smart_pet_feeder_feed"  # 请根据您的实际情况修改

# 示例使用
if __name__ == "__main__":
    # 设置要分配的份数
    portion_size = 4  # 可以根据需要修改
    response = dispense_portions(portion_size)
    if response:
        print("Dispense request completed.")
        view_response(response)
    else:
        print("Failed to send dispense request.")
