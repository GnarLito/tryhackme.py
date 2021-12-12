

class VPN:
    __slots__ = ("_state", "available", "connected", "servers", "unlock_VIP_servers", "current_server", "IP", "public_ip", )
    
    def __init__(self, state):
        self._state = state
        self.available = False
        self.connected = False
        
        self._fetch()
    
    def _fetch(self):
        data = self.http.get_available_vpns()
        info = self.http.get_vpn_info()
        if data.get('success', False):
            self.available = True
            self.servers = data.get('servers')
            self.unlock_VIP_servers = data.get('unlockVIPServers')
            self.current_server = data.get('currentServer')

            self.IP = info.get('virtualIP', None)
            self.public_ip = info.get('publicIP', None)
            
            if self.IP is not None:
                self.connected = True
    