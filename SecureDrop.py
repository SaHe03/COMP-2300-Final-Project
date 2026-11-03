# this verion handles without security, basic registration and login, under a single users credential file
# login doesn't write over any file, it will redirect to registration
# login checks if the email in user id is in user creds at all, using user entered email
# added a help, added "add" to add a contact under the user id
import hmac
import os
import yaml
from getpass import getpass

def register (cred_path):
    print("No users are registered with this client.")
    enter = input("Do you want to register a new user (y/n)? ")
    if enter.lower() == 'n':
        exit("Exiting SecureDrop.")
    elif enter.lower() == 'y':
        name = input("Enter Full Name: ")
        #need to ensure unique email, with user cred file, a loop
        email = input("Enter Email Address: ")
        try:
            with open(cred_path, "r") as creds:
                users = yaml.safe_load(creds) or {}
        except Exception as e:
            users = {}
        emailList = [users.get('Email') for users in users.values() if isinstance(users, dict)]
        while email in emailList:
            print("Email already exists. Please try again.")
            email = input("Enter Email Address: ")

        password = getpass("Enter Password: ")
        passcheck = getpass("Re-enter Password: ")
        while not (hmac.compare_digest(password, passcheck)):
                print("Passwords didn't match. Please try again.")
                password = getpass("Enter Password: ")
                passcheck = getpass("Re-enter Password: ")
        idList = []
        idList = [int(userID) for userID in users.keys() if str(userID).isdigit()]
        latestID = max(idList, default=0)
        newID = latestID + 1
        userData:dict = {
            "User_ID": newID,
            "Full_Name": name,
            "Email": email,
            "Password": password,
        }
        users[newID] = userData
        with open(cred_path, "w") as creds:
            yaml.safe_dump(users, creds, sort_keys=True)

        print("Passwords Match.\nUser Registered.\n")
        exit("Exiting SecureDrop.")


def login(cred_path):
    #need to know that a user on id is already in user creds
    #defaultFound is for automatically finding if userid email is in user cred at all
    enteredEmail = input("Enter Email Address: ")
    with open(cred_path, "r") as creds:
        users = yaml.safe_load(creds) or {}
    matchingUsers = [user
        for user in users.values()
        if isinstance(user, dict) and user.get("Email") == enteredEmail
    ]
    if not matchingUsers:
        print("Email not registered.")
        exit("Exiting SecureDrop.")
    data = matchingUsers[0]
    enteredPassword = getpass("Enter Password: ")
    if not hmac.compare_digest(enteredPassword,data.get("Password", "")):
        print("Email and Password Combination Invalid.")
        login(cred_path)
    else:
        print("Welcome to SecureDrop.\nType \"help\" For Commands.")
        return data.get("User_ID")
    
def help(cred_path, idNumber):
    print("\"add\"  -> Add a new contact" \
    "\n\"list\" -> List all online contacts" \
    "\n\"send\" -> Transfer file to contact\
        \n\"exit\" -> Exit SecureDrop")

def scanningInput(cred_path, idNumber):
    currentInput = input("")
    if currentInput == "add":
        add(cred_path, idNumber)
    elif currentInput == "list":
        list(cred_path, idNumber)
    elif currentInput == "send":
        send(cred_path, idNumber)
    elif currentInput == "help":
        help(cred_path, idNumber)
    elif currentInput == "exit":
        exit("Exiting SecureDrop")

def add(cred_path, idNumber):
    contact_name = input("Enter Full Name: ")
    contact_email = input("Enter Email Address: ")
    contact: dict = {
        "Full_Name": contact_name,
        "Email": contact_email,
    }
    with open(cred_path, "r") as creds:
        users = yaml.safe_load(creds) or {}
    users[idNumber].setdefault("Contacts",{})
    users[idNumber]["Contacts"][contact_email] = contact
    with open(cred_path, "w") as creds:
        yaml.safe_dump(users, creds, sort_keys=False)
    print("Contact Added")
    return

def list(cred_path, idNumber):
    print("The following contacts are online:\n")
    #code to list all online contacts
    return

def send(cred_path, idNumber):
    print("Sending file to contact")
    #code to send a file to a contact
    return
def main():
    cred_path = 'user_creds.yml'
    if not os.path.exists(cred_path):
            register(cred_path)
    else:
        idNumber = login(cred_path)
        while True:
            scanningInput(cred_path, idNumber)

main()


#Will have a seperate security function to do the salt and hashing


