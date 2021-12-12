import re
import sys
from urllib.parse import quote as _uriquote

import requests

from . import __version__, errors, utils
from .converters import _county_types, _leaderboard_types, _vpn_types, _not_none
from . import checks
from .cog import request_cog

GET='get'
POST='post'


class HTTPClient:
    __CSRF_token_regex = re.compile("const csrfToken[ ]{0,1}=[ ]{0,1}[\"|'](.{36})[\"|']")
    __Username_regex   = re.compile("const username[ ]{0,1}=[ ]{0,1}[\"|'](.{1,16})[\"|']")
    
    def __init__(self, session=None):
        self._state = None
        self.authenticated = False
        self.__session = requests.Session()
        self.static_session = requests.Session()
        self.connect_sid = None
        self._CSRF_token = None
        self.username = None
        
        self.user_agent = f'Tryhackme: (https://github.com/GnarLito/thm-api-py {__version__}) Python/{sys.version_info[0]}.{sys.version_info[1]} requests/{requests.__version__}'
        
        if session is not None:
            self.static_login(session)
    
    def close(self):
        if self.__session:
            self.__session.close()
    
    def static_login(self, session):
        self.connect_sid = session
        cookie = requests.cookies.create_cookie('connect.sid', session, domain='tryhackme.com')
        self.__session.cookies.set_cookie(cookie)
        try: 
            self.request(RouteList.get_unseen_notifications())
            self.authenticated = True
            self._CSRF_token = self.retrieve_CSRF_token()
            self.username = self.retrieve_username()
        except Exception as e:
            print("session Issue:", e)
    
    def retrieve_CSRF_token(self):
        if not self.authenticated:
            return None
        try:
            page = self.request(RouteList.get_profile_page())
            return self._HTTPClient__CSRF_token_regex.search(page).group(1)
        except AttributeError:
            self.authenticated = False
            return None

    def retrieve_username(self):
        if not self.authenticated:
            return None
        try:
            page = self.request(RouteList.get_profile_page())
            return self._HTTPClient__Username_regex.search(page).group(1)
        except AttributeError:
            self.authenticated = False
            return None
    
    def request(self, route, **kwargs):
        session = self.__session
        endpoint = route.url
        method = route.method
        settings = kwargs.pop('settings', {})
        
        headers = {
            'User-Agent': self.user_agent
        }
        
        if 'json' in kwargs:
            headers['Content-Type'] = 'application/json'
            kwargs['data'] = utils.to_json(kwargs.pop('json'))
        
        if "static" in settings:
            session = self.static_session
        if "CSRF" in settings:
            headers['CSRF-Token'] = self._CSRF_token
            kwargs["data"]["_CSRF"] = self._CSRF_token

        # TODO: retries, Pagenator
        try:
            with session.request(method, endpoint, **kwargs) as r:
                
                data = utils.response_to_json_or_text(r)
                
                # * valid return
                if 300 > r.status_code >= 200:

                    # $ if return url is login then no auth
                    if r.url.split('/')[-1] == "login":
                        raise errors.Unauthorized(request=r, route=route, data=data)

                    return data
                
                # $ no auth
                if r.status_code in {401, 403}:
                    raise errors.Unauthorized(request=r, route=route, data=data)
                
                # $ endpoint not found
                if 404 == r.status_code:
                    raise errors.NotFound(request=r, route=route, data=data)
                
                # $ server side issue's
                if r.status_code in {500, 502}:
                    raise errors.ServerError(request=r, route=route, data=data)
        
        except Exception as e:           
            raise e


class Route:
    # TODO: add post payload capabilities
    BASE = "https://www.tryhackme.com"
    def __init__(self, method=GET, path='', **parameters):
        self.method = method
        self._path = path
        self.path = path
        url = self.BASE + self.path
        
        options = parameters.pop("options", None)
        if parameters:
            try:
                self.path = self.path.format(**{k: _uriquote(v) if isinstance(v, str) else v for k, v in parameters.items()})
                self.url = self.BASE + self.path
            except Exception as e:
                raise errors.NotValidUrlParameters(e)
        else:
            self.url = url
        
        if options:
            if "?" not in self.url:
                self.url + "?" + "&".join([f"{i}={options[i]}" for i in options.keys() if options[i] != None])
            else:
                self.url + "&" + "&".join([f"{i}={options[i]}" for i in options.keys() if options[i] != None])
        
        self.bucket = f"{method} {path}"


class RouteList:
    def get_profile_page(**parameters): return Route(path="/profile", **parameters)
    
    # * normal site calls
    
    def get_server_time(    **parameters): return Route(path="/api/server-time",        **parameters)
    def get_site_stats(     **parameters): return Route(path="/api/site-stats",         **parameters)
    def get_practise_rooms( **parameters): return Route(path="/api/practice-rooms",     **parameters)
    def get_series(         **parameters): return Route(path="/api/series?show={show}", **parameters)
    def get_glossary_terms( **parameters): return Route(path="/glossary/all-terms",     **parameters)
    
    # * Leaderboards
    
    def get_leaderboards(     **parameters): return Route(path="/api/leaderboards",      **parameters)
    def get_koth_leaderboards(**parameters): return Route(path="/api/leaderboards/koth", **parameters)
    
    # * networks
    
    def get_networks(     **parameters): return Route(path="/api/networks",                         **parameters)
    def get_network(      **parameters): return Route(path="/api/room/network?code={network_code}", **parameters)
    def get_network_cost( **parameters): return Route(path="/api/room/cost?code={network_code}",    **parameters)
    
    # * account
    
    def get_subscription_cost(**parameters): return Route(path="/account/subscription/cost", **parameters)
    
    # * paths
    
    def get_path(           **parameters): return Route(path="/paths/single/{path_code}",  **parameters)
    def get_public_paths(   **parameters): return Route(path="/paths/public",              **parameters)
    def get_path_summary(   **parameters): return Route(path="/paths/summary",             **parameters)
    
    # * modules
    
    def get_modules_summary(**parameters): return Route(path="/modules/summary",           **parameters)
    def get_module(         **parameters): return Route(path="/modules/data/{module_code}",**parameters)
    
    # * games
    
    def get_machine_pool(    **parameters):  return Route(path="/games/koth/get/machine-pool",           **parameters)
    def get_game_detail(     **parameters):  return Route(path="/games/koth/data/{game_code}",           **parameters)
    def get_recent_games(    **parameters):  return Route(path="/games/koth/recent/games",               **parameters)
    def get_user_games(      **parameters):  return Route(path="/games/koth/user/games",                 **parameters)
    def get_game_tickets_won(**parameters):  return Route(path="/games/tickets/won?username={username}", **parameters)
    def post_join_koth(      **parameters):  return Route(method=POST, path="/games/koth/new",           **parameters) 
    def post_new_koth(       **parameters):  return Route(method=POST, path="/games/koth/join-public",   **parameters) # ? might be different for premium users
    
    # * VPN
    
    def get_available_vpns(**parameters): return Route(path="/vpn/get-available-vpns", **parameters)
    def get_vpn_info(      **parameters): return Route(path="/vpn/my-data",            **parameters)
    
    # * VM
    
    def get_machine_running(    **parameters): return Route(path="/api/vm/running",                **parameters)
    def post_renew_machine(     **parameters): return Route(method=POST, path="/api/vm/renew",     **parameters)
    def post_terminate_machine( **parameters): return Route(method=POST, path="/api/vm/terminate", **parameters)
    
    # * user -badge
    
    def get_own_badges( **parameters): return Route(path="/api/badges/mine",           **parameters)
    def get_user_badges(**parameters): return Route(path="/api/badges/get/{username}", **parameters)
    def get_all_badges( **parameters): return Route(path="/api/badges/get",            **parameters)
    
    # * user -team
    
    def get_team_info(**parameters): return Route(path="/api/team/is-member", **parameters)
    
    # * user -notifications
    
    def get_unseen_notifications(**parameters): return Route(path="/notifications/has-unseen", **parameters)
    def get_all_notifications(   **parameters): return Route(path="/notifications/get",        **parameters)
    
    # * user -messages
    
    def get_unseen_messages(   **parameters): return Route(path="/message/has-unseen",              **parameters)
    def get_all_group_messages(**parameters): return Route(path="/message/group/get-all",           **parameters)
    def get_group_messages(    **parameters): return Route(path="/message/group/get/{group_id}",    **parameters)
    
    # * user -room
    
    def get_user_completed_rooms_count( **parameters): return Route(path="/api/no-completed-rooms-public/{username}",    **parameters)
    def get_user_completed_rooms(       **parameters): return Route(path="/api/all-completed-rooms?username={username}", **parameters)
    def get_user_created_rooms(         **parameters): return Route(path="/api/created-rooms/{username}",                **parameters)
    
    # * user
    
    def get_user_rank(   **parameters): return Route(path="/api/user/rank/{username}",                     **parameters)
    def get_user_activty(**parameters): return Route(path="/api/user/activity-events?username={username}", **parameters)
    def get_all_friends( **parameters): return Route(path="/api/friend/all",                               **parameters)
    def get_discord_user(**parameters): return Route(path="/api/discord/user/{username}",                  **parameters) # ? rename to user profile
    def get_user_exist(  **parameters): return Route(path="/api/user/exist/{username}",                    **parameters)
    def search_user(     **parameters): return Route(path="/api/similar-users/{username}",                 **parameters)
    
    # * room
    
    def get_new_rooms(           **parameters): return Route(path="/api/new-rooms",                        **parameters)
    def get_recommended_rooms(   **parameters): return Route(path="/recommend/last-room?type=json",        **parameters)
    def get_questions_answered(  **parameters): return Route(path="/api/questions-answered",               **parameters)
    def get_joined_rooms(        **parameters): return Route(path="/api/my-rooms",                         **parameters)
    def get_room_percetages(     **parameters): return Route(method=POST, path="/api/room-percentages",    **parameters) # ? is a post but it gets stuff
    def get_room_scoreboard(     **parameters): return Route(path="/api/room/scoreboard?code={room_code}", **parameters)
    def get_room_votes(          **parameters): return Route(path="/api/room/votes?code={room_code}",      **parameters)
    def get_room_details(        **parameters): return Route(path="/api/room/details?codes={room_code}",   **parameters) # ? list posibility
    def get_room_tasks(          **parameters): return Route(path="/api/tasks/{room_code}",                **parameters)
    def post_room_answer(        **parameters): return Route(method=POST, path="/api/{room_code}/answer",  **parameters)
    def post_deploy_machine(     **parameters): return Route(method=POST, path="/material/deploy",         **parameters)
    def post_reset_room_progress(**parameters): return Route(method=POST, path="/api/reset-progress",      **parameters)
    def post_leave_room(         **parameters): return Route(method=POST, path="/api/room/leave",          **parameters)


class HTTP(request_cog, HTTPClient):
    # * normal site calls
    
    def get_server_time(self, **attrs):
        return self.request(RouteList.get_server_time(), **attrs)
    def get_site_stats(self, **attrs):
        return self.request(RouteList.get_site_stats(), **attrs)
    def get_practise_rooms(self, **attrs): 
        return self.request(RouteList.get_practise_rooms(), **attrs)
    def get_serie(self, show, serie_code, **attrs):
        return self.request(RouteList.get_series(show=show, options={"name": serie_code}), **attrs)
    def get_series(self, show, **attrs):
        return self.request(RouteList.get_series(show=show), **attrs)
    def get_glossary_terms(self, **attrs): 
        return self.request(RouteList.get_glossary_terms(), **attrs)
    
    # * Leaderboards
    def get_leaderboards(self, country: _county_types, type:_leaderboard_types, **attrs):
        return self.request(RouteList.get_leaderboards(country=country.to_lower_case(), type=type), **attrs)
    def get_koth_leaderboards(self, country: _county_types, type:_leaderboard_types, **attrs):
        return self.request(RouteList.get_koth_leaderboards(country=country.to_lower_case(), type=type), **attrs)

    # * networks
    
    def get_network(self, network_code, **attrs): 
        return self.request(RouteList.get_network(network_code=network_code), **attrs)
    def get_networks(self, **attrs): 
        return self.request(RouteList.get_networks(),**attrs)
    def get_network_cost(self, network_code, **attrs): 
        return self.request(RouteList.get_networks(network_code=network_code), **attrs)
    
    # * account
    @checks.is_authenticated()
    def get_subscription_cost(self, **attrs): 
        return self.request(RouteList.get_subscription_cost(), **attrs)
    
    # * paths
    
    def get_path(self, path_code, **attrs):
        return self.request(RouteList.get_path(path_code=path_code), **attrs)
    def get_public_paths(self, **attrs):
        return self.request(RouteList.get_public_paths(), **attrs)
    def get_path_summary(self, **attrs):
        return self.request(RouteList.get_path_summary(), **attrs)
    
    # * modules
    
    def get_modules_summary(self, **attrs):
        return self.request(RouteList.get_modules_summary(), **attrs)
    def get_module(self, module_code, **attrs):
        return self.request(RouteList.get_module(module_code), **attrs)
    
    # * games
    
    def get_machine_pool(self, **attrs):
        return self.request(RouteList.get_machine_pool(), **attrs)
    def get_game_detail(self, game_code, **attrs):
        return self.request(RouteList.get_game_detail(game_code=game_code), **attrs)
    def get_recent_games(self, **attrs):
        return self.request(RouteList.get_recent_games(), **attrs)
    def get_user_games(self, **attrs):
        return self.request(RouteList.get_user_games(), **attrs)
    def get_game_tickets_won(self, username, **attrs):
        return self.request(RouteList.get_game_tickets_won(username=username), **attrs)
    @checks.set_header_CSRF()
    def post_join_koth(self, **attrs):
        return self.request(RouteList.post_join_koth(), **attrs)
    @checks.set_header_CSRF()
    def post_new_koth(self, **attrs):
        return self.request(RouteList.post_new_koth(), **attrs)
    
    # * VPN
    @checks.is_authenticated()
    def get_available_vpns(self, type : _vpn_types, **attrs):
        return self.request(RouteList.get_available_vpns(options={"type": type}), **attrs)
    @checks.is_authenticated()
    def get_vpn_info(self, **attrs):
        return self.request(RouteList.get_vpn_info(), **attrs)
    
    # * VM

    def get_machine_running(self, **attrs):
        return self.request(RouteList.get_machine_running(), **attrs)
    @checks.set_header_CSRF()
    def post_renew_machine(self, room_code, **attrs):
        return self.request(RouteList.post_renew_machine(), json={"code": room_code}, **attrs)
    @checks.set_header_CSRF()
    def post_terminate_machine(self, room_code, **attrs):
        return self.request(RouteList.post_terminate_machine(), json={"code": room_code}, **attrs)
    
    # * user -badge
    @checks.is_authenticated()
    def get_own_badges(self, **attrs):
        return self.request(RouteList.get_own_badges(), **attrs)
    def get_user_badges(self, username, **attrs):
        return self.request(RouteList.get_user_badges(username=username), **attrs)
    def get_all_badges(self, **attrs):
        return self.request(RouteList.get_all_badges(), **attrs)
    
    # * user -team
    @checks.is_authenticated()
    def get_team_info(self, **attrs): 
        return self.request(RouteList.get_team_info(), **attrs)
    
    # * user -notifications
    @checks.is_authenticated()
    def get_unseen_notifications(self, **attrs):
        return self.request(RouteList.get_unseen_notifications(), **attrs)
    @checks.is_authenticated()
    def get_all_notifications(self, **attrs):
        return self.request(RouteList.get_all_notifications(), **attrs)

    # * user -messages

    @checks.is_authenticated()
    def get_unseen_messages(self, **attrs):
        return self.request(RouteList.get_unseen_messages(), **attrs)
    @checks.is_authenticated()
    def get_all_group_messages(self, **attrs):
        return self.request(RouteList.get_all_group_messages(), **attrs)
    @checks.is_authenticated()
    def get_group_messages(self, group_id, **attrs):
        return self.request(RouteList.get_group_messages(group_id), **attrs)
    
    # * user -room

    def get_user_completed_rooms_count(self, username, **attrs):
        return self.request(RouteList.get_user_completed_rooms_count(username=username), **attrs)
    def get_user_completed_rooms(self, username, limit:int=10, page:int=1, **attrs):
        return self.request(RouteList.get_user_completed_rooms(username=username, options={"limit": limit, "page": page}), **attrs)
    def get_user_created_rooms(self, username, limit:int=10, page:int=1, **attrs):
        return self.request(RouteList.get_user_created_rooms(username=username, options={"limit": limit, "page": page}), **attrs)

    # * user

    def get_user_rank(self, username : _not_none, **attrs):
        return self.request(RouteList.get_user_rank(username=username), **attrs)
    def get_user_activty(self, username : _not_none, **attrs):
        return self.request(RouteList.get_user_activty(username=username), **attrs)
    @checks.is_authenticated()
    def get_all_friends(self, **attrs):
        return self.request(RouteList.get_all_friends(), **attrs)
    def get_discord_user(self, username : _not_none, **attrs):
        return self.request(RouteList.get_discord_user(username=username), **attrs)
    def get_user_exist(self, username : _not_none, **attrs):
        return self.request(RouteList.get_user_exist(username=username), **attrs)
    def search_user(self, username : _not_none, **attrs):
        return self.request(RouteList.search_user(username=username), **attrs)

    # * room

    def get_new_rooms(self, **attrs):
        return self.request(RouteList.get_new_rooms(), **attrs)
    @checks.is_authenticated()
    def get_recommended_rooms(self, **attrs):
        return self.request(RouteList.get_recommended_rooms(), **attrs)
    def get_questions_answered(self, **attrs):
        return self.request(RouteList.get_questions_answered(), **attrs)
    @checks.is_authenticated()
    def get_joined_rooms(self, **attrs):
        return self.request(RouteList.get_joined_rooms(), **attrs)
    @checks.is_authenticated()
    def get_room_percentages(self, room_codes, **attrs):
        return self.request(RouteList.get_room_percetages(), json={"rooms": room_codes}, **attrs)
    @checks.is_authenticated()
    def get_room_scoreboard(self, room_code, **attrs):
        return self.request(RouteList.get_room_scoreboard(room_code=room_code), **attrs)
    def get_room_votes(self, room_code, **attrs):
        return self.request(RouteList.get_room_votes(room_code=room_code), **attrs)
    def get_room_details(self, room_code, loadWriteUps: bool=True, loadCreators: bool=True, loadUser: bool=True, **attrs):
        return self.request(RouteList.get_room_details(room_code=room_code, options={"loadWriteUps": loadWriteUps, "loadCreators": loadCreators, "loadUser": loadUser}), **attrs).get(room_code, {})
    def get_room_tasks(self, room_code, **attrs):
        return self.request(RouteList.get_room_tasks(room_code=room_code), **attrs)
    @checks.set_header_CSRF()
    @checks.is_authenticated()
    def post_room_answer(self, room_code, taskNo: int, questionNo: int, answer: str, **attrs):
        return self.request(RouteList.post_room_answer(room_code=room_code), json={"taskNo": taskNo, "questionNo": questionNo, "answer": answer}, **attrs)
    @checks.set_header_CSRF()
    @checks.is_authenticated()
    def post_deploy_machine(self, room_code, uploadId, **attrs):
        return self.request(RouteList.post_deploy_machine(), json={"roomCode": room_code, "id": uploadId}, **attrs)
    @checks.set_header_CSRF()
    @checks.is_authenticated()
    def post_reset_room_progress(self, room_code, **attrs):
        return self.request(RouteList.post_reset_room_progress(), json={"code": room_code}, **attrs)
    @checks.set_header_CSRF()
    @checks.is_authenticated()
    def post_leave_room(self, room_code, **attrs):
        return self.request(RouteList.post_leave_room(), json={"code": room_code}, **attrs)
