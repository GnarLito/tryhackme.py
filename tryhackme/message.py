from . import utils

class Message:
    __slots__ = ("_state", "group", "inserted", "user", )
    
    def __init__(self, state, group, data):
        self._state = state
        self.group = group
        self._from_data(data)
    
    def _from_data(self, data):
        self.message = data.get("message")
        self.inserted = data.get("inserted")
        self.user = self.group.get_user_from_userId(data.get("userId"))
        

# * can only be used on `get_all_message_groups` api call
class MessageGroup:
    __slots__ = ("_state", "_users", "messages", "id", "title", )
    def __init__(self, state, data):
        self._state = state
        self.messages = []
        self._from_data(data)
        
    def _from_data(self, data):
        self.id = data.get("groupId")
        self.title = data.get("title")
        self._users = data.get("users")
        
        self._sync(data)

    def _sync(self, data):
        self.messages = [Message(state=self._state, group=self, data=message) for message in self._state.http.get_group_messages(self.id)]
        
    @property
    def users(self):
        return [self._stats.store_user(user) for user in self._users]
    
    def get_user_from_userId(self, userId):
        try:
            username = [user.get("username") for user in self._users if user.get("userId") == userId]
            return self._state.get_user(username[0])
        except:
            return None