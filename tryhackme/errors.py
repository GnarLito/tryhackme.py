
class NotImplemented(Exception):
    pass

class NotValidUrlParameters(Exception):
    def __init__(self, e):
        self.e = e
    def __str__(self):
        return self.e

class WebError(Exception):
    def __init__(self, request, route, data):
        self.request = request
        self.route = route
        self.data = data
    
    def __str__(self):
        return f"{type(self).__name__}(code={self.request.status_code}, URL={self.route.path}, returned_url={self.request.url}, data_length: {self.data.__len__()})"

class Unauthorized(WebError):
    pass

class ServerError(WebError):
    pass

class NotFound(WebError):
    pass


# * Checks

class BaseCheckError(NotImplemented):
    pass

class CheckFailed(BaseCheckError):
    pass

class TypeNotInTypeList(BaseCheckError):
    pass

class SessionRequired(BaseCheckError):
    pass



# * Context

class BaseContextError(NotImplemented):
    pass

class MissingArgumentError(BaseContextError):
    pass