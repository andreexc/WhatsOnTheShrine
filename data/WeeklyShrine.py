import requests
import json
import datetime

class WeeklyShrine:

    __URL = "https://api.nightlight.gg/v1/shrine?pretty=false"
    __PerkPageURL = "https://nightlight.gg/perks/"
    __enc = "utf-8"
    __cachePath = "permanent_data/cache.json"

    def __init__(self):
        super().__init__()
        self.__RequestStatusCode = 0
        self.__ShrineJSON = None
        return

    def __checkRequestSuccess(self):
        return True if self.__RequestStatusCode >= 200 and self.__RequestStatusCode < 300 else False

    def __createCache(self):
        # creates the file
        f = open(self.__cachePath, "w", encoding=self.__enc)
        f.close()
        return

    def __handleCacheError(self):
        self.__createCache()
        return
    
    def __handleMissingPermissionError(self):
        print("Missing permission to read my own cache.")
        return

    def __deserializeDate(self, date : str):
        date = date.replace('T', '-')
        date = date.replace(':', '-')
        date_list = date.split('-')
        return datetime.datetime(year=int(date_list[0]), month=int(date_list[1]), day=int(date_list[2]),
                                 hour=int(date_list[3]), minute=int(date_list[4]), second=int(date_list[5]))
    
    def __isExpired(self):
        try:
            f = open(self.__cachePath, "r", encoding=self.__enc)
            cache = json.loads(f.read())
            f.close()

            now = datetime.datetime(year=datetime.datetime.now().year, month=datetime.datetime.now().month, day=datetime.datetime.now().day,
                                 hour=datetime.datetime.now().hour, minute=datetime.datetime.now().minute, second=datetime.datetime.now().second)
            end_shrine_date = self.__deserializeDate(cache["data"]["end"])
            if (now >= end_shrine_date):
                return True
            else:
                return False
        except(FileNotFoundError, OSError, IOError):
            self.__handleCacheError()
        except(PermissionError):
            self.__handleMissingPermissionError()
        return

    def __checkOnCache(self):
        try:
            f = open(self.__cachePath, "r", encoding=self.__enc)
            content = f.read()
            f.close()
            if (content == ''):
                return False
            else:
                if self.__checkRequestSuccess() and not self.__isExpired():
                    return True
                else:
                    return False
        except(FileNotFoundError, OSError, IOError):
            self.__handleCacheError()
            self.__sendRequest()
        except(PermissionError):
            self.__handleMissingPermissionError()
            self.__sendRequest()
        return

    def __readFromCache(self):
        print("Reading from cache")
        try:
            f = open(self.__cachePath, "r", encoding=self.__enc)
            self.__ShrineJSON = json.loads(f.read())
            self.__RequestStatusCode = self.__ShrineJSON["status"]
            f.close()
        except(FileNotFoundError, OSError, IOError):
            self.__handleCacheError()
        except(PermissionError):
            self.__handleMissingPermissionError()
        return

    def __sendRequest(self):
        print("Making the get request")
        res = requests.get(self.__URL)
        self.__RequestStatusCode = res.status_code
        self.__ShrineJSON = res.json()
        self.__ShrineJSON["status"] = res.status_code

        try:
            f = open(self.__cachePath, "w", encoding=self.__enc)
            f.write(json.dumps(self.__ShrineJSON, indent=4))
            f.close()
        except(OSError, PermissionError, IOError):
            pass
            # don't save on the cache, let be the next request
            # to handle the cache
        return

    def __makeRequest(self):
        if (not self.__checkOnCache()):
            self.__sendRequest()
        else:
            self.__readFromCache()
        return

    def __sanitizeLink(self, name: str):
        string = self.__PerkPageURL + name
        output = ''
        for char in string:
            if (char == ' '):
                output += '_'
            else:
                output += char
        return output

    def __deserializeJSON(self):
        str_res : str = " --- WEEKLY SHRINE ---\n"
        for perk in self.__ShrineJSON["data"]["perks"]:
            str_res += f"\n Name: {perk["name"]}\n Character: {perk["character"]}\n Page: '{self.__sanitizeLink(perk["name"])}'\n"
        str_res += "\n ---------------------"
        return str_res

    def __str__(self):
        self.__makeRequest()  # FIX: makes the get request anyway even if it's in the cache
        if self.__checkRequestSuccess():
            print(self.__deserializeJSON())
        else:
            print(f"Error code {self.__RequestStatusCode}. Try again later.")
        return