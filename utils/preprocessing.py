import os


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
        for the "How might we..?" workshops
        """
        return self._process_text("How might we", "?")

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

    def process_crazy_text(self) -> str:
        return self._process_text("Give a completely crazy new idea for this topic:", "")

    def process_normal_text(self) -> str:
        return self._process_text("Give a new idea for this topic:", "")

    def _process_text(self, start_text: str = "", end_text: str = "") -> str:
        problem = self.input_data
        if not problem:
            raise ValueError(" Please enter your text")
        if len(problem) <= 50:
            self.output_data = f"{start_text} {problem} {end_text}"
        else:
            raise ValueError("Too long! Only 50 characters allowed!")
        return self.output_data
