from .errors import NotImplemented
from .task import RoomTask
from . import utils
# ? writeups class

class Room:
    __slots__ = ("__weakref__", "_state", "_creators", "name", "id", "raw_title", "title", "raw_description", "description", "created", "published", "users", "type", "public", "difficulty", "freeToUse", "ctf", "tags", "ipType", "simpleRoom", "writeups", "locked", "comingSoon", "views", "certificate", "timeToComplete", "userCompleted", )
    
    def __init__(self, state, data):
        self._state = state

        self._creators = []
        
        if not data.get('success', False):
            if data.get("code") == 5:
                raise NotImplemented(f"Room: {data.get('roomCode')}, Unable to load room: {data.get('message')}")
            else:
                raise NotImplemented("failed to create room, no success value returned")
        
        self._from_data(data)
        
    def _from_data(self, data):
        self.name = data.get("roomCode")
        self.id = data.get("roomId")
        self.raw_title = data.get("title")
        self.title = utils.HTML_parse(self.raw_title).strip()
        self.raw_description = data.get("description")
        self.description = utils.HTML_parse(self.raw_description).strip()
        self.created = data.get("created")
        self.published = data.get("published")
        self.users = data.get("users")
        self.type = data.get("type")
        self.public = data.get("public")
        self.difficulty = data.get("difficulty")
        self.freeToUse = data.get("freeToUse")
        self.ctf = data.get("ctf")
        self.tags = data.get("tags")
        self.ipType = data.get("ipType")
        self.simpleRoom = data.get("simpleRoom")
        self.writeups = data.get("writeups")
        self.locked = data.get("locked")
        self.comingSoon = data.get("comingSoon")
        self.views = data.get("views")
        self.certificate = data.get("certificate")
        self.timeToComplete = data.get("timeToComplete")
        self.userCompleted = data.get("userCompleted")
        self._creators = data.get("creators")
    
    @property
    def question_count(self):
        count = 0
        for task in self.tasks:
            count += task.question_count
        return count
    @property
    def precentage(self):
        try: return self._state.http.get_room_percentages(room_codes=self.name)
        except: return {"roomCode": self.name, "correct": 0, "total":self.question_count, "prec": 0}
    @property
    def votes(self):
        return self._state.http.get_room_votes(room_code=self.name)
    @property
    def scoreboard(self):
        return self._state.http.get_room_scoreboard(room_code=self.name)
    @property
    def tasks(self):
        if self.freeToUse or self._state.subscribed:
            return [RoomTask(state=self._state, data=task) for task in self._state.http.get_room_tasks(room_code=self.name).get('data')]
        else:
            return [RoomTask(state=self._state, data=task) for task in self._state.http.get_room_tasks(room_code=self.name, settings=["static"]).get('data')]
    @property
    def creators(self):
        return [self._state.store_user(username=user.get('username')) for user in self._creators]
    