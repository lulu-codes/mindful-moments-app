# helpers.py

from utilities.emojis import *

# REUSABLE HELPER FUNCTIONS USED IN main.py and journal.py

def display_menu(menu_options):
    """ To format and display menu options (key=menu number) """
    print(f"\n{EMOJI_MENU} MENU OPTIONS:")
    print("=" * 60)
    for key, value in menu_options.items():
        if isinstance(value, tuple):
            emoji, label = value
            print(f"{key}. {emoji} {label}")
        else:
            print(f"{key}. {value}")
    print()


def get_menu_choice(menu_options):
    """ Get valid menu choice from user """
    while True:
        user_choice = input("Choose a menu option. Enter a number: ").strip()
        if user_choice in menu_options.keys():
            return user_choice
        else:
            print(f"{EMOJI_INVALID} You have entered an Invalid option. Please try again.")


def retry_prompt(prompt_message=f"{EMOJI_RETRY} Would you like to try again? [y/n]: "):
    """ Prompts user option to retry, True to try again, otherwise False """
    while True:
        retry_input = input(prompt_message).strip().lower()
        if retry_input == 'y':
            return True
        elif retry_input == 'n':
            return False
        else:
            print(f"{EMOJI_WARNING} Invalid input. Please enter 'y' OR 'n'")


def get_valid_input(
        prompt: str,
        field_name: str ="Input",
        allow_blank: bool = False,
        allow_spaces: bool = True,
        min_length: int = 5,
        max_length: int = 200
    ):
    """ Prompts user for valid input until it meets validated input criteria """
    while True:
        user_input = input(prompt).strip()
        if not allow_blank and user_input == "":
            print(f"{EMOJI_INVALID} {field_name} can not be blank. Please try again!")
        elif not allow_spaces and " " in user_input:
            print(f"{EMOJI_INVALID} {field_name} cannot contain spaces. Please try again!")
        elif len(user_input) < min_length or len(user_input) > max_length:
            print(f"{EMOJI_INVALID} {field_name} Input must be between {min_length}-{max_length} characters. Please try again!")
        else:
            return user_input