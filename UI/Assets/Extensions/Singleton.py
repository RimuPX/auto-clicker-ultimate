class Singleton:
    __instance = None
    hasInstance = False

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(Singleton, cls).__new__(cls)
        return cls.__instance

    def __init__(self, *args, **kwargs):
        print('f')
        if self.hasInstance: return
        self.hasInstance = True

    @classmethod
    def getInstance(cls):
        try:
            if not cls.__instance: raise AttributeError
            return cls.__instance
        except AttributeError:
            print("Object's instance does not exist!")
