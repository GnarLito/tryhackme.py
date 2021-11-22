import weakref

from .room import Room
from .path import Path
from .module import Module
from .user import User
from .serie import Serie
from .network import Network
from .vpn import VPN
from .http import HTTP

# TODO: vpn
class State:
    def __init__(self, http : HTTP):
        self.http = http
        self.user = None
        self._CRRF_token = self.http._CSRF_token
                
        self._rooms = weakref.WeakValueDictionary()
        self._paths = weakref.WeakValueDictionary()
        self._modules = weakref.WeakValueDictionary()
        self._users = weakref.WeakValueDictionary()
        self._badges = weakref.WeakValueDictionary()
        self._series = weakref.WeakValueDictionary()
        self._networks = weakref.WeakValueDictionary()
        self.vpn = [] # ? hmm
    
    
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
    
    # TODO: badge class redirect temp workaround issue/#6 
    @property
    def badges(self):
        badge_list = []
        if self._badges.__len__() < 1:
            for badge in self.http.get_all_badges(): badge_list.append(self.store_badge(badge))
        
        return badge_list
        # return list(self._badges.values())
    def store_badge(self, data):
        badge_code = data.get("name")
        try:
            return self._badges[badge_code]
        except KeyError:
            # badge = Badge(state=self, data=data)
            badge = data
            # self._badges[badge_code] = badge
            return badge
    def get_badge(self, badge_name):
        try:
            return self._badges[badge_name]
        except KeyError:
            badge_data = [badge for badge in self.http.get_all_badges() if badge.get("name") == badge_name]
            return self.store_badge(badge_data)
    
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
    def authenticated(self):
        return self.http.authenticated
    @property
    def subscribed(self):
        if self.authenticated:
            return self.user.subscribed
        else:
            return False