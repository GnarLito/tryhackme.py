

class Team:
    __slots__ = ("_state", "_members", "name", "captain", "password", "university", )
    
    def __init__(self, state, data):
        self._state = state
        
        if data.get("found", False):
            self._from_data(data)
    
    def _from_data(self, data):
        self.name = data.get("name")
        self._members = data.get("members")
        self.captain = self._state.get_user(data.get("captain"))
        self.password = data.get("password")
        self.university = data.get("university")
    
    @property
    def members(self):
        return [self._state.get_user(user) for user in self._members]