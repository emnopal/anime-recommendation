"""
Source code is from: https://stackoverflow.com/questions/1557571/how-do-i-get-time-of-a-python-programs-execution
"""

import time, sys

MEGABYTES = 10**6

def timeit(method):
    def timed(*args, **kwargs):
        ts = time.time()
        result = method(*args, **kwargs)
        te = time.time()
        size = sys.getsizeof(result)
        if 'log_time' in kwargs:
            name = kwargs.get('log_name', method.__name__.upper())
            kwargs['log_time'][name] = int((te - ts) * 1000)
            print('execute function: %r  %22f MB' % (method.__name__, size / MEGABYTES))
        else:
            print('execute function: %r  %22f ms' % (method.__name__, (te - ts) * 1000))
            print('execute function: %r  %22f MB' % (method.__name__, size / MEGABYTES))
        return result
    return timed