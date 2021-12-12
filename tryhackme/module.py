

class Module:
    __slots__ = ("__weakref__", "_state", "_rooms", "_prerequisites", "_next_steps", "name", "code", "id", "description", "summary", )
    
    def __init__(self, state, data):
        self._state = state
        
        self._from_data(data)
    
    def _from_data(self, data):
        self.name = data.get('moduleURL').replace('-', ' ') # * the api leaves this http save
        self.code = data.get('moduleURL')
        self.id = data.get('id')
        self.description = data.get('description')
        self.summary = data.get('summary')
        self._rooms = data.get('rooms')
        self._prerequisites = data.get('prerequisites')
        self._next_steps = data.get('nextSteps')

    @property
    def rooms(self):
        return [self._state.store_room(room) for room in self._rooms]
    @property
    def prerequisites(self):
        return [self._state.store_module(module) for module in self._prerequisites]
    @property
    def next_steps(self):
        return [self._state.store_module(module) for module in self._next_steps]

