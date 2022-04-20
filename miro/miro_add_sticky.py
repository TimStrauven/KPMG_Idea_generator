import os
import requests

key = os.getenv("MIRO_DEV_API_KEY")
board_id = "uXjVO7_CXDs="
url = f"https://api.miro.com/v1/boards/{board_id}/widgets/"

payload = {
    "type": "sticker",
    "text": "<p>Added By Tim</p>",
}

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {key}"
}

response = requests.request("POST", url, json=payload, headers=headers)
print(response.text)
