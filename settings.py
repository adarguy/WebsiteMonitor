import sys
import os

parentPath = os.path.abspath("src")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
import breach as B

class Settings:
    url = ""
    push = "True"
    timer = 600
    email = "robertpower420@gmail.com"
    password = "*******"
    number = "4377715619@sms.rogers.com"


def proceed():
    while True:
        p = input("How do you want to proceed?\n"+
        "Proceed Options:\n"+
        "  -m : Proceed to monitoring screen\n"+
        "  -s : Go back to 'Settings Options'\n"+
        "  -e : Exit Program\n"+
        ">>>> ")

        if p != "m" and p != "s" and p != "e":
            print("Error: Please enter s or e")
        else:
            break
    return p


def add():
    print_settings()
    while True:
        url = input("Paste the URL you want to check for updates \n>>>> ")
        if 'http://' not in url and 'https://' not in url or "," in url:
            print("Error: Please provide valid url (no comma's)")
        else:
            break

    while True:
        get_notification = input("\nDo you want to get a notification to your phone when the website has been changed? (y/n) \n>>>> ")
        if get_notification != "y" and get_notification != "n":
            print("Error: Please enter y or n")
        else:
            if get_notification == "y":
                push = True
                print("Notifications to your phone have been turned ON\n")
                break
            else:
                push = False
                print("Notifications to your phone have been turned OFF\n")
                break
    
    with open("src\\settings.txt", "a", encoding="utf-8") as f:
        f.write(url+","+str(push)+"\n")

    print_settings()


def remove():
    while True:
        l = print_settings()
        r = input("Which number do you want to remove from the website list? \n>>>> ")
        try:
            i = ""
            r = int(r)
            if (r < 1) or (r-2 > len(l)):
                raise Exception
            while True:
                i = input("\nAre you sure you want to remove "+l[r].split(",")[0]+"? (y/n) \n>>>> ")
                if i != "y" and i != "n":
                    print("Error: Please enter y or n")
                else:
                    if i == "y":
                        del l[r]
                        break
                    elif i == "n":
                        raise Exception
            break
        except:
            if i != "n":
            	print("\nError: Please enter a valid number from the list above")
    
    with open("src\\settings.txt", "w") as f:
        for line in l:
            f.write(line)
        f.close()

    print_settings()


def change_timer():
    while True:
        check_interval = input("How often do you want to check your websites for updates? Enter it in seconds (min. 20) \n>>>> ")
        if check_interval.isdigit():
            check_interval = int(check_interval)
            if check_interval > 19:
                print("The website will be checked for updates every " + str(check_interval) + " seconds\n")
                Settings.timer = check_interval
                l = print_settings(0)
                del l[0]
                l.insert(0,"Timer="+str(check_interval)+"\n")
                with open("src\\settings.txt", "w") as f: 
                    for i in range(0,len(l)):
                        f.write(l[i])
                    f.close()
                break
            else:
                print("Make sure to enter a value bigger than 19\n")
        else:
            print("Please enter an integer (which has to be bigger than 19)\n")


def print_settings(p=1):
    f = open("src\\settings.txt", "r")
    l = [line for line in f.readlines()]

    if (p == 1):
        print("\n\n+---------------------------------------------------------------------+\n")
        if (len(l) > 1):
            print("Current Websites Being Monitored\n")
            print('{0:2} || {1:5} || {2:5}'.format("#", "SMS", "URL"))
            print("==========================")
            for i in range(1,len(l)):
                p = l[i].split(",")
                if p[1][-1] == "\n":
                    p[1] = p[1][:-1]
                print('{0:2} || {1:5} || {2:5}'.format(str(i),p[1], p[0]))
        else:
            print("There are currently no websistes being monitored")
        print("\n+--------------------------------------------------------------------+\n\n")
    return l


def main():
    print("\n\nSup breach?")
    x = 's'
    while x == 's':
        options = input("What do you want to do?\n"+
        "\n\n+---------------------------------------------------------------------+\n"+    
        "Program Options:\n"+
        "  -add     : Add a url to the list of monitored websites\n"+
        "  -remove  : Remove a url from the list of monitored websites\n"+
        "  -show    : Show all current websites being monitored\n"+
        "  -timer   : Edit the monitor rate\n"+
        "  -monitor : Go to the monitoring page\n"+
        "  -exit    : Exit program"
        "\n+---------------------------------------------------------------------+\n\n"+
        ">>>> ")
        if options == "add":
            add()
        elif options == "remove":
            remove()
        elif options == "show":
            print_settings()
        elif options == "timer":
            change_timer()
        elif options == "monitor":
            os.chdir("src")
            B.main(1)
        elif options.strip() == "":
            break
        elif options == "exit":
            print("\nPeace Bro!")
            sys.exit()
        else:
            print("Please select an option from the menu or hit ENTER to go straight to monitoring")
            continue

        x = proceed()           
        if x == "e":
            print("\nPeace Bro!")
            break
        elif x == "m":
            os.chdir("src")
            B.main(1)

if __name__ == "__main__":
    main()