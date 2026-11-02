import hmac
#import crypt
import yaml
from getpass import getpass

def register ():
    try:
        id_path = 'user_id'
        open(id_path, 'x')
        with open(id_path, 'w') as id:
            name = input("Enter Full Name: ")
            id.write(name + "\n")
            email = input("Enter Email Address: ")
            id.write(email + "\n")
            password = getpass("Enter Password: ")
            passcheck = getpass("Re-enter Password: ")
            if not (hmac.compare_digest(password, passcheck)):
                while not (hmac.compare_digest(password, passcheck)):
                    print("Passwords didn't match. Please try again.")
                    password = getpass("Enter Password: ")
                    passcheck = getpass("Re-enter Password: ")
            id.write(password)
    except FileExistsError:
        login()



def login():
    with open(id_path, 'r') as id:
        id.readline()
        email = id.readline()
    found = false
    while not (found):
        with open("user_creds.yml", "r") as creds:
            data = yaml.safe_load(creds)
        entry = data.get('Email')
        found = hmac.compare_digest(email, entry)
    if (found):
        hmac.compare_digest(email, data.get('Password'))

register()

# logged_in_check will check a file (lets name it "user_creds" for now for a username
# if that username matches a username stored in JSON file and if it does, will salt
# and encrypt it to check
# against that username's encrypted passwd
