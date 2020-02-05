import copy
import types
import functools


def copy_func(f, globals=None, module=None):
    """
    Copies a function with supplied globals
    Based on http://stackoverflow.com/a/6528148/190597 (Glenn Maynard)
    Based on https://stackoverflow.com/a/49077211/8070948
    """
    if globals is None:
        globals = f.__globals__
    # print('globals in function', f.__globals__)
    print('__code__', f.__code__)
    g = types.FunctionType(
        f.__code__,
        globals,
        name=f.__name__,
        argdefs=f.__defaults__,
        closure=f.__closure__)
    g = functools.update_wrapper(g, f)
    if module is not None:
        g.__module__ = module
    g.__kwdefaults__ = copy.copy(f.__kwdefaults__)
    return g
