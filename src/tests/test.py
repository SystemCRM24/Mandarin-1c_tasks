import traceback

def some_func():
    raise ValueError('UUUUU SUCA')


try:
    a = some_func()
except Exception as e:
    print(e)
    print(traceback.format_exc())
