def try_catch(func, *args, **kwargs):
    try:
        return func(*args, **kwargs), None
    except Exception as err:
        return None, err