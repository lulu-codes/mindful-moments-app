# main.py to Launch Mindful Moments App

# source .venv/bin/activate

# IMPORT BUILT IN LIBRARIES:
import sys
from pathlib import Path

# IMPORT THIRD-PARTY LIBRARIES:
# import rich

# IMPORT CUSTOM MODULES:
from utilities.auth import UserManager
from utilities.ascii_art import display_welcome_banner
from utilities.emojis import EMOJI_LOGIN, EMOJI_CREATE_USER, EMOJI_EXIT, EMOJI_ROCKET, EMOJI_INVALID, EMOJI_WARNING, EMOJI_SUCCESSFUL
from journal import run_journal

# Path to user accounts JSON file (used for loading/saving account data)
USER_ACCOUNTS_JSON_FILE = Path('data/user_accounts.json')

# Instance created from UserManager
user_manager = UserManager(USER_ACCOUNTS_JSON_FILE)

# WELCOME MAIN MENU OPTIONS: Dict with Numbered menu options = key, Menu description = value
MENU_LOGIN = "1"
MENU_CREATE_ACCOUNT = "2"
MENU_EXIT = "3"

# WELCOME MAIN MENU OPTIONS: Dict with Constant variables set above with numbers stored in constants for when getting user menu choice options
WELCOME_MENU = {
     MENU_LOGIN: f"{EMOJI_LOGIN} Login (Existing Users)",
     MENU_CREATE_ACCOUNT: f"{EMOJI_CREATE_USER} Create an Account (New Users)",
     MENU_EXIT: f"{EMOJI_EXIT} Exit App"
}

def display_menu(menu):
    for menu_number, menu_description in menu.items():
        print(f"{menu_number}. {menu_description}")

# APP ENTRY POINT (MAIN FUNCTION TO RUN APP)
def run_app():
    display_welcome_banner()
    print("Welcome to Mindful Moments - Your Personal Reflection Journaling App!")
    while True:
        menu_choice = get_menu_choice(WELCOME_MENU)
        if menu_choice == MENU_LOGIN:
            login()
        elif menu_choice == MENU_CREATE_ACCOUNT:
            create_new_account()
        elif menu_choice == MENU_EXIT:
            print("Exiting Mindful Moments App...")
            sys.exit()


# FUNCTION TO GET VALID MENU CHOICE & RETURN USER MENU CHOICE
def get_menu_choice(menu_options):
    display_menu(menu_options)
    while True:
        user_choice = input("Choose a menu option [1-3]: ").strip()
        try:
            if user_choice in menu_options.keys():
                return user_choice
            else:
                print(f"{EMOJI_INVALID} Invalid choice. Please try again.")
        except Exception as GetMenuErr:
            print(f"Error during get menu choice {GetMenuErr}")

def retry_prompt(prompt_message="Would you like to try again? (y/n): "):
    retry_input = input(prompt_message).strip().lower()
    return retry_input == 'y'
            
# FUNCTION FOR LOGIN, ONCE LOGIN SUCCESSFUL, LOADS INTO JOURNAL APP MENU:
def login():
    try:
        while True:
            username_input = input("Enter your username: ").strip().lower()
            current_user = user_manager.get_user_account(username_input)
            if not current_user:
                print(f"{EMOJI_INVALID} Invalid username. Please try again")
                # retry_login = input("Would you like to try again? (y/n): ").strip().lower()
                if not retry_prompt():
                    break
                continue    
            password_input = input("Enter your password: ").strip()
            login_authenticated = user_manager.authenticate_user(current_user, password_input)     # From UserManager Class (in utilities > auth.py file). Used to authenticate using user_manager instance 
            if login_authenticated:
                print(f"{EMOJI_SUCCESSFUL} Login Successful. Welcome back {current_user.username}!")
                run_journal(current_user.username)
                break
            else:
                print(f"{EMOJI_INVALID} Login Unsuccessful.")
                if not retry_prompt():
                    break
    except Exception as LoginErr:
        print(f"{EMOJI_WARNING} Error during Login: {LoginErr}")

# FUNCTION TO CREATE A NEW USER ACCOUNT
def create_new_account():
    try:
        while True:
            username = input("Enter your username: ").strip().lower()
            if user_manager.user_exists(username):
                print(f"{EMOJI_WARNING} Username is already taken. Please choose a different username.")
                if not retry_prompt():
                    break
                continue    
            else:
                # if username not in user_manager.accounts:
                print("Username is available.")
                break
        while True:
            password = input("Create a password: ").strip()
            confirm_password = input("Confirm your password: ").strip()
            if password == confirm_password:
                print("Passwords match and confirmed. Creating new account...")
                user_manager.create_user(username, password)
                print(f"{EMOJI_SUCCESSFUL} Your account has been created. You can now Login!")
                login()
                break
            elif password != confirm_password:
                print(f"{EMOJI_INVALID} Passwords do not match. Please try again.")
                if not retry_prompt():
                    break
            else:
                print(f"{EMOJI_WARNING} Something went wrong creating your account. Please try again.")
                if not retry_prompt():
                    break
    except Exception as NewAccountErr:
        print(f"Error during creating new account {NewAccountErr}")


# DISPLAY WELCOME BANNER AND RUN THE APP
if __name__ == "__main__":
    run_app()