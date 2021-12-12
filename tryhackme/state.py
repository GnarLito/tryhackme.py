import weakref

from .room import Room
from .path import Path
from .module import Module
from .user import User, ClientUser
from .message import MessageGroup
from .team import Team
from .badge import Badge
from .serie import Serie
from .network import Network
from .vpn import VPN
from .http import HTTP
from .errors import NotImplemented

# TODO: vpn
class State:
    def __init__(self, http : HTTP):
        self.http = http
        self.http._state = self
        self.user = None
        self._team = None
        self._CSRF_token = self.http.retrieve_CSRF_token()
        
        self._rooms = weakref.WeakValueDictionary()
        self._paths = weakref.WeakValueDictionary()
        self._modules = weakref.WeakValueDictionary()
        self._users = weakref.WeakValueDictionary()
        self._message_groups = weakref.WeakValueDictionary()
        self._series = weakref.WeakValueDictionary()
        self._networks = weakref.WeakValueDictionary()
        self._badges = {}
        self.vpn = [] # ? hmm
    
    def _sync(self):
        for badge in self.http.get_all_badges(): self.store_badge(badge)
    
    def _clear_client(self):
        self._message_groups = weakref.WeakValueDictionary()
        self._team = None
    
    def _clear_all(self):
        self._rooms = weakref.WeakValueDictionary()
        self._paths = weakref.WeakValueDictionary()
        self._modules = weakref.WeakValueDictionary()
        self._users = weakref.WeakValueDictionary()
        self._message_groups = weakref.WeakValueDictionary()
        self._series = weakref.WeakValueDictionary()
        self._networks = weakref.WeakValueDictionary()
        self._badges = {}
    
    def get_client_user(self):
        return self.user
    
    @property
    def rooms(self):
        return list(self._rooms.values())
    
    def store_room(self, data):
        room_code = data.get("roomCode")
        try:
            return self._rooms[room_code]
        except KeyError:
            room = Room(state=self, data=data)
            self._rooms[room_code] = room
            return room
    def get_room(self, room_code):
        try:
            return self._rooms[room_code]
        except KeyError:
            room_data = self.http.get_room_details(room_code=room_code)
            return self.store_room(room_data)
    
    @property
    def paths(self):
        return list(self._paths.values())
    
    def store_path(self, data):
        path_code = data.get("code")
        try:
            return self._paths[path_code]
        except KeyError:
            path = Path(state=self, data=data)
            self._paths[path_code] = path
            return path
    def get_path(self, path_code):
        try:
            return self._paths[path_code]
        except KeyError:
            path_data = self.http.get_path(path_code=path_code)
            return self.store_path(path_data)
    
    @property
    def modules(self):
        return list(self._modules.values())
    
    def store_module(self, data):
        module_code = data.get("moduleURL")
        try:
            return self._modules[module_code]
        except KeyError:
            module = Module(state=self, data=data)
            self._modules[module_code] = module
            return module
    def get_module(self, module_code):
        try:
            return self._modules[module_code]
        except KeyError:
            module_data = self.http.get_module(module_code=module_code)
            return self.store_module(module_data)
    
    @property
    def users(self):
        return list(self._users.values())
    
    def store_user(self, username):
        try:
            return self._users[username]
        except KeyError:
            user = User(state=self, username=username)
            self._users[username] = user
            return user
    def get_user(self, username):
        try:
            return self._users[username]
        except KeyError:
            return self.store_user(username)
    
    @property
    def badges(self):
        return list(self._badges.values())
    
    def store_badge(self, data):
        badge_name = data.get("name")
        try:
            return self._badges[badge_name]
        except KeyError:
            badge = Badge(state=self, data=data)
            self._badges[badge_name] = badge
            return badge
    def get_badge(self, badge_name):
        try:
            return self._badges[badge_name]
        except KeyError:
            self._sync()
            try:
                return self._badges[badge_name]
            except KeyError:
                raise NotImplemented(f"Badge with name {badge_name} is not found")
    
    @property
    def series(self):
        return list(self._series.values())
    
    def store_serie(self, data):
        serie_code = data.get("id")
        try:
            return self._series[serie_code]
        except KeyError:
            serie = Serie(state=self, data=data)
            self._series[serie_code] = serie
            return serie
    def get_serie(self, serie_code):
        try:
            return self._series[serie_code]
        except KeyError:
            serie_data = self.http.get_serie(serie_code=serie_code)
            return self.store_serie(serie_data)
    
    @property
    def networks(self):
        return list(self._networks.values())
    
    def store_network(self, data):
        network_code = data.get("code")
        try:
            return self._networks[network_code]
        except KeyError:
            network = Network(state=self, data=data)
            self._networks[network_code] = network
            return network
    def get_network(self, network_code):
        try:
            return self._networks[network_code]
        except KeyError:
            network_data = self.http.get_network(network_code=network_code)
            return self.store_network(network_data)

    @property
    def message_groups(self):
        return list(self._message_groups.values())
    
    def store_message_group(self, data):
        group_id = data.get("groupId")
        try:
            return self._message_groups[group_id]
        except KeyError:
            message_group = MessageGroup(state=self, data=data)
            self._message_groups[group_id] = message_group
            return message_group
    def get_message_group(self, group_id):
        try:
            return self._message_groups[group_id]
        except KeyError:
            raise NotImplemented(f"message group with id {group_id} cannot be found")

    @property
    def team(self):
        return self.team

    def store_team(self, data):
        if self._team is not None:
            return self._team
        else:
            team = Team(state=self, data=data)
            self._team = team
            return team

    @property
    def authenticated(self):
        return self.http.authenticated
    
    @property
    def subscribed(self):
        if self.authenticated:
            return self.user.subscribed
        else:
            return False