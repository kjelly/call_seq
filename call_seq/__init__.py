from .core import CallSeq


def trace(name, max_depth=None):
    def wrapper(func):
        def inner(*args, **kwargs):
            trail = CallSeq(max_depth=max_depth)
            trail.set_trace()
            ret = func(*args, **kwargs)
            trail.unset_trace()
            trail.dump_to_file(name)
            return ret
        return inner
    return wrapper
