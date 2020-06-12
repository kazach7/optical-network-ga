import time


def measure_time(method):
    def measure(*args, **kw):
        start_time = time.time()
        result = method(*args, **kw)
        end_time = time.time()

        time_in_ms = (end_time - start_time) * 1000

        print("{} spent {} ms to execute".format(method.__name__, time_in_ms))
        return result
    
    return measure