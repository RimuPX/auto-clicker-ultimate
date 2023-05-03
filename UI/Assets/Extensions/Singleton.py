class Singleton:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(Singleton, cls).__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        try:
            if not cls.__instance: raise AttributeError
            return cls.__instance
        except AttributeError:
            print("Object's instance does not exist!")
