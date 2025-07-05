# journal.py
# FOR CREATING & VIEWING JOURNAL ENTRIES LOGIC AND FLOW

# IMPORT BUILT IN LIBRARIES:
import random

# IMPORT THIRD-PARTY LIBRARIES:
from rich.console import Console

# IMPORT CUSTOM CORE MODULES:
from core.journal_models import JournalManager, JournalEntry
from core.user_auth_models import UserManager
from core.helpers import display_menu, get_menu_choice, get_valid_input
from core.quotes import encouragement_quotes
from ui.styling import display_journal_banner
from ui.emojis import (
    EMOJI_CREATE_ENTRY,
    EMOJI_VIEW_ENTRIES,
    EMOJI_LOGOUT,
    EMOJI_MOOD_AWFUL,
    EMOJI_MOOD_SAD,
    EMOJI_MOOD_OKAY,
    EMOJI_MOOD_GOOD,
    EMOJI_MOOD_GREAT,
    EMOJI_WRITE,
    EMOJI_WAVE,
    EMOJI_HOURGLASS,
    EMOJI_SUCCESSFUL,
    EMOJI_WARNING,
    EMOJI_ENCOURAGEMENT,
    EMOJI_SAVE
    )


# IMPORT CONSTANT FILE PATHS
from core.file_paths import JOURNAL_ENTRIES_JSON_FILE, USER_ACCOUNTS_JSON_FILE

# IMPORT CUSTOM EXCEPTION CLASSES
from core.exception_classes import JournalCreationError


# For rich console printing
console = Console()

# JOURNAL MENU OPTIONS (Dict based menu)
JOURNAL_MENU = {
    "1": f"{EMOJI_CREATE_ENTRY} Create a Journal Entry",
    "2": f"{EMOJI_VIEW_ENTRIES} View Past Journal Entries",
    "3": f"{EMOJI_LOGOUT} Logout"
}

# MOOD RATINGS
"""For simple input prompt, dict key holds tuple of emoji + label."""
MOOD_RATINGS = {
    "1": (EMOJI_MOOD_AWFUL, "Awful"),
    "2": (EMOJI_MOOD_SAD, "Sad"),
    "3": (EMOJI_MOOD_OKAY, "Okay"),
    "4": (EMOJI_MOOD_GOOD, "Good"),
    "5": (EMOJI_MOOD_GREAT, "Great")
}


# MAIN FUNCTION TO START JOURNAL
def run_journal(current_user):
    display_journal_banner()
    journal_manager = JournalManager(JOURNAL_ENTRIES_JSON_FILE, current_user)
    console.print(f"Welcome back {current_user} to your Journal {EMOJI_WRITE}\n")
    while True:
        display_menu(JOURNAL_MENU)
        menu_choice = get_menu_choice(JOURNAL_MENU)
        if menu_choice == "1":
            console.print(f"{EMOJI_CREATE_ENTRY} You have chosen to create a new Journal Entry.\n")
            create_journal_entry(journal_manager)
        elif menu_choice == "2":
            console.print(f"{EMOJI_VIEW_ENTRIES} You have chosen to View Past Journal Entries.\n")
            view_journal_entries(journal_manager)
        elif menu_choice == "3":
            console.print(f"{EMOJI_WAVE} Thanks for using Mindful Moments. Goodbye and see you next time {current_user}!\n")
            break


# CREATE NEW JOURNAL ENTRY FLOW:
def create_journal_entry(journal_manager: JournalManager):
    console.print(f"{EMOJI_CREATE_ENTRY} Starting new journal entry.\n")
    console.print(f"{EMOJI_HOURGLASS} Take a moment to reflect on your day...(Daily Mood, Wins, Challenges, Gratitude and Goal for tomorrow)\n")
    try:
        console.print("How are you feeling today? Choose your Mood Rating: [1, 2, 3, 4 or 5]\n")
        mood_label = get_user_mood_selection(MOOD_RATINGS, encouragement_quotes)
        print()
        wins_input = get_valid_input("\nWhat went well today? \n")
        challenges_input = get_valid_input("\nWhat were the challenges you faced today? \n")
        gratitude_input = get_valid_input("\nWhat are you grateful for today? \n")
        goals_input = get_valid_input("\nWhat is your goal for tomorrow? \n")
        print()
        new_entry = JournalEntry(mood_label, wins_input, challenges_input, gratitude_input, goals_input)
        if journal_manager.save_journal_entry(new_entry):
            console.print(f"[green]{EMOJI_SUCCESSFUL} Your journal entry was saved successfully {EMOJI_SAVE}[/green]\n")
        else:
            console.print(f"[red]{EMOJI_WARNING} Sorry! There was a problem saving your entry.[/red]\n")
    except JournalCreationError:
        console.print(f"[red]{EMOJI_WARNING} Sorry! There was an error during creating your journal entry[/red]\n")
        return
    except Exception as err:
        console.print(f"[red]{EMOJI_WARNING} Unexpected error during creating your journal entry[/red]\n")

def get_user_mood_selection(mood_ratings, encouragement_quotes):
    """Handles mood selection, menu display and random selection to display respective mood encouragement quote."""
    display_menu(MOOD_RATINGS)
    mood_key = get_menu_choice(MOOD_RATINGS)
    emoji, mood_label = MOOD_RATINGS[mood_key]
    console.print(f"\n[bold bright_cyan]You have rated your daily mood as: {emoji} {mood_label}[bold bright_cyan]")
    mood_encouragement = random.choice(encouragement_quotes[mood_key])
    console.print(f"\n[magenta italic]{EMOJI_ENCOURAGEMENT} {mood_encouragement}[/magenta italic]\n")
    return mood_label

# VIEW PAST JOURNAL ENTRIES FLOW:
def view_journal_entries(journal_manager):
    all_user_entries = journal_manager.get_user_entries()
    if not all_user_entries:
        console.print(f"[red]{EMOJI_WARNING} Sorry! No journal entries found.[/red]\n")
        return
    for entry in all_user_entries:
        entry.display_entry()
        console.print("=" * 60)
        print()     # returns back to main after


# RUN THE JOURNAL - This is launched from the main after authenticated user login - links data to store to current user.
if __name__ == '__main__':
    user_manager = UserManager(USER_ACCOUNTS_JSON_FILE)
    run_journal()
