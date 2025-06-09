import json
from pathlib import Path
import bcrypt

from utilities.emojis import EMOJI_INVALID, EMOJI_WARNING

# CLASS REPRESENTS A USER ACCOUNT (Used to support storing and checking username and hashed password):
class UserAccount:
    # CONSTRUCTOR to create a new UserAccount instance
    # Takes in the parameters of the user's login name (username) and the user's hashed password as a string (hashed_password_str)
    def __init__(self, username, hashed_password):
        self.username = username
        self.hashed_password = hashed_password
    
    # METHOD to convert this UserAccount instance into a dict, so that it can be saved into the JSON file (as user acount data)
    def to_dict(self):
        return {
            "hashed_password": self.hashed_password
        }

    @classmethod
    # CLASS METHOD to reconstruct a UserAccount instance from the JSON dict data.
    # Takes the username as the key and account_data (dict) which contains the hashed password
    def from_dict(cls, username, account_data):
        return cls(username, account_data.get("hashed_password"))
    
    # METHOD to verify user's password input against the stored hashed password, returns True if they match, otherwise returns False (Bcrypt used)
    def verify_password(self, password_input):
        password_input_bytes = password_input.encode('utf-8')                   # Converting 'password_input' string into bytes (to use in bcrypt)
        stored_password_bytes = self.hashed_password.encode('utf-8')            # Converting 'stored_password_bytes' (from JSON string) back into bytes (to use in bcrypt)
        return bcrypt.checkpw(password_input_bytes, stored_password_bytes)      # Using bcrypt to compare 'password_input_bytes' with 'stored_password_bytes'. Returns 'True' if they match

    # For printing username string in app e.g. welcome back 'user' etc.
    def __str__(self):
        return self.username

# PARENT CLASS BaseDataManager (Used to support file handling for loading and saving JSON data).
# As path files and data will be handled similarly for user accounts and journal entries, Child classes also created for UserManager and JournalManager, which inherit from Base class and extends with additional methods related to the Child classes.
class BaseDataManager:
    def __init__(self, json_file_path):
        self.json_file_path = json_file_path

    def load_json_file(self):
        try:
            with open(self.json_file_path, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            print(f"Warning: {self.json_file_path} is empty, invalid or corrupted.")
            return {}
        except Exception as LoadJsonErr:
            print(f"Error occured while loading {self.json_file_path} file: {LoadJsonErr}")
            return {}
        except FileNotFoundError:
            print(f"{self.json_file_path} not found. Creating new empty file.")
            self.save_json_file({})
            return {}
        
    def save_json_file(self, updated_data):
        try:
            with open(self.json_file_path, 'w') as file:
                json.dump(updated_data, file, indent=4)
                print(f"File saved successfully to {self.json_file_path}")
                return True
        except json.JSONDecodeError:
            print("Warning: Accounts file is empty or corrupted.")
            return False
        except Exception as SaveJsonErr:
            print(f"Error saving updated data to {self.json_file_path}: {SaveJsonErr}")
            return False

# Create class to define exception name, inherits 'Exception' generic base class
# Create 'error' classes to handle errors, use try and except to test.

# CHILD CLASS UserManager - Used to inherit BaseDataManager (file handling methods) and used with UserAccount class instances to check, get and add user account data.
class UserManager(BaseDataManager):
    def __init__(self, json_file_path):
        super().__init__(json_file_path)
        self.user_accounts = self.load_json_file()

    def user_exists(self, username):
        if username in self.user_accounts:
            return True
        else:
            return False
        
    def get_user_account(self, username):
        try:
            if self.user_exists(username):
                return UserAccount.from_dict(username, self.user_accounts[username])
            else:
                return None
        except Exception as GetUserErr:
            print(f"Get user account error: {GetUserErr}")

    def add_user_account(self, user_account):
        self.user_accounts[user_account.username] = user_account.to_dict()
        saved_account = self.save_json_file(self.user_accounts)
        if not saved_account:
            print(f"{EMOJI_WARNING} Failed to save new user account.")
            return False
        self.user_accounts = self.load_json_file()        # Reload from updated file with new user added,to be able to login with stored user acc
        print(f"for testing Reloaded user accounts: {self.user_accounts}")        # remove line after testing
        return True
    
    # Method to hash password (return as a String so it can be stored in user_accounts JSON file).
    def hash_password(self, password):
        password_bytes = password.encode('utf-8')                                   # Converting 'new_password' string into bytes (for bcrypt usage)
        generated_salt = bcrypt.gensalt()                                           # Using bcrypt to generate a random salt
        hashed_password_bytes = bcrypt.hashpw(password_bytes, generated_salt)       # Using bcrypt to hash 'password_bytes' combined with 'generated_salt', to create a 'hashed_password_bytes'
        hashed_password_str = hashed_password_bytes.decode('utf-8')                 # Converting 'hashed_password_bytes' to string version (so that it can be saved in JSON storage later)
        hashed_password = hashed_password_str                                       # Assigning hashed_password variable for consistency and readability in other functions/methods
        return hashed_password                                                      # Returning the 'hashed_password' (decoded as string version)

    # FUNCTION --> METHOD TO AUTHENTICATE USER ACC CREDENTIALS WHEN USER ATTEMPTING TO LOGIN.
    def authenticate_user(self, user_account, password):
        if not user_account:
            print(f"{EMOJI_INVALID} User account does not exist.")
            print(f"{EMOJI_WARNING} If you are a new user, please create a New User Account.")
            return False
        if user_account.verify_password(password):
            return True
        else:
            print("Incorrect password. Login Unsuccessful. Please try again.")
            return False
        
    def create_user(self, username, password):
        if self.user_exists(username):
            return False
        hashed_password = self.hash_password(password)
        new_account = UserAccount(username, hashed_password)
        return self.add_user_account(new_account)       # Returns True/False depending on if save succesful

