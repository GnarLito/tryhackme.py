from .errors import NotImplemented
from .team import Team

class BaseUser:
    def __init__(self, state, username):
        self._state = state
        
        if not self._state.http.get_user_exist(username=self.username).get('success', False):
            raise NotImplemented("Unknown user with username: "+ self.username)
        
        self.name = username
        self._completed_rooms = []
        
        data = self._fetch()
        self._from_data(data)
    
    # ? fixable. fetch is a mess, but this is also how tryhackme web does it ..
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
    def badges(self):
        return [self._state.get_badge(badge.get("name")) for badge in self._badges]
    @property
    def completed_rooms(self):
        return [self._state.store_room(room.get("name")) for room in self._completed_rooms]

class User(BaseUser):
    pass

class ClientUser(BaseUser):
    def __init__(self, state, username):
        super().__init__(state, username)
        self._message_groups = []
        self._update()
    
    def _update(self):
        self._message_groups = self._state.http.get_all_message_groups()
        self._team = self._state.http.get_team_info()
        for badge in self._state.badges:
            if [user_badge for user_badge in self.badges if badge.name == user_badge.name].__len__() > 1:
                badge.earned = True
    
    
    # * Team data is semi dynamic, it isnt likly to change much during runtime
    @property
    def team(self):
        return Team(state=self._state, data=self._team)