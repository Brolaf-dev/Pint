import os


def askForUsername():
    user = input("\nEnter the username: ")
    print('Username: ' + user)
    return user


def askForPassword():
    password = input("Enter the password: ")
    print('Password: ' + password)
    return password


def emergencyCall():
    numberEmergency = "0644626244"
    print('Initialize connect to: ' + numberEmergency)


def run():

    while 1:
        username = askForUsername()
        password = askForPassword()
        f = open("Baymax.txt", "r")

        for x in f:
            word = x.strip().split(',')

        if username == word[0] and password == word[1]:
            print("Login Successfully")
            emergencyCall()
            break
        print("No access is granted")



if __name__ in ('__main__','EmergencyCall'):
    run()