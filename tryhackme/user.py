from .errors import NotImplemented
from .team import Team

# TODO: add message/notification class 
class User:
    def __init__(self, state, username):
        self._state = state
        
        self.username = username
        self._completed_rooms = []
        
        if not self._state.http.get_user_exist(username=self.username).get('success', False):
            raise NotImplemented("Unknown user with username: "+ self.username)
        
        data = self._fetch()
        self._from_data(data)
    # TODO: fetch is a mess, needs fixing
    def _fetch(self):
        data = {}
        data['badges'] = self._state.http.get_user_badges(username=self.username)
        data['rank'] = self._state.http.get_discord_user(username=self.username)
        data['completed_rooms'] = self._state.http.get_user_completed_rooms(username=self.username)
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
        return [self._state.get_badge(badge_code) for badge_code in self._badges]


class ClientUser(User):
    def __init__(self, state, username):
        super().__init__(state, username)
        
        data = self._fetch()
        self._from_data(data)
    
    def _fetch(self):
        data = {}
        data['team'] = self._state.http.get_team_info()
        return data
    
    def _from_data(self, data):
        self.team = Team(state=self._state, data=data.get("team"))