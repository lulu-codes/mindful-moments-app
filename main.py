# main.py
# To activate VENV note (to remove later) source .venv/bin/activate

# IMPORT BUILT IN LIBRARIES:
import sys
import getpass

# IMPORT THIRD-PARTY LIBRARIES:
from rich import print
from rich.console import Console

# IMPORT CUSTOM MODULES:
from core.user_auth_models import UserManager
from core.helpers import display_menu, get_menu_choice, retry_prompt, get_valid_input
from ui.styling import display_welcome_banner
from ui.emojis import (
    EMOJI_LOGIN,
    EMOJI_CREATE_USER,
    EMOJI_EXIT,
    EMOJI_INVALID,
    EMOJI_WARNING,
    EMOJI_AUTHENTICATED,
    EMOJI_SUCCESSFUL,
    EMOJI_REFLECTION,
    EMOJI_WAVE
)

from journal import run_journal

# IMPORT CONSTANT FILE PATHS
from core.file_paths import USER_ACCOUNTS_JSON_FILE

# IMPORT CUSTOM EXCEPTION CLASSES:
from core.exception_classes import (
    UserNotFoundError,
    ErrorGettingUserAccount,
    AccountRegistrationError,
    AuthenticationError,
    )

# For rich console printing
console = Console()

# MAIN MENU OPTIONS (Dict mapping user menu choice accessed by keys)
WELCOME_MENU = {
        "1": f"{EMOJI_LOGIN} Login (Existing Users)",
        "2": f"{EMOJI_CREATE_USER} Create an Account (New Users)",
        "3": f"{EMOJI_EXIT} Exit App"
}

# INSTANCE OF UserManager: Used to handle user login authentication and registration of new user accounts
user_manager = UserManager(USER_ACCOUNTS_JSON_FILE)


# APP ENTRY POINT & MAIN FUNCTION TO START APP
def main():
    """Displays banner and menu, handles user's menu choice then calls respective menu function."""
    display_welcome_banner()
    console.print(f"\nWelcome to Mindful Moments - Your Personal Reflection Journaling App! {EMOJI_REFLECTION}\n")
    while True:
        display_menu(WELCOME_MENU)
        menu_choice = get_menu_choice(WELCOME_MENU)
        try:
            if menu_choice == "1":
                console.print(f"\n You have chosen to Login\n")
                current_user = login()
                if current_user:
                    run_journal(current_user)   # Pass logged in current user to uesr's journal
            elif menu_choice == "2":
                console.print(f"\n You have chosen to Create a New User Account\n")
                create_new_account()
            elif menu_choice == "3":
                console.print(f"\n {EMOJI_WAVE} Exiting App...\n")
                sys.exit(0)
        except Exception as err:
            console.print(f"[red]{EMOJI_WARNING} Unexpected error: {err}[/red]")


# CORE LOGIC FUNCTIONS

def login():
    """Handles Login flow to authenticate user's login credentials."""
    console.print(f"Login with your account details to get started!\n")
    while True:
        username_input = get_valid_input("Enter your username: ").strip().lower()
        try:
            user_account = user_manager.get_user_account(username_input)   # Gets and returns user account object, if exists
        except UserNotFoundError as err:
            console.print(f"[red]{EMOJI_WARNING} User not found. Please try again.[/red]")
            if not retry_prompt():
                return None         # Returns back to main menu
            continue                # Retry loop for username
        except ErrorGettingUserAccount as err:
            console.print(f"[red]{EMOJI_WARNING} Oops! There was a problem retrieving your account data.[/red]")
            if not retry_prompt():
                return None
            continue
        except Exception as err:
            console.print(f"[red]{EMOJI_WARNING} Unexpected error: {err}[/red]")
            return None


        while True:
            password_input = getpass.getpass("Enter your password: ").strip()
            try:
                authenticated_user = user_manager.authenticate_user(user_account, password_input)
                if authenticated_user:
                    console.print(f"[green]{EMOJI_SUCCESSFUL} Login Successful.[/green]\n")
                    console.print(f"\n{EMOJI_AUTHENTICATED} Welcome back {authenticated_user}!\n")
                    return authenticated_user    # Returns to parse through to run journal for current user
            except AuthenticationError:
                    console.print(f"[red]{EMOJI_INVALID} Login Unsuccessful. Incorrect password.[/red]\n")
                    if not retry_prompt():
                        return None
                    continue
    

def create_new_account():
    """Handles creating new account flow to get validated username and password.
       Registers a new account on completion, otherwise exits to main if user cancels or error.
    """
    console.print(f"Let's get you setup with a new account to get started!\n")
    while True:
        username = get_valid_username()
        if username is None:
            return      # User chose to cancel during username, return back to main menu
        password = get_valid_password()
        if password is None:
            return      # User chose to cancel during password, return back to main menu
        try:
            if user_manager.register_user(username, password):
                console.print(f"[green]{EMOJI_SUCCESSFUL} Your user account is successfully created.\n{EMOJI_LOGIN} You can now Login from the main menu![/green]\n")
                return None
            else:
                console.print(f"[red]{EMOJI_WARNING} There was a problem registering your account. Please try again.[/red]\n")
                if not retry_prompt():
                    return None
        except AccountRegistrationError:
            console.print(f"[red]{EMOJI_WARNING} Error occurred while creating new user account. Please try again.[/red]\n")
            if not retry_prompt():
                return None
            continue

def get_valid_username():
    """Prompt for a valid username that is available, allows user to retry. Returns valid username choice or None if cancelled """
    while True:
        print()
        username = get_valid_input(
            prompt="Choose a Username: ",
            field_name="Username",
            allow_spaces=False,
            min_length= 5,
            max_length=20
        ).lower()
        if user_manager.is_existing_user(username):     # Checks if username exists using user manager methods
            console.print(f"[red]{EMOJI_WARNING} Sorry! That Username is already taken. Please choose a different username.[/red]\n")
            if not retry_prompt():
                return None
        else:
            console.print(f"[green]{EMOJI_SUCCESSFUL} Yay! Username is available![/green]\n")
            return username
        
def get_valid_password():
    """Prompt for a valid password and confirmation. Returns password if matches, otherwise None if cancelled retry."""
    while True:
        password = get_valid_input(
            prompt="Choose a password: ",
            field_name="Password",
            allow_spaces=False,
            min_length= 8,
            max_length=16,
            hide_input=True
        )
        confirm_password = getpass.getpass("Confirm your password: ").strip()
        if password == confirm_password:
            console.print(f"[green]{EMOJI_SUCCESSFUL} Passwords match and confirmed.[/green]\n")
            return password
        else:
            console.print(f"[red]{EMOJI_INVALID} Passwords do not match.[/red]\n")
            if not retry_prompt():
                return None
            
            
# RUN THE PROGRAM
if __name__ == "__main__":
    main()