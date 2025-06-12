# journal.py
# FOR CREATING & VIEWING JOURNAL ENTRIES LOGIC AND FLOW

from pathlib import Path
import random

from models.journal_models import JournalManager, JournalEntry, UserNotLoggedInError
from models.user_auth_models import UserManager
from models.helpers import display_menu, get_menu_choice, get_valid_input
from models.quotes import encouragement_quotes

from ui.ascii_art import display_journal_banner
from ui.emojis import *

# Custom classes exceptions (base Exception)
class JournalCreationCancelled(Exception):
    """ Raised when user cancels journal entry creation """
    pass

# # CONSTANT FILE PATH TO USER ACCOUNTS DATA (used to access and tie journal entries to user)
# USER_ACCOUNTS_JSON_FILE = Path('data_storage/user_accounts.json')


# JOURNAL MENU OPTIONS (Dict based menu)
JOURNAL_MENU = {
    "1": f"{EMOJI_CREATE_ENTRY} Create a Journal Entry",
    "2": f"{EMOJI_VIEW_ENTRIES} View Past Journal Entries",
    "3": f"{EMOJI_LOGOUT} Logout"
}

# MOOD RATINGS
"""  for simple input prompt, dict key holds tuple of emoji + label """
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
    print(f"Welcome back {current_user} to your Journal {EMOJI_WRITE}\n")
    while True:
        display_menu(JOURNAL_MENU)
        menu_choice = get_menu_choice(JOURNAL_MENU)
        if menu_choice == "1":
            print("You have chosen to create a new Journal Entry\n")
            create_journal_entry(journal_manager)
        elif menu_choice == "2":
            print("You have chosen to View Past Journal Entries\n")
            view_journal_entries(journal_manager)
        elif menu_choice == "3":
            print(f"{EMOJI_WAVE} Thanks for using Mindful Moments. Goodbye and see you next time {current_user}!\n")
            break


# CREATE NEW JOURNAL ENTRY FLOW:
def create_journal_entry(journal_manager: JournalManager):
    print(f"{EMOJI_CREATE_ENTRY} Starting new journal entry\n")
    print(f"{EMOJI_HOURGLASS} Take a moment to reflect on your day... (Daily Mood, Wins, Challenges, Gratitude and Goal for tomorrow)\n")
    try:
        print("How are you feeling today? Choose your Mood Rating: [1, 2, 3, 4 or 5]\n")
        mood_label = get_user_mood_selection(MOOD_RATINGS, encouragement_quotes)
        print()
        wins_input = get_valid_input("What went well today? ")
        challenges_input = get_valid_input("What were the challenges you faced today? ")
        gratitude_input = get_valid_input("What are you grateful for today? ")
        goals_input = get_valid_input("What is your goal for tomorrow? ")
        print()
        new_entry = JournalEntry(mood_label, wins_input, challenges_input, gratitude_input, goals_input)
        if journal_manager.save_journal_entry(new_entry):
            print(f"{EMOJI_SUCCESSFUL} Your journal entry was saved successfully {EMOJI_SAVE}\n")
        else:
            print(f"{EMOJI_WARNING} Sorry! There was a problem saving your entry\n")
    except Exception as err:
        print(f"{EMOJI_WARNING} Sorry! There was an error during creating your journal entry: {err}")

def get_user_mood_selection(mood_ratings, encouragement_quotes):
    """ Handles mood selection, menu display and random selection to display respective mood encouragement quote"""
    display_menu(MOOD_RATINGS)
    mood_key = get_menu_choice(MOOD_RATINGS)
    emoji, mood_label = MOOD_RATINGS[mood_key]
    print(f"You have rated your daily mood as: {emoji} {mood_label}")
    mood_encouragement = random.choice(encouragement_quotes[mood_key])
    print(f"{EMOJI_ENCOURAGEMENT} {mood_encouragement}")
    return mood_label

# VIEW PAST JOURNAL ENTRIES FLOW:
def view_journal_entries(journal_manager):
    all_user_entries = journal_manager.get_user_entries()
    if not all_user_entries:
        print(f"{EMOJI_WARNING} Sorry! No journal entries found\n")
        return
    for entry in all_user_entries:
        entry.display_entry()
        print("=" * 60)
        print()


# RUN THE JOURNAL
if __name__ == '__main__':
    user_manager = UserManager(USER_ACCOUNTS_JSON_FILE)
    test_user = user_manager.get_user_account("nhihuynh")
    if test_user:
        run_journal(test_user)
    else:
        print("Test user not found")
