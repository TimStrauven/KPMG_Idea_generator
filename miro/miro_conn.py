import os
import random
import requests

key = os.getenv("MIRO_DEV_API_KEY")
board_id = "uXjVO6K6Sck="
url = f"https://api.miro.com/v1/boards/{board_id}/widgets/"

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {key}",
    }

def _sticky_onto_miro(text: str, x: int, y: int) -> None:
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
    """get the text from 2 random sticky notes on the board and return them in a list"""
    response = requests.request("GET", url, headers=headers)
    text = []
    for widget in response.json()["data"]:
        this_text = widget["text"].replace("<p>", "").replace("</p>", "")
        text.append(this_text)
    # return random list if there are more than 2 stickies
    if len(text) > 2:
        final_text = []
        random_ints = random.sample(range(0, len(text)), 2)
        for i in random_ints:
            final_text.append(text[i])
        return final_text
    else:
        return text

def create_sticky(text: str) -> None:
    """create a sticky on miro taking the last position into account"""
    max_x, max_y = get_last_sticky_pos()
    _sticky_onto_miro(text, max_x + 108, max_y)
