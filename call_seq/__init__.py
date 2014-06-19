from .core import CallSeq


def trace(name):
    def wrapper(func):
        def inner(*args, **kwargs):
            trail = CallSeq()
            trail.set_trace()
            ret = func(*args, **kwargs)
            trail.unset_trace()
            trail.dump_to_file(name)
            return ret
        return inner
    return wrapper
