from . import utils

class Question:
    def __init__(self, state, data):
        self._state = state
        self._from_data(data)
        
    def _from_data(self, data):
        self.raw_question = data.get("question")
        self.question = utils.HTML_parse(self.raw_question)
        self.raw_hint = data.get("hint")
        self.hint = utils.HTML_parse(self.raw_hint)
        self.number = data.get("questionNo")

        # * only when valid session is used
        self.raw_description = data.get("answerDesc", "")
        self.description = utils.HTML_parse(self.raw_description)
        self.extra_points = data.get("extraPoints", None)
        self.correct = data.get("correct", False)
        self.attempts = data.get("attempts", 0)
        self.submission = data.get("submission", "")
        self.has_answer = not data.get("noAnswer", False)
    