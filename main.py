# main.py
# source .venv/bin/activate

# IMPORT BUILT IN LIBRARIES:
import sys
from pathlib import Path

# IMPORT THIRD-PARTY LIBRARIES:
import rich

# IMPORT CUSTOM MODULES:
from utilities.user_auth_models import UserManager
from utilities.journal_models import JournalEntry
from utilities.helpers import display_menu, get_menu_choice, retry_prompt, get_valid_input
from utilities.ascii_art import display_welcome_banner
from utilities.emojis import *
from journal import run_journal

# Custom classes exceptions (off base Exception)
class UserAuthError(Exception):
    """ Raised when there is an issue with user authentication """
    pass

class AccountCreationCancelled(Exception):
    """ Raised when user cancels account creation """
    pass

# CONSTANT FILE PATH TO USER ACCOUNTS DATA
USER_ACCOUNTS_JSON_FILE = Path('data/user_accounts.json')

# INSTANCE OF UserManager: Used to handle user login authentication and registration of new user accounts
user_manager = UserManager(USER_ACCOUNTS_JSON_FILE)

# MAIN MENU OPTIONS (Dict based menu)
WELCOME_MENU = {
        "1": f"{EMOJI_LOGIN} Login (Existing Users)",
        "2": f"{EMOJI_CREATE_USER} Create an Account (New Users)",
        "3": f"{EMOJI_EXIT} Exit App"
}

# CORE LOGIC FUNCTIONS

def login():
    """ Handles Login flow to validate username and password, then runs journal once authenticated successfully """
    print(f"Login with your account details to get started!\n")
    try:
        while True:
            username_input = input("Enter your username: ").strip().lower()
            current_user = user_manager.get_user_account(username_input)
            if not current_user:
                print(f"{EMOJI_INVALID} Invalid username. Please try again\n")
                if not retry_prompt():
                    break
                continue    
            password_input = input("Enter your password: ").strip()
            login_authenticated = user_manager.authenticate_user(current_user, password_input)
            if login_authenticated:
                print(f"\n{EMOJI_AUTHENTICATED} Login Successful. Welcome back {current_user}!\n")
                run_journal(current_user)
                break
            else:
                print(f"{EMOJI_INVALID} Login Unsuccessful\n")
                if not retry_prompt():
                    break
    except Exception as err:
        print(f"{EMOJI_WARNING} Unexpected Error during Login: {err}\n")

def prompt_username():
    """ Prompt for a valid username that is available, allows user to retry """
    while True:
        print()
        username = get_valid_input(prompt="Choose a Username: ", field_name="Username", allow_blank=False, allow_spaces=False, min_length= 5, max_length=20).lower()
        if user_manager.user_exists(username):
            print(f"{EMOJI_WARNING} Sorry! That Username is already taken. Please choose a different username\n")
            if not retry_prompt():
                return None     # User prompted to retry, opts to quit
        else:
            print(f"{EMOJI_SUCCESSFUL} Yay! Username is available!\n")
            return username
        
def prompt_password():
    """ Prompt for a valid password and password confirmation, for mismatch entries, allows user to retry """
    while True:
        password = get_valid_input(prompt="Choose a password: ", field_name="Password", allow_blank=False, allow_spaces=False, min_length= 8, max_length=16)
        confirm_password = input("Confirm your password: ").strip()
        if password == confirm_password:
            print(f"{EMOJI_SUCCESSFUL} Passwords match and confirmed\n")
            return password
        else:
            print(f"{EMOJI_INVALID} Passwords do not match\n")
            if not retry_prompt():
                return None

def create_new_account():
    """ Handles creating new account flow to get validated username and password to register new account on completion or exits function early """
    print(f"Let's get you setup with a new account to get started!\n")
    try:
        username = prompt_username()
        if not username:
            print(f"{EMOJI_WARNING} Account creation cancelled during username request\n")
            return None
        password = prompt_password()
        if not password:
            print(f"{EMOJI_WARNING} Account creation cancelled during password request\n")
            return None
        registration_successful = user_manager.register_user(username, password)
        if registration_successful:
            print(f"{EMOJI_SAVE} Your account has now been created. {EMOJI_LOGIN} You can now Login from the main menu!\n")
        else:
            print(f"{EMOJI_WARNING} Sorry! There was a problem registering your account. Please try again\n")
            if retry_prompt():
                create_new_account()
    except Exception as err:
        print(f"{EMOJI_WARNING} There was an Error during creating your new account: {err}\n")


# APP ENTRY POINT & MAIN FUNCTION TO START APP
def main():
    """  Displays banner and menu, handles user's menu choice then calls respective menu function """
    display_welcome_banner()
    print(f"Welcome to Mindful Moments - Your Personal Reflection Journaling App! {EMOJI_REFLECTION}\n")
    while True:
        display_menu(WELCOME_MENU)
        menu_choice = get_menu_choice(WELCOME_MENU)
        if menu_choice == "1":
            print(f"You have chosen to Login\n")
            login()
        elif menu_choice == "2":
            print(f"You have chosen to Create a New User Account\n")
            create_new_account()
        elif menu_choice == "3":
            print(f"{EMOJI_WAVE} Exiting App...\n")
            sys.exit(0)


# RUN THE PROGRAM
if __name__ == "__main__":
    main()