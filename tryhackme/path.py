from .task import PathTask


class Path:
    def __init__(self, state, data):
        self._state = state
        
        self._badges = []
        self._careers = []
        self._modules = []
        self._tasks = []
        
        self._from_data(data)
    
    def _from_data(self, data):
        self.code = data.get("code")
        self.description = data.get("description")
        self.color = data.get("color")
        self.intro = data.get("intro")
        self.type = data.get("contentType")
        self.public = data.get("public", False)
        self.room_count = data.get("roomNo")
        self.summary = data.get("summary")
        self._careers = data.get("careers", [])
        self.difficulty = data.get("easy")
        self.time_to_complete = data.get("timeToComplete")
        self._modules = data.get("modules", [])
        self._badges = data.get("badges", [])
        self._tasks = data.get("tasks", [])
        
        self._sync(data)

    def _sync(self, data):
        self.user = self._state.store_user(data.get('username'))

    @property
    def tasks(self):
        return [PathTask(state=self._state, data=task) for task in self._tasks]
    @property
    def modules(self):
        return [self._state.store_module(module) for module in self._module]
    # TODO: badge class
    @property
    def badges(self):
        return [self._state.store_badge(badge) for badge in self._badges]
    # ? What is this
    @property
    def careers(self):
        return [career for career in self._careers]
