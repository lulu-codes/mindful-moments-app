# user_auth_models.py

# IMPORT BUILT IN LIBRARIES:
import json
import bcrypt

# IMPORT THIRD-PARTY LIBRARIES:
from rich import print

# IMPORT CUSTOM MODULES:
from ui.emojis import EMOJI_WARNING, EMOJI_INVALID

# IMPORT CUSTOM EXCEPTION CLASSES:
from core.exception_classes import (
    DataFileCorruptedError,
    FileLoadingError,
    FileSavingError,
    UserNotFoundError,
    ErrorAddingUser,
    ErrorGettingUserAccount,
    UserRegistrationError,
    AuthenticationError
    )


# CLASS FOR USER ACCOUNT DATA REPRESENTATION (data class to create user account instances to format for storage)
class UserAccount:
    def __init__(self, username, hashed_password):
        self.username = username
        self.hashed_password = hashed_password
    
    def to_dict(self):
        """Converts UserAccount instance to a dict."""
        return {
            "hashed_password": self.hashed_password
        }

    @classmethod
    def from_dict(cls, username, account_data):
        """Reconstructs a UserAccount instance from dict data."""
        return cls(username, account_data.get("hashed_password"))
    
    def verify_password(self, password_input):
        """Verifies password by comparing plain text password input against stored hashed password - using bcrypt."""
        password_input_bytes = password_input.encode('utf-8')
        stored_password_bytes = self.hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_input_bytes, stored_password_bytes)

    def __str__(self):
        """For printing username string in app e.g. welcome back current user."""
        return self.username


# BASE DATA MANAGER CLASS
class BaseDataManager:
    """BASE CLASS BaseDataManager: Handles JSON file loading and saving data."""
    def __init__(self, json_file_path):
        self.json_file_path = json_file_path

    def load_json_file(self):
        """Loads data from the JSON file."""
        try:
            with open(self.json_file_path, 'r') as file:
                content = file.read().strip()
                if not content:     # If file exists but is an empty file (usually for first time users),
                    return {}       # Then return and create new dict in file
                else:
                    return json.loads(content)
        except json.JSONDecodeError:
            raise DataFileCorruptedError(f"[red]{EMOJI_WARNING} Error loading data: Data file is corrupted or invalid.[/red]\n")
        except Exception as err:
            raise FileLoadingError(f"[red]{EMOJI_WARNING} Unexpected Error while loading file:[/red]\n") from err
        

    def save_json_file(self, updated_data):
        """Saves data to the JSON file. Returns True if save successful, otherwise raises error."""
        try:
            with open(self.json_file_path, 'w') as file:
                json.dump(updated_data, file, indent=4)
            return True
        except (IOError, TypeError) as err:
            raise FileSavingError(f"[red]{EMOJI_WARNING} Error saving data:[/red]\n") from err
        except Exception as err:
            raise FileSavingError(f"[red]{EMOJI_WARNING} Unexpected error occured while saving data.[/red]\n") from err


# USER MANAGER CLASS
class UserManager(BaseDataManager):
    """Manages user account authentication, registration and user account storage."""
    def __init__(self, json_file_path):
        super().__init__(json_file_path)
        self.user_accounts = self.load_json_file()

    def is_existing_user(self, username): 
        """Check if a user exists in stored accounts: Returns True if existing, otherwise False."""
        return username in self.user_accounts

    def get_user_account(self, username):
        """Retrieves and returns a UserAccount instance by username if exists, otherwise raises error."""
        try:
            if self.is_existing_user(username):
                return UserAccount.from_dict(username, self.user_accounts[username])
            else:
                raise UserNotFoundError(f"[red]{EMOJI_INVALID} {username} not found.[/red]")
        except Exception as err:
            raise ErrorGettingUserAccount(f"[red]{EMOJI_WARNING} Unexpected Error occurred while attempting to retrieve user account.[/red]\n") from err

    def authenticate_user(self, user_account, password):
        """Authenticate a user's login credentials, returns UserAccont instance if successfully authenticated, otherwise None/error"""
        try:
            if user_account.verify_password(password):
                return user_account
            else:
                return None
        except Exception as err:
            raise AuthenticationError(f"[red]{EMOJI_WARNING} Error occurred while authenticating user.[/red]\n") from err


    def register_user(self, username, password):
        """Register a new user account with a username and hashed password, returns True if successful, otherwise False."""
        try:
            hashed_password = self.hash_password(password)
            user_account = UserAccount(username, hashed_password)   # Creates instance of user account
            return self.add_user_account(user_account)
        except Exception as err:
            raise UserRegistrationError(f"[red]{EMOJI_WARNING} Error occurred during registration of new user account.[/red]\n") from err

    def hash_password(self, password):
        """Hashes password using bcrypt, then returned the bcrypt hashed password as a string (so it can be stored in JSON)."""
        password_bytes = password.encode('utf-8')
        generated_salt = bcrypt.gensalt()
        hashed_password_bytes = bcrypt.hashpw(password_bytes, generated_salt)
        hashed_password = hashed_password_bytes.decode('utf-8')
        return hashed_password

    def add_user_account(self, user_account):
        """Adds a new user and saves accounts to the JSON file: Returns True if succesfful, otherwise raises error."""
        try:
            self.user_accounts[user_account.username] = user_account.to_dict()
            self.save_json_file(self.user_accounts)
            # Reload user accounts from JSON file to sync memory, so new user can login after creating acc
            self.user_accounts = self.load_json_file()
            return True
        except Exception as err:
            raise ErrorAddingUser(f"[red]{EMOJI_WARNING} Error occurred while adding user account.[/red]\n") from err
