import requests
import os

key = os.getenv("MIRO_DEV_API_KEY")
board_id = "uXjVO7_CXDs="
url = f"https://api.miro.com/v1/boards/{board_id}/widgets/"

headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {key}"
}

response = requests.request("GET", url, headers=headers)
print(response.text)
