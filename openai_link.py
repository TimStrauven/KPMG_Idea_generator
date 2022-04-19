import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def openai_completion(prompt, max_tokens):
    answer = openai.Completion.create(
        engine="text-davinci-002",
        prompt="list 5 animals",
        max_tokens=30
    )
    answers = []
    for i in range(len(answer.choices)):
        answers.append(answer.choices[i].text)
    return answers

print(openai_completion("list 5 animals", 10))
