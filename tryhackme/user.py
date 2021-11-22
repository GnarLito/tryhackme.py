from .message import MessageGroup
from .errors import NotImplemented
from .team import Team

# TODO: add message/notification class 
class User:
    def __init__(self, state, username):
        self._state = state
        
        self.name = username
        self._completed_rooms = []
        
        if username is None or not self._state.http.get_user_exist(username=self.name).get('success', False):
            raise NotImplemented("Unknown user with username: "+ str(self.name))
        
        data = self._fetch()
        self._from_data(data)
    # TODO: fetch is a mess, needs fixing
    def _fetch(self):
        data = {}
        data['badges'] = self._state.http.get_user_badges(username=self.name)
        data['rank'] = self._state.http.get_discord_user(username=self.name)
        data['completed_rooms'] = self._state.http.get_user_completed_rooms(username=self.name)
        return data
    
    def _from_data(self, data):
        self._badges = data.get('badges')
        self.rank = data.get('rank').get('userRank')
        self.points = data.get('rank').get('points')
        self.subscribed = data.get('rank').get('subscribed')
        self._completed_rooms = data.get('completed_rooms')

    @property
    def completed_rooms(self):
        return [self._state.store_room(data=data) for data in self._completed_rooms]
    @property
    def badges(self):
        return [self._state.get_badge(badge_code.get("name")) for badge_code in self._badges]


class ClientUser(User):
    def __init__(self, state, username):
        super().__init__(state, username)
        
        self.message_groups = []
        data = self._fetch()
        self._from_data(data)
    
    def _fetch(self):
        data = {}
        data['team'] = self._state.http.get_team_info()
        return data
    
    def _from_data(self, data):
        self.team = Team(state=self._state, data=data.get("team"))
        
        self._sync()
    
    def _sync(self):
        self.message_groups = [MessageGroup(state=self._state, data=group) for group in self._state.http.get_all_group_messages()]
    