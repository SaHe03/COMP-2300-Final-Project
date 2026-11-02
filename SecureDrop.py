import hmac
#import crypt
import yaml
from getpass import getpass

def register ():
    with open(id_path, 'w') as id:
        # common func starts here without writing to file
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
        # common func ends here


def login():
    id_path = 'user_id'
    with open(id_path, 'r') as id:
        id.readline()
        email = id.readline()
        id.readline()
        read_passwd = id.readline()
    pair = find_email(email)
    if (pair is None):
        print("Email and Password Combination invalid\n")
    else :
        passwd = pair.get('Password')
        if not (hmac.compare_digest(read_passwd, passwd)):
            print("Email and Password Combination invalid\n")
            # call function to be made and used in common with register to get
            # and read user inputs for new set of credentials

def find_email(find_email):
    found = False
    while not (found):
        with open("user_creds.yml", "r") as creds:
            data = yaml.full_load(creds)
        entry = data.get('Email')
        if (entry is None):
            return None
        if (hmac.compare_digest(find_email, entry)):
            found = True
            return data

#common function handle_input should take input and make sure no duplicate email
# in user_creds.yml

try:
    id_path = 'user_id'
    open(id_path, 'x')
except FileExistsError:
    login()

# logged_in_check will check a file (lets name it "user_creds" for now for a username
# if that username matches a username stored in JSON file and if it does, will salt
# and encrypt it to check
# against that username's encrypted passwd
