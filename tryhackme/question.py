
# TODO: de HTML all the things
class Question:
    def __init__(self, state, data):
        self._state = state
        self._from_data(data)
        
    def _from_data(self, data):
        self.question = data.get("question")
        self.number = data.get("questionNo")
        self.hint = data.get("hint")
        self.description = data.get("answerDesc", None)
        self.extra_points = data.get("extraPoints", None)
        self.correct = data.get("correct", False)
        self.attempts = data.get("attempts", None)
        self.submission = data.get("submission", None)
        self.has_answer = data.get("noAnswer", False)