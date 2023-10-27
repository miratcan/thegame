def renderer_decorator_factory(attr_name):
    def renderer(obj):
        def decorator(func):
            objs = [obj,]
            if isinstance(obj, list):
                objs = obj
            elif isinstance(obj, dict):
                objs = obj.values()
            for box in objs:
                setattr(box, attr_name, func)
        return decorator
    return renderer


fg_renderer = renderer_decorator_factory('fg_renderer')
bg_renderer = renderer_decorator_factory('bg_renderer')
