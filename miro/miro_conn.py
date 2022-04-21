import os
import requests

key = os.getenv("MIRO_DEV_API_KEY")
board_id = "uXjVO7_CXDs="
url = f"https://api.miro.com/v1/boards/{board_id}/widgets/"

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {key}",
}

def sticky_onto_miro(text, x, y) -> None:
    """create a sticky on miro"""
    payload = {
        "type": "sticker",
        "text": f"<p>{text}</p>",
        "x": x,
        "y": y
    }
    response = requests.request("POST", url, json=payload, headers=headers)
    # print(response.text)

def get_last_sticky_pos() -> tuple:
    """get the last sticky's position"""
    response = requests.request("GET", url, headers=headers)
    max_X = 0
    max_Y = 0
    for widget in response.json()["data"]:
        if float(widget["x"]) > max_X:
            max_X = round(float(widget["x"]))
        if float(widget["y"]) > max_Y:
            max_Y = round(float(widget["y"]))
    return max_X, max_Y

def get_stickies_text() -> list:
    """get all stickies' text"""
    response = requests.request("GET", url, headers=headers)
    text = []
    for widget in response.json()["data"]:
        this_text = widget["text"].replace("<p>", "").replace("</p>", "")
        text.append(this_text)
    return text

def create_sticky(text):
    """create a sticky on miro taking the last position into account"""
    max_x, max_y = get_last_sticky_pos()
    sticky_onto_miro(text, max_x + 108, max_y)
