# journal_models.py
# CLASSES, METHODS/HELPERS FOR JOURNAL ENTRY DATA REPRESENTATION AND MANAGING USER'S JOURNAL ENTRIES

# IMPORT THIRD-PARTY LIBRARIES:
from datetime import datetime
from rich import print
from rich.table import Table
from rich.console import Console

# IMPORT CUSTOM CORE MODULES:
from core.user_auth_models import BaseDataManager
from ui.emojis import EMOJI_DATE_TIME, EMOJI_HEART, EMOJI_WINS, EMOJI_CHALLENGES, EMOJI_GRATITUDE, EMOJI_GOALS, EMOJI_WARNING

# IMPORT CONSTANT FILE PATHS
from core.file_paths import JOURNAL_ENTRIES_JSON_FILE

# Custom Exception Classes
class UserNotLoggedInError(Exception):
    """Exception raised when a method requires a logged in user, but none is found."""
    pass

# CLASS FOR JOURNAL ENTRY: FOR DATA REPRESNTATION
class JournalEntry():
    """Represents a journal entry, used for saving and loading from JSON file."""
    def __init__(self, mood, wins, challenges, gratitude, goals, timestamp=None):
        """Use timestamp for loading from JSON file, otherwise create new timestamp."""
        self.timestamp = timestamp or datetime.now().isoformat()
        self.mood = mood
        self.wins = wins
        self.challenges = challenges
        self.gratitude = gratitude
        self.goals = goals

    def to_dict(self):
        """Converts the journal entry to dict format for JSON storage."""
        return {
            "timestamp": self.timestamp,
            "mood": self.mood,
            "wins": self.wins,
            "challenges": self.challenges,
            "gratitude": self.gratitude,
            "goals": self.goals,
        }

    @classmethod
    def from_dict(cls, entry_dict):
        """Reconstructs a JournalEntry instance loaded from dict data - used when loading from JSON file."""
        return cls(
            timestamp=entry_dict["timestamp"],
            mood=entry_dict["mood"],
            wins=entry_dict["wins"],
            challenges=entry_dict["challenges"],
            gratitude=entry_dict["gratitude"],
            goals=entry_dict["goals"],
        )

    def get_display_datetime(self):
        """Returns user friendly timestamp format for display."""
        return datetime.fromisoformat(self.timestamp).strftime("%d-%m-%Y %H:%M")
    
    def display_entry(self):
        """Formatted printed journal entry for display."""
        console = Console()
        table = Table(title="Mindful Moments Reflections\n", show_lines=True)
        table.add_column(f"{EMOJI_DATE_TIME} Journal Entry created on", style="cyan")
        table.add_column(f"{self.get_display_datetime()}", style="magenta", no_wrap=False)
        table.add_row(f"{EMOJI_HEART} Mood Rating", self.mood)
        table.add_row(f"{EMOJI_WINS} Wins of the day", self.wins)
        table.add_row(f"{EMOJI_CHALLENGES} Challenges of the day", self.challenges)
        table.add_row(f"{EMOJI_GRATITUDE} Gratitude of the day", self.gratitude)
        table.add_row(f"{EMOJI_GOALS} Goal for tomorrow", self.goals)
        console.print(table)

# JOURNAL MANAGER CLASS: FOR MANAGING USER ENTRIES
class JournalManager(BaseDataManager):
    """Inherits from BaseDataManager to handle file loading and saving for JSON storage."""
    def __init__(self, json_file_path=JOURNAL_ENTRIES_JSON_FILE, current_user=None):
        super().__init__(json_file_path)
        self.current_user = current_user
        self.journal_data = self.load_json_file() or {}

    def validate_user(self):
        """Helper method used to ensure a user is logged in (and has a username attribute)."""
        if not self.current_user or not hasattr(self.current_user, 'username'):
            raise UserNotLoggedInError(f"[red]{EMOJI_WARNING} No user is currently logged in.[/red]")

    def get_user_entries(self):
        """Retrieves and returns a list of JournalEntry instances for the validated current user."""
        self.validate_user()
        user_entries = self.journal_data.get(self.current_user.username, [])
        return [JournalEntry.from_dict(entry) for entry in user_entries]


    def save_journal_entry(self, journal_entry):
        """ Saves a journal entry for the current user, returns True if entry saved successfully, otherwise False """
        try:
            self.validate_user()
            username = self.current_user.username
            # Checks if user already has stored entries, otherwise cretes an empty list for saving new entries
            if username not in self.journal_data:
                self.journal_data[username] = []
            # Adds new journal entry to user's list of entries and attempts to save entry
            self.journal_data[username].append(journal_entry.to_dict())
            saved_entry = self.save_json_file(self.journal_data)
            if saved_entry:
                return True
            else:
                print(f"[red]{EMOJI_WARNING} Failed to save entry for {username}[/red]\n")
                return False
        except Exception as err:
            print(f"[red]{EMOJI_WARNING} Error occurred while saving journal entry: {err}[/red]\n")
            return False