import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def openai_completion(prompt: str, max_tokens: int, temp: int) -> str:
    """
    Asks openai text-davinci-002 model for completion
    and returns the text string of the first choice
    """
    if temp == 0:  # Conservative
        temperature = 0.5
        top_p = 0.5
        pres_pen = 2
        freq_pen = 2
    elif temp == 2:  # Crazy
        temperature = 1
        top_p = 1
        pres_pen = 2
        freq_pen = 2
    else:  # Normal
        temperature = 0.8
        top_p = 0.8
        pres_pen = 2
        freq_pen = 2
    print(prompt)
    answer = openai.Completion.create(
        engine="text-davinci-002",
        temperature=temperature,
        top_p=top_p,
        prompt=prompt,
        presence_penalty=pres_pen,
        frequency_penalty=freq_pen,
        max_tokens=max_tokens
    )
    print(answer)
    cleananswer = answer.choices[0].text
    cleananswer = cleananswer.replace("\n", "")
    return cleananswer
