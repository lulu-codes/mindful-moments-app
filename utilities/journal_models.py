# journal_models.py
from pathlib import Path
from datetime import datetime
from utilities.user_auth_models import BaseDataManager
from utilities.emojis import *
import random
from utilities.helpers import display_menu, get_menu_choice
from utilities.quotes import encouragement_quotes

# CONSTANT FILE PATH TO JSON file (for stored users journal entries data)
JOURNAL_ENTRIES_JSON_FILE = Path('data/journal_entries.json')

# MOOD RATINGS
"""  for simple input prompt, dict key holds tuple of emoji + label """
MOOD_RATINGS = {
    "1": (EMOJI_MOOD_AWFUL, "Awful"),
    "2": (EMOJI_MOOD_SAD, "Sad"),
    "3": (EMOJI_MOOD_OKAY, "Okay"),
    "4": (EMOJI_MOOD_GOOD, "Good"),
    "5": (EMOJI_MOOD_GREAT, "Great")
}

def get_user_mood_selection(mood_ratings, encouragement_quotes):
    """ Handles mood selection, menu display and random selection to display respective mood encouragement quote"""
    display_menu(MOOD_RATINGS)
    mood_key = get_menu_choice(MOOD_RATINGS)
    emoji, mood_label = MOOD_RATINGS[mood_key]
    print(f"You have rated your daily mood as: {emoji} {mood_label}")
    mood_encouragement = random.choice(encouragement_quotes[mood_key])
    print(f"{EMOJI_ENCOURAGEMENT} {mood_encouragement}")
    return mood_label

# CLASS FOR JOURNAL ENTRY DATA REPRESNTATION
class JournalEntry():
    """ Data class to create journal entries to format for display and storage """
    def __init__(self, mood, wins, challenges, gratitude, goals, timestamp=None):
        """ Use timestamp for loading from JSON file, otherwise create new timestamp """
        self.timestamp = timestamp or datetime.now().isoformat()
        self.mood = mood
        self.wins = wins
        self.challenges = challenges
        self.gratitude = gratitude
        self.goals = goals

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "mood": self.mood,
            "wins": self.wins,
            "challenges": self.challenges,
            "gratitude": self.gratitude,
            "goals": self.goals,
        }

    def get_display_datetime(self):
        """ Format timestamp for display (in user friendly format) """
        return datetime.fromisoformat(self.timestamp).strftime("%d-%m-%Y %H:%M")
    
    @classmethod
    def from_dict(cls, entry_dict):
        """ Reconstructs a JournalEntry instance loaded from dict data """
        return cls(
            timestamp=entry_dict["timestamp"],
            mood=entry_dict["mood"],
            wins=entry_dict["wins"],
            challenges=entry_dict["challenges"],
            gratitude=entry_dict["gratitude"],
            goals=entry_dict["goals"],
        )

    def display_entry(self):
        print(f"{EMOJI_DATE_TIME} Journal Entry created on: {self.get_display_datetime()}")
        print(f"{EMOJI_HEART} Mood Rating: {self.mood}")
        print(f"{EMOJI_WINS} Wins of the day: {self.wins}")
        print(f"{EMOJI_CHALLENGES} Challenges of the day: {self.challenges}")
        print(f"{EMOJI_GRATITUDE} Gratitude of the day: {self.gratitude}")
        print(f"{EMOJI_GOALS} Goal for tomorrow: {self.goals}")


# JOURNAL MANAGER CLASS MANAGES ENTRIES FOR A USER
class JournalManager(BaseDataManager):
    """ Inherits from BaseDataManager class to manage entries for a user and handle JSON file loading and saving """
    def __init__(self, json_file_path=JOURNAL_ENTRIES_JSON_FILE, current_user=None):
        super().__init__(json_file_path)
        self.current_user = current_user
        self.journal_data = self.load_json_file() or {}

    def get_user_entries(self):
        """ Retrun list of JournalEntry instances for current user """
        if not self.current_user or not hasattr(self.current_user, 'username'):
            print(f"{EMOJI_WARNING} No user logged in to retrieve journal entries")
            return []
        user_entries = self.journal_data.get(self.current_user.username, [])
        return [JournalEntry.from_dict(entry) for entry in user_entries]

    def save_journal_entry(self, journal_entry):
        try:
            if not self.current_user or not hasattr(self.current_user, 'username'):
                raise ValueError(f"{EMOJI_WARNING} No user logged in to retrieve journal entries")
                # return False
            if self.current_user.username not in self.journal_data:
                self.journal_data[self.current_user.username] = []
            self.journal_data[self.current_user.username].append(journal_entry.to_dict())
            saved_entry = self.save_json_file(self.journal_data)
            if not saved_entry:
                raise 
            #     return True
            # else:
                # print(f"{EMOJI_WARNING} Failed to save entry for {self.current_user.username}")
            return saved_entry
        except Exception as err:
            return False
            # print(f"{EMOJI_WARNING} Error occurred during adding journal entry: {err}")