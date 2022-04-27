
import os
import openai


class OpenAI_Generator():
    """
    A Class that generate idea for user based GPT-3 API.
    """
    def __init__(self, prepared_question: str, number_of_idea: int) -> None:
        """
        A constructor function for Generator class.
        :param prepared_question: A question that user want to ask.
        :param number_of_idea: Number of idea that user want to get.
        :param crazy: A boolean value that indicate if user want to get an unusual suggestions or a more normal one.
        :param workshop_method: A string value that indicate which workshop method user want to use.
        """
        self.prepared_question: str = prepared_question
        self.number_of_idea: int = number_of_idea
        self.raw_result: dict = None
        self.idea_list: list = []
        self.payload: dict = {}

    def connect_openai(self) -> bool:
        """
        A function that create api connection.
        :return: A boolean value that indicate if api connection is created or not.
        """
        try:
            openai.api_key = os.getenv("OPENAI_API_KEY")
        except openai.exceptions.InvalidAPIKeyError:
            return False
        except FileNotFoundError:
            return False
        except openai.exceptions.InvalidRequestError:
            return False
        else:
            return True

    def generate_idea(self) -> list:
        """
        A Funtion that generate idea for user based on GPT-3 API.
        :return: A boolean value that indicate if idea is generated or not.
        """
        if self.connect_openai():
            """
            If api connection is created, then generate idea.
            """
            self.payload['prompt'] = self.prepared_question
            self.payload['engine'] = "text-davinci-002"
            self.payload['max_tokens'] = 200
            self.payload['temperature'] = 1
            self.payload['top_p'] = 1
            self.payload['presence_penalty'] = 2
            self.payload['frequency_penalty'] = 2
            self.payload['n'] = self.number_of_idea
            self.raw_result = openai.Completion.create(**self.payload)
            self.get_idea_list()
            return self.idea_list
        else:
            """
            If api connection is not created, then return false.
            """
            self.idea_list.append("No result generated")
            return self.idea_list

    def get_idea_list(self) -> list:
        """
        A function that get idea list from raw result.
        :return: A list of idea.
        """
        if self.raw_result is not None:
            for i in range(self.number_of_idea):
                self.idea_list.append(self.raw_result['choices'][i]['text'].replace("\n", ""))
        else:
            self.idea_list.append("No result generated")
        return self.idea_list
