from .user import KOTHUser

class KingoftheHill:
    __slot__ = ("__weakref__", "_state", "id", "start_time", "finnish_time", "status", "flag_count", "resets", "game_type", "ceator", "users", "King", )
    
    def __init__(self, state, data):
        self._state = state
        
        self._from_data(data)
    
    def _from_data(self, data):
        self.id = data.get("id")
        self.start_time = data.get("startTime")
        self.finnish_time = data.get("finnishTime")
        self.status = data.get("status")
        self.flag_count = data.get("flagNo")
        self.resets = data.get("resets")
        self.game_type = data.get("gameType")
        self.creator = self._state.get_user(data.get("createdBy", {}).get("username", None))
        self.users = [KOTHUser(state=self._state, data=user) for user in data.get("tableData", [])]
        
        try:
            self.king = [user for user in self.users if user.name == data.get("king").get("username")][0]
        except KeyError:
            self.king = None
    