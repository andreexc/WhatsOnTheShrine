import json as js

class SettingParser():
    
    __encoding = "utf-8"
    __settings : dict = None

    def __init__(self, path):
        self.__path = path
        return
    
    def parseSettings(self):
        try:
            f = open(self.__path, "r", encoding=self.__encoding)
            self.__settings = js.loads(f.read())
            f.close()
        except(IOError):
            print("Error while opening the settings.")
        return
    
    def getSettings(self, key):
        return self.__settings[key]
    
    def setSettings(self, key, value):
        self.__settings[key] = value

        f = open(self.__path, "w", encoding=self.__encoding)
        f.write(js.dumps(self.__settings, indent=4))
        f.close()