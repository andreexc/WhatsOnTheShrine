import requests
from data.RequestException import RequestException as ReqEx

class WeeklyShrine:

    __URL = "https://api.nightlight.gg/v1/shrine?pretty=false"
    __PerkPageURL = "https://nightlight.gg/perks/"

    def __init__(self):
        super().__init__()
        self.__RequestStatusCode = 0
        self.__ShrineJSON = None
        return

    def __checkRequestSuccess(self):
        return True if self.__RequestStatusCode >= 200 and self.__RequestStatusCode < 299 else False

    def __makeRequest(self):
        res = requests.get(self.__URL)
        self.__RequestStatusCode = res.status_code
        self.__ShrineJSON = res.json()
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