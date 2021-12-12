from .http import HTTP
from .state import State
from .user import ClientUser
from .game import KingoftheHill

class Client:
    def __init__(self, session=None):
        self.http = HTTP()
        self._state = State(self.http)
        
        if(session is not None):
            self.login(session)
        
    def login(self, session):
        self.http.static_login(session)
        if self._state.authenticated:
            try:
                self._state.user = ClientUser(state=self._state, username=self.http.username)
            except Exception as e:
                print("Failed to create CLient user: ", str(e))
                self._state.authenticated = False
    
    def get_room(self, room_code):
        try:
            return self._state.get_room(room_code)
        except Exception as e:
            raise e # * pre definition for when exception overruling is needed
    
    def get_path(self, path_code):
        try:
            return self._state.get_path(path_code)
        except Exception as e:
            raise e # * pre definition for when exception overruling is needed

    def get_module(self, module_code):
        try:
            return self._state.get_module(module_code)
        except Exception as e:
            raise e # * pre definition for when exception overruling is needed
    
    def get_user(self, username):
        try:
            return self._state.get_user(username)
        except Exception as e:
            raise e # * pre definition for when exception overruling is needed
    
    def get_badge(self, badge_name):
        return self._state.get_badge(badge_name)
    def get_badges(self):
        return self._state.badges
    
    def get_practice_rooms(self):
        practice_rooms = self.http.get_practise_rooms()
        return_rooms = []
        return_rooms += [self._state.get_room(room_code=room.get("code")) for room in practice_rooms.get("featured", [])]
        return_rooms += [self._state.get_room(room_code=room.get("code")) for room in practice_rooms.get("webExploitation", [])]
        return_rooms += [self._state.get_room(room_code=room.get("code")) for room in practice_rooms.get("windowsExploitation", [])]
        return_rooms += [self._state.get_room(room_code=room.get("code")) for room in practice_rooms.get("defensive", [])]
        return_rooms += [self._state.get_room(room_code=room.get("code")) for room in practice_rooms.get("recommended", [])]
        return return_rooms

    # ! network is basicly nothing at the moment since i cant access is (im not a premium member)
    def get_network(self, network_code):
        try:
           return self._state.get_network(network_code)
        except Exception as e:
            raise e # * pre definition for when exception overruling is needed
    
    # ! Not Implemented (hacktivities API)
    # def search_room(self, room_code, page=1, order=None, difficulty=None, type=None, free=None, limit=None):
        # try:
        #     return self.http.search_room(room_code, page=page, order=order, difficulty=difficulty, type=type, free=free, limit=limit)
        # except Exception as e:
            # raise e # * pre definition for when exception overruling is needed
    
    def search_user(self, username):
        try:
            return self.http.search_user(username=username)
        except Exception as e:
            raise e # * pre definition for when exception overruling is needed
    
    def get_series(self):
        return [self._state.store_serie(data=data) for data in self.http.get_series(show="all")]
    
    def get_serie(self, serie_code):
        return self._state.get_serie(serie_code)
    
    def get_koth_game(self, game_code):
        try:
            game = self.http.get_game_detail(game_code=game_code)
            return KingoftheHill(state=self._state, data=game)
        except Exception as e:
            raise e
    
    def get_leaderboard(self, country=None, type=None):
        return self.http.get_leaderboards(country=country, type=type)
    
    def get_koth_leaderboard(self, country=None, type=None):
        return self.http.get_koth_leaderboards(counrty=country, type=type)
    
    @property
    def server_time(self):
        return self.http.get_server_time().get('datetime')
    @property
    def server_stats(self):
        return self.http.get_site_stats()
    @property
    def subscription_cost(self):
        return self.http.get_subscription_cost()
    @property
    def glossary(self):
        return self.http.get_glossary_terms()
    @property
    def user(self):
        return self._state.user
    @property
    def authenticated(self):
        return self._state.authenticated