from .errors import *

class http_ctx:
    def __init__(self, state, **attrs):
        self._state = state
        self.args = attrs.get("args", [])
        self.kwargs = attrs.get("kwargs", {})
        self.client_user = self._state.user
    
    def add_arg(self, *args, **kwargs):
        if args.__len__() > 0:
            self.args.extend(args)
        elif kwargs.__len__() > 0:
            for key in kwargs:
                if key in self.kwargs:
                    if type(self.kwargs.get(key)) is list:
                        if type(kwargs.get(key))  is list:
                            self.kwargs.get(key).extend(kwargs.get(key))
                        else:
                            self.kwargs.get(key).append(kwargs.get(key))
                    elif type(self.kwargs.get(key)) is tuple:
                        if    type(kwargs.get(key)) is tuple:
                            self.kwargs[key] += kwargs.get(key)
                        elif  type(kwargs.get(key)) is list:
                            self.kwargs[key] += tuple(kwargs.get(key))
                        else:
                            self.kwargs[key] += (kwargs.get(key), )
                    else:
                        self.kwargs[key] = kwargs.get(key)
                else:
                    self.kwargs[key] = kwargs.get(key)
        else:
            raise MissingArgumentError()
    
    @property
    def authenticated(self):
        return self._state.authenticated