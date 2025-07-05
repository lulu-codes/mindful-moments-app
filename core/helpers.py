# helpers.py
# REUSABLE HELPER FUNCTIONS USED IN main.py and journal.py

# IMPORT BUILT IN LIBRARIES:
import getpass

# IMPORT THIRD-PARTY LIBRARIES:
from rich import print
from rich.console import Console

# IMPORT CUSTOM CORE MODULES:
from ui.emojis import EMOJI_MENU, EMOJI_INVALID, EMOJI_WARNING, EMOJI_RETRY

# For rich console printing
console = Console()

# MENU HELPERS
def display_menu(menu_options):
    """ To format and display menu options (key=menu number) using rich text styling"""
    console.print("=" * 60)
    console.print(f"\n[bold cyan]{EMOJI_MENU} MENU OPTIONS:[/bold cyan]\n")
    console.print("=" * 60)
    for key, value in menu_options.items():
        if isinstance(value, tuple):
            emoji, label = value
            console.print(f"[bold]{key}. {emoji} {label}[/bold]")
        else:
            console.print(f"[bold]{key}. {value}[/bold]")
        print()


def get_menu_choice(menu_options):
    """ Get valid menu choice from user """
    while True:
        try:
            user_choice = input("Choose a menu option. Enter a number: ").strip()
            if user_choice in menu_options.keys():
                return user_choice
            else:
                console.print(f"[red]{EMOJI_INVALID} You have entered an Invalid option. Please try again.[/red]\n")
        except Exception as err:
            console.print(f"\n[red]{EMOJI_WARNING} Unexpected error occurred, please try again.[/red]\n")


# RETRY PROMPT HELPER
def retry_prompt(prompt_message=f"{EMOJI_RETRY} Would you like to try again? [y/n]: "):
    """ Prompts user option to retry, True to try again, otherwise False """
    while True:
        retry_input = input(prompt_message).strip().lower()
        if retry_input == 'y':
            return True
        elif retry_input == 'n':
            return False
        else:
            console.print(f"[red]{EMOJI_WARNING} Invalid input. Please enter [y/n][/red]")


# VALIDATE INPUT HELPER
""" Helper function to validate input against validation criteria """
def get_valid_input(
        prompt: str,
        field_name: str ="Input",
        allow_spaces: bool = True,      # set True as default to allow spaces for journal entries only
        min_length: int = 5,
        max_length: int = 200,
        hide_input: bool = False
    ):
    """ Prompts user for valid input until it meets validated input criteria """
    while True:
        try:
            """ hide_input=True uses getpass to hide input characters (used only for password input)"""
            if hide_input:
                user_input = getpass.getpass(prompt).strip()
            else:
                user_input = input(prompt).strip()
            if user_input == "":
                console.print(f"[red]{EMOJI_INVALID} {field_name} can not be blank. Please try again![/red]\n")
                continue
            elif not allow_spaces and " " in user_input:
                console.print(f"[red]{EMOJI_INVALID} {field_name} cannot contain spaces. Please try again![/red]\n")
                continue
            elif len(user_input) < min_length or len(user_input) > max_length:
                console.print(f"[red]{EMOJI_INVALID} {field_name} Input must be between {min_length}-{max_length} characters. Please try again![/red\n]")
                continue
            return user_input
        except Exception as err:
            console.print(f"[red]{EMOJI_WARNING} Unexpected error occurred: {err}. Please try again.[/red]\n")