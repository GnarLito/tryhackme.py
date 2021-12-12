from .errors import *

def check(predicate):
    def decorator(func):
        if not hasattr(func, '__checks__'):
            func.__checks__ = []
        func.__checks__.append(predicate)
        return func
    
    decorator.predicate = predicate
    return decorator

def arg_injector(predicate):
    def decorator(func):
        if not hasattr(func, '__arg_injectors__'):
            func.__arg_injectors__ = []
        func.__arg_injectors__.append(predicate)
        return func
    
    decorator.predicate = predicate
    return decorator


# * HTTP checks

def is_authenticated():
    def predicate(cls):
        if cls.authenticated:
            return True
        raise SessionRequired()
    return check(predicate)


# * HTTP arg injectors

def set_header_CSRF(): # ? if try hack me doesnt accept both at the same time, setting needs to be adjusted acordingly
    def predicate(ctx):
        ctx.add_arg(settings=["CSRF"])
    return arg_injector(predicate)

def set_body_CSRF(): # ? if try hack me doesnt accept both at the same time, setting needs to be adjusted acordingly
    def predicate(ctx):
        ctx.add_arg(settings=["CSRF"])
    return arg_injector(predicate)
