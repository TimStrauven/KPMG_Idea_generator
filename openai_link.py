import os
from secrets import choice
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def openai_completion(prompt, max_tokens):
    answer = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=max_tokens
    )
    print(answer)
    return answer.choices[0].text
