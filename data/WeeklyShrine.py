import requests
from data.RequestException import RequestException as ReqEx
import json

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
        return True if self.__RequestStatusCode >= 200 and self.__RequestStatusCode < 299 else False

    def __checkOnCache(self):
        try:
            f = open(self.__cachePath, "r", encoding=self.__enc)
            content = f.read()
            f.close()
            if (content == ''):
                return False
            else:
                return True
        except(IOError):
            print("Error while reading the cache.")
            return

    def __makeRequest(self):

        if (not self.__checkOnCache()):
            print("Making the get request")
            res = requests.get(self.__URL)
            self.__RequestStatusCode = res.status_code
            self.__ShrineJSON = res.json()
            self.__ShrineJSON["status"] = res.status_code

            f = open(self.__cachePath, "w", encoding=self.__enc)
            f.write(json.dumps(self.__ShrineJSON, indent=4))
            f.close()
        else:
            print("Reading from cache")
            f = open(self.__cachePath, "r", encoding=self.__enc)

            # need to check if shrine is expired !!!
            # we can use the key end in the json

            self.__ShrineJSON = json.loads(f.read())
            self.__RequestStatusCode = self.__ShrineJSON["status"]
            f.close()
        
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

        if not self.__checkRequestSuccess():
            self.__makeRequest()
        
        if self.__checkRequestSuccess():
            print(self.__deserializeJSON())
        else:
            print(f"Error code {self.__RequestStatusCode}. Try again later.")
        return