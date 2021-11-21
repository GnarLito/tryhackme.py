from .question import Question

# TODO: html elements removing
class RoomTask:
    def __init__(self, state, data):
        self._state = state
        self._questions = []
        
        self._from_data(data)
    
    def _from_data(self, data):
        self.title = data.get('taskTitle')
        self.description = data.get('taskDesc')
        self.type = data.get('taskType')
        self.number = data.get('taskNo')
        self.created = data.get('taskCreated')
        self.deadline = data.get('taskDeadline')
        self.uploadId = data.get('uploadId')
        self._questions = data.get('tasksInfo', []) if self._state.authenticated else data.get('questions', [])

    @property
    def question_count(self):
        return self._questions.__len__()
    @property
    def questions(self):
        return [Question(state=self._state, data=question) for question in self._questions]


class PathTask:
    def __init__(self, state, data):
        self.state = state
        self._rooms = []
        self._from_data(data)
    
    def _from_data(self, data):
        self.id = data.get("_id")
        self.title = data.get("title")
        self._moduleURL = data.get("moduleURL")
        self.time = int(data.get("time"))
        self.overview = data.get("overview")
        self.outcomes = data.get("outcome")
        self.number = data.get("taskNo")
        self._rooms = data.get("rooms", [])
    
    @property
    def rooms(self):
        return [self._state.get_room(room_code=room.get("code")) for room in self._rooms]
    @property
    def module(self):
        return self._state.get_module(moduleURL=self._moduleURL)
