from . import utils

class Message:
    def __init__(self, state, group, data):
        self._state = state
        self.group = group
        self._from_data(data)
    
    def _from_data(self, data):
        self.message = data.get("msg")
        self.inserted = data.get("inserted")
        self.user = utils.find_userId(data.get("userId"), self.group.users)
        

# * can only be used on `get_all_message_groups` api call
class MessageGroup:
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
