from .errors import CheckFailed
from .context import http_ctx


class Base_decorator:
    pass

class Decorator_cog:
    __decorator__ = Base_decorator
    def __init__(self, *args, **kwargs):
        if type(self.__decorator__) == Base_decorator:
            raise NotImplemented("Failed to decorate class, unknown decorator class found")
        
        
        # * Annotations auto decorator
        class_func_list = [i for i in type(self).__dict__ if not i.startswith('__')]
        for func_name in class_func_list:
            class_func = type(self).__dict__[func_name]
            setattr(self, func_name, self.__decorator__(self, class_func))
        super().__init__(*args, **kwargs)

class annotater(Base_decorator):
    def __init__(self, cls, func):
        self.cls = cls
        self.function = func
    
    def __call__(self, *args, **kwargs):
        try:
            args, kwargs = self.convert(*args, **kwargs)
            result = self.function(self.cls, *args, **kwargs)
            return result
        except Exception as e:
            raise e

    def convert(self, *args, **kwargs):
        func_args = [i for i in self.function.__code__.co_varnames if i not in ('self') and not i.startswith("__")]
        annotions = self.function.__annotations__
        out_args = ()
        out_kwargs = {}
        index = 0
        for arg in args:
            if func_args[index] in annotions:
                try:
                    result = self.function.__annotations__[func_args[index]]
                    out_args = (*out_args, result().convert(self.cls, arg))
                except Exception as e:
                    raise e
            else: out_args = (*out_args, arg)
            index += 1
        for arg in kwargs:
            if arg in annotions:
                try:
                    result = self.function.__annotations__[arg]
                    out_kwargs[arg] = result().convert(self.cls, kwargs[arg])
                except Exception as e:
                    raise e
            else: out_kwargs[arg] = kwargs[arg]
                
        return (out_args, out_kwargs)

class request_annotator(annotater):
    def __call__(self, *args, **kwargs):
        try:
            ctx = http_ctx(state=self.cls._state, args=args, kwargs=kwargs)
            ctx.args, ctx.kwargs = self.convert(*ctx.args, **ctx.kwargs) # ? global context needed for convert to accept a context object
            self.arg_injectors(ctx)
            if self.check(ctx):
                result = self.function(self.cls, *ctx.args, **ctx.kwargs)
                return result
            raise CheckFailed()
        except Exception as e:
            print(f"Failed to run: {self.function.__name__}(), reason: {e.__repr__()}")
            return None
    
    def arg_injectors(self, ctx):
        if hasattr(self.function, "__arg_injectors__"):
            for injector in self.function.__arg_injectors__:
                try:
                    injector(ctx)
                except Exception as e:
                    raise e

    def check(self, ctx):
        if hasattr(self.function, "__checks__"):
            for check in self.function.__checks__:
                try:
                    if not check(ctx):
                        return False
                except Exception as e:
                    raise e
        return True

class request_cog(Decorator_cog):
    __decorator__ = request_annotator
    
