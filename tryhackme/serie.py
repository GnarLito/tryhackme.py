

class Serie:
    __slots__ = ("__weakref__", "_state", "_rooms", "id", "code", "name", "description", "difficulty", )
    def __init__(self, state, data):
        self._state = state
        
        self._from_data(data)
    
    def _from_data(self, data):
        self.id = data.get("_id")
        self.code = data.get("id")
        self.name = data.get("name")
        self.description = data.get("description")
        self.difficulty = data.get("difficulty")
        self._rooms = data.get("rooms")

        self._sync(data)

    def _sync(self, data):
        self._badge = self._state.store_badge(data.get("badge"))
        
    @property
    def rooms(self):
        return [self._state.get_room(room.get("code")) for room in self._rooms]
    