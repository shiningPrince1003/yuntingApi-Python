import time
import requests
from hashlib import md5
import base64


def generate_sign(data_json, timestamp, yunting_key):
    data_json_stringify = "&".join(
        [f"{key}={value}" for key, value in data_json.items()]
    )
    api_sign_pre_text = f"{data_json_stringify}&timestamp={timestamp}&key={yunting_key}"
    return md5(api_sign_pre_text.encode()).hexdigest().upper()


def request_yun_ting_api(data_json):
    timestamp = int(time.time() * 1000)
    yunting_key = base64.b64decode("ZjBmYzRjNjY4MzkyZjlmOWE0NDdlNDg1ODRjMjE0ZWU=").decode()
    sign = generate_sign(data_json, timestamp, yunting_key)

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Equipmentid": "0000",
        "Origin": "https://www.radio.cn",
        "Referer": "https://www.radio.cn",
        "Sign": sign,
        "Timestamp": str(timestamp),
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
    }

    url = "https://ytmsout.radio.cn/web/appBroadcast/list"
    try:
        response = requests.get(url, params=data_json, headers=headers)
        response.raise_for_status() 
        json_data = response.json()
        if json_data["message"] == "SUCCESS":
            return json_data["data"]
        else:
            return "API REQUEST ERROR"
    except requests.RequestException as e:
        print(f"Error: {e}")
        return None


if __name__ == "__main__":
    data = {"categoryId": 5, "provinceCode": 0}
    result = request_yun_ting_api(data)
    if result:
        for item in result:
            if item["contentId"] == "641":
                print(item["playUrlLow"])

