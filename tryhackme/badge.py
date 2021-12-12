

class Badge:
    __slots__ = ("_state", "_to_earn", "title", "name", "description", "earned", )
    
    def __init__(self, state, data):
        self._state = state
        self.earned = False
        self._from_data(data)
    
    def _from_data(self, data):
        self.title = data.get("title")
        self.name = data.get("name")
        self.description = data.get("description")
        self._to_earn = data.get("toEarn", [])
    
    @property
    def to_earn(self):
        return [self._state.get_room(room_code) for room_code in self._to_earn]