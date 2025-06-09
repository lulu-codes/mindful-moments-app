import json
from pathlib import Path
from datetime import datetime
import random
import quotes
import data
import mood
from utilities.emojis import EMOJI_CREATE_ENTRY, EMOJI_VIEW_ENTRIES, EMOJI_MOOD_SUMMARY, EMOJI_LOGOUT, EMOJI_MOOD_AWFUL, EMOJI_MOOD_SAD, EMOJI_MOOD_OKAY, EMOJI_MOOD_GOOD, EMOJI_MOOD_GREAT, EMOJI_WRITE


# Journal menu options - create journal entry, view past journal entry, view mood summary, logout
JOURNAL_MENU_OPTIONS = {
    "1": f"{EMOJI_CREATE_ENTRY} Create a Journal Entry",
    "2": f"{EMOJI_VIEW_ENTRIES} View Past Journal Entries",
    "3": f"{EMOJI_MOOD_SUMMARY} View Mood Trend Summary",
    "4": f"{EMOJI_LOGOUT} Logout"
}

MOOD_RATING_OPTIONS = {
    "1": f"{EMOJI_MOOD_AWFUL} Awful",
    "2": f"{EMOJI_MOOD_SAD} Sad",
    "3": f"{EMOJI_MOOD_OKAY} Okay",
    "4": f"{EMOJI_MOOD_GOOD} Good",
    "5": f"{EMOJI_MOOD_GREAT} Great"
}

MOO_DESCRIPTIONS = {
    "1": "Overwhelmed or had a rough day",
    "2": "Feeling down or low",
    "3": "Neutral",
    "4": "Feeling pretty good or pleasant",
    "5": "Feeling happy, fulfilled or amazing"
}



# MAIN MENU INTERFACE AND NAVIGATION (after login):
# 1. Add new journal entry
# 2. View past journal entry -> Allow editing/deleting??
# 3. View mood trend summary (NICE TO HAVE FEATURE)
def journal_menu(menu_options):
    print(f"Ready to Journal? {EMOJI_WRITE}")
    display_main_menu(menu_options)
    user_choice = input("Enter a menu choice: ")
    while user_choice not in menu_options.keys():
        print("Invalid option. Please try again.")
        user_choice = input("Enter a valid menu choice: ")
    if user_choice == "1":
        create_journal()
    elif user_choice == "2":
        view_journal()
    elif user_choice == "3":
        view_mood_summary()
    elif user_choice == "4":
        logout()

# Journal file (JSON)
# eg. SETTINGS_JSON_FILE = "settings.json"
JOURNAL_ENTRIES_JSON_FILE = Path('data/journals_entries.json')

# JOURNAL ENTRY FUNCTIONS in journal.py

# NEW JOURNAL ENTRY FUNCTIONS:
# Add classes for 'Moodtracker' and 'JournalEntry'
class JournalEntry:
    def __init__(self, date, mood, wins, challenges, goals, gratitude):
        self.datetime = datetime.now()
        self.mood = mood    
        self.wins = wins
        self.challenges = challenges
        self.gratitude = gratitude
        self.goals = goals

    def display(self):
        print(f"Journal Entry created on: {self.timestamp}")
        print(f"Mood Rating: {self.mood}")
        print(f"Wins of the day: {self.wins}")
        print(f"Challenges of the day: {self.challenges}")
        print(f"Gratitude of the day: {self.gratitude}")
        print(f"Goal for tomorrow: {self.goals}")

    # def save_to_file():


    # def save_to_file(self, ):

    # def load_from_file():
    
    # def display_affirmation():

    # def add_journal_entry():
        
# MOOD TRENDS SUMMARY in mood.py


# Function for add new journal entry
# Log timestamp
# Input prompts
# 1. Daily Mood - Save option
# 2. Daily Wins - Save option
# 3. Daily Challenges - Save option
# 4. Daily Gratitude (optional) - Save option
# 5. Completed entry returns randomly selected motivational affirmation
# WRITE to JSON file


# VIEW JOURNAL ENTRY FUNCTIONS:
# Function for view past journal entry
# READ to JSON file
# Show logged timestamp
# Navigate by timestamp (days/time)
# To work on - Allow Edit/Delete entries?
# Write/Read JSON files
# 1. Daily Mood
# 2. Daily Wins
# 3. Daily Challenges
# 4. Daily Gratitude
# 5. Motivational affirmation

def run_journal():
    print("Welcome to Mindful Moments - Your Personal Reflection Journaling App!")
    while True:
        display_main_menu(JOURNAL_MENU_OPTIONS)
        print(f"Select an option from the Menu to get started! {EMOJI_WRITE}")

if __name__ == '__main__':
    run_journal()
