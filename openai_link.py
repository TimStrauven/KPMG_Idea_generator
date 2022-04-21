import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def openai_completion(prompt: str, max_tokens: int) -> str:
    """
    Asks openai text-davinci-002 model for completion
    and returns the text string of the first choice
    """
    answer = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=max_tokens
    )
    print(answer)
    return answer.choices[0].text
