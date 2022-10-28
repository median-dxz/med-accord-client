class MemberController:
    _instance = None
    name = None
    avatar = None

    def __init__(self):
        pass

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kw)
        return cls._instance