from . import utils

class Question:
    __slots__ = ("_state", "raw_question", "question", "raw_hint", "hint", "number", "raw_description", "description", "extra_points", "correct", "attempts", "submission", "has_answer", )
    
    def __init__(self, state, data):
        self._state = state
        self._from_data(data)
        
    def _from_data(self, data):
        self.raw_question = data.get("question")
        self.question = utils.HTML_parse(self.raw_question).strip()
        self.raw_hint = data.get("hint")
        self.hint = utils.HTML_parse(self.raw_hint).strip()
        self.number = data.get("questionNo")

        # * only when authenticated
        self.raw_description = data.get("answerDesc", "")
        self.description = utils.HTML_parse(self.raw_description).strip()
        self.extra_points = data.get("extraPoints", None)
        self.correct = data.get("correct", False)
        self.attempts = data.get("attempts", 0)
        self.submission = data.get("submission", "")
        self.has_answer = not data.get("noAnswer", False)
    