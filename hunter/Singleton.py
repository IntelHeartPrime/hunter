def singleton(cls, *args, **kw):
106.    instances = {}
107.    def _singleton():
108.        if cls not in instances:
109.            instances[cls] = cls(*args, **kw)
110.        return instances[cls]
111.    return _singleton
112.
113.@singleton
114.class MyClass4(object):
115.    a = 1
116.    def __init__(self, x=0):
117.        self.x = x




