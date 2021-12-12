from .task import PathTask
from . import utils

class Path:
    __slots__ = ("__weakref__", "_state", "_badges", "_careers", "_modules", "_tasks", "code", "raw_description", "color", "raw_intro", "type", "public", "room_count", "summary", "difficult", "time_to_complete", )
    
    def __init__(self, state, data):
        self._state = state
        
        self._badges = []
        self._careers = []
        self._modules = []
        self._tasks = []
        
        self._from_data(data)
    
    def _from_data(self, data):
        self.code = data.get("code")
        self.raw_description = data.get("description")
        self.color = data.get("color")
        self.raw_intro = data.get("intro")
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
    def description(self):
        return utils.HTML_parse(self.raw_description)
    @property
    def intro(self):
        return utils.HTML_parse(self.raw_intro)
    @property
    def tasks(self):
        return [PathTask(state=self._state, data=task) for task in self._tasks]
    @property
    def modules(self):
        return [self._state.store_module(module) for module in self._module]
    @property
    def badges(self):
        return [self._state.store_badge(badge) for badge in self._badges]
    @property
    def careers(self): # ? What is this
        return [career for career in self._careers]
