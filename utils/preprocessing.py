import os
import string


class Preprocessing():
    """
    A class that handles the preprocessing of the raw user input
    depending on the workshop method selected
    return : json ?(str?)
    """
    #     workshop_method = data['workshop_method']

    def __init__(self, input_data: str):
        """
        Initializes the preprocessing class.
        :param intput_data: The directory of the data.
        :param output_data: The output data.
        """
        self.input_data: str = input_data
        self.output_data: str = None

    def process_hmw(self) -> str:
        """
        A Function that prepares usable question for GPT-3
        for the "How might X..?" workshops
        """
        # TODO update for json from save facilitator status (wait for Fortuné)
        with open("./data/facilitator_status.txt", "r") as f:
            workshop = int(f.read())
        return self._process_text("How might", f" {workshop}")

    def process_opposite(self) -> str:
        """
        A Function that prepares usable question for GPT-3
        for the "Opposite thinking" workshops
        """
        return self._process_text("What is the opposite of how", "should be?")

    def process_bad_idea(self) -> str:
        """
        A Function that prepares usable question for GPT-3
        for the "Worst possible idea" workshops
        """
        return self._process_text("What is the worst possible idea about", "?")

    def process_free_text(self) -> str:
        """
        A Function to take a free text input
        to generate ideas from GPT3 during a workshop
        """
        return self._process_text("", "")

    def process_avalanche(self) -> list:
        """
        A Function that prepares usable question for GPT-3
        for the "Ideas Avalanche" workshops
        """
        text_list = []
        for letter in string.ascii_lowercase:
            text = f"Give an idea starting with the letter: {letter}, about this topic:"
            append_text = self._process_text(text, "")
            text_list.append(append_text)

        # TODO needs to be completed with option to select a single letter

        return text_list

    def process_crazy_text(self) -> str:
        return self._process_text("Give a completely crazy new idea for this topic:", "")

    def process_normal_text(self) -> str:
        return self._process_text("Give a new idea for this topic:", "")

    def _process_text(self, start_text: str = "", end_text: str = "") -> str:
        problem = self.input_data
        if not problem:
            raise ValueError(" Please enter your text")
        if len(problem) <= 200:
            self.output_data = f"{start_text} {problem} {end_text}"
        else:
            raise ValueError("Too long! Only 200 characters allowed!")
        return self.output_data
