class Singleton:
    #comes from geeks for geeks
    # Here will be the instance stored.
    #this is the singleton pattern and makes sure one instance of the pipe is made
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if Singleton.__instance == None:
            Singleton()
        return Singleton.__instance 

    def __init__(self):
        """ Virtually private constructor. """
        if Singleton.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Singleton.__instance = self