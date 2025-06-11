import json
from pathlib import Path
import bcrypt

from utilities.emojis import *

# CLASS FOR USER ACCOUNT DATA REPRESENTATION (data class to create user account instances to format for storage)
class UserAccount:
    def __init__(self, username, hashed_password):
        self.username = username
        self.hashed_password = hashed_password
    
    def to_dict(self):
        """ Converts UserAccount instance to a dict """
        return {
            "hashed_password": self.hashed_password
        }

    @classmethod
    def from_dict(cls, username, account_data):
        """ Reconstructs a UserAccount instance from dict data """
        return cls(username, account_data.get("hashed_password"))
    
    def verify_password(self, password_input):
        """ Verifies password by comparing plain text password input against stored hashed password (using bcrypt) """
        password_input_bytes = password_input.encode('utf-8')
        stored_password_bytes = self.hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_input_bytes, stored_password_bytes)

    def __str__(self):
        """ For printing username string in app e.g. welcome back current_user """
        return self.username


# BASE DATA MANAGER CLASS
class BaseDataManager:
    """ BASE CLASS BaseDataManager: Handles JSON file loading and saving data) """
    def __init__(self, json_file_path):
        self.json_file_path = json_file_path

    def load_json_file(self):
        """ Loads data from the JSON file """
        try:
            with open(self.json_file_path, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            print(f"{EMOJI_WARNING} {self.json_file_path} is empty, invalid or corrupted: {json.JSONDecodeError}")
            return {}
        except FileNotFoundError:
            print(f"{EMOJI_WARNING} {self.json_file_path} not found: Creating new empty file.")
            self.save_json_file({})
            return {}
        except Exception as err:
            print(f"{EMOJI_WARNING} Error occured while loading {self.json_file_path} file: {err}")
            return {}
        
    def save_json_file(self, updated_data):
        """ Saves data to the JSON file """
        try:
            with open(self.json_file_path, 'w') as file:
                json.dump(updated_data, file, indent=4)
                print(f"{EMOJI_SUCCESSFUL} File saved successfully to {self.json_file_path} {EMOJI_SAVE}")
                return True
        except json.JSONDecodeError:
            print(f"{EMOJI_WARNING} Error during attempt to save to {self.json_file_path}. File is empty or corrupted: {json.JSONDecodeError}")
            return False
        except Exception as err:
            print(f"{EMOJI_WARNING} Error saving updated data to {self.json_file_path}: {err}")
            return False

# USER MANAGER CLASS
class UserManager(BaseDataManager):
    """ Manages user account authentication, registration and user account storage """
    def __init__(self, json_file_path):
        super().__init__(json_file_path)
        self.user_accounts = self.load_json_file()

    def user_exists(self, username): 
        """ Check if a user exists in stored accounts: Returns True if existing, otherwise False """
        return username in self.user_accounts

    def get_user_account(self, username):
        """ Retrieves a UserAccount instance by username. Returns None if username doesn't exist or error occurs """
        try:
            if self.user_exists(username):
                return UserAccount.from_dict(username, self.user_accounts[username])
            else:
                print(f"{EMOJI_WARNING} Username not found")
                return None
        except Exception as err:
            print(f"{EMOJI_WARNING} Error occurred during retrieving user account: {err}")

    def save_user_account(self, user_account):
        """ Adds a new user and saves accounts to the JSON file: Returns True if succesfful, otherwise False """
        try:
            self.user_accounts[user_account.username] = user_account.to_dict()
            saved_account = self.save_json_file(self.user_accounts)
            if not saved_account:
                print(f"{EMOJI_WARNING} Failed to save new user account.")
                return False
            self.reload_user_accounts()
            return True
        except Exception as err:
            print(f"{EMOJI_WARNING} Error occurred during adding user account: {err}")
            return False
    
    def reload_user_accounts(self):
        """ Reload user accounts from JSON file (to sync so new user can login after) """
        try:
            self.user_accounts = self.load_json_file()
            return True
        except Exception as err:
            print(f"{EMOJI_WARNING} Failed to reload user accounts: {err}")
            return False

    def register_user(self, username, password):
        """ Register a new user account with a username and hashed password """
        try:
            if self.user_exists(username):
                hashed_password = self.hash_password(password)
                user_account = UserAccount(username, hashed_password)
                return True
        except Exception as err:
            print(f"{EMOJI_WARNING} Error occurred during registering new user account: {err}")
            return False


    def hash_password(self, password):
        """ Hashes password using bcrypt, then returned the bcrypt hashed password as a string (so it can be stored in JSON) """
        password_bytes = password.encode('utf-8')
        generated_salt = bcrypt.gensalt()
        hashed_password_bytes = bcrypt.hashpw(password_bytes, generated_salt)
        hashed_password = hashed_password_bytes.decode('utf-8')
        return hashed_password

    def authenticate_user(self, user_account, password):
        """ Authenticate a user's login credentials """
        if not user_account:
            print(f"{EMOJI_INVALID} User account does not exist.")
            print(f"{EMOJI_WARNING} If you are a new user, please create a New User Account.")
            return False
        if user_account.verify_password(password):
            return True
        else:
            print("Incorrect password. Login Unsuccessful. Please try again.")
            return False
