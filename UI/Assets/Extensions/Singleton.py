class Singleton:
    __instance = None
    hasInstance = False

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(Singleton, cls).__new__(cls)
            print('new: ', cls.__instance)
        return cls.__instance

    def __init__(self, *args, **kwargs):
        if Singleton.hasInstance: return
        Singleton.hasInstance = True

    @classmethod
    def getInstance(cls):
        print('get: ', cls.__instance)
        try:
            if not cls.__instance: raise AttributeError
            return cls.__instance
        except AttributeError:
            print("Object's instance does not exist!")