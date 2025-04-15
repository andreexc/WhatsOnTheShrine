from data.WeeklyShrine import WeeklyShrine
from data.SettingParser import SettingParser

if (__name__ == "__main__"):

    settings = SettingParser("permanent_data/settings.json")
    settings.parseSettings()

    print("Welcome to my shrine bot.")
    if settings.getSettings("remember_intro"):
        print("Please read the README file and don't forget to check me on GitHub!")
        inp = input("Write 'N' to if you wish to delete this message. ")
        if (inp == 'N'):
            settings.setSettings("remember_intro", 0)

    shrine = WeeklyShrine()
    inp : chr = ' '

    while (inp != 'E'):
        print("\nCHOOSE YOUR ACTION:")
        print("G - Get the latest shrine\nI - Info about the developer\nE - Exit the bot")
        inp = input("Choice: ")
        print()

        if (inp == 'G'):
            shrine.__str__()
        elif (inp == 'I'):
            print("Check me on GitHub at the following link!\nhttps://github.com/andreexc")
        elif (inp == 'E'):
            print("See you in the foo next week ;)")
            del shrine
            del settings
        else:
            pass