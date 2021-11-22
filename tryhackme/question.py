from . import utils

# TODO: de HTML all the things
class Question:
    def __init__(self, state, data):
        self._state = state
        self._from_data(data)
        
    def _from_data(self, data):
        self.raw_question = data.get("question")
        self.number = data.get("questionNo")
        self.raw_hint = data.get("hint")
        self.raw_description = data.get("answerDesc", "")
        self.extra_points = data.get("extraPoints", None)
        self.correct = data.get("correct", False)
        self.attempts = data.get("attempts", 0)
        self.submission = data.get("submission", "")
        self.has_answer = data.get("noAnswer", False)
    
    @property
    def question(self):
        return utils.HTML_parse(self.raw_question)
    @property
    def description(self):
        return utils.HTML_parse(self.raw_description)
    @property
    def hint(self):
        return utils.HTML_parse(self.raw_hint)