# exception_classes.py

import json

class DataManagerError(Exception):
    """Base class for file related errors."""
    pass

class DataFileCorruptedError(json.JSONDecodeError, DataManagerError):
    """Raised when JSON data file is corrupt or invalid."""
    pass

class FileLoadingError(DataManagerError):
    """Raised when there is an unexpected error during attempt to load JSON file."""
    pass
    
class FileSavingError(DataManagerError):
    """Raised when there is an unexpected error during attempt to save JSON file."""
    pass

class UserManagerError(DataManagerError):
    """Base class for User management related errors."""
    pass

class UserNotFoundError(UserManagerError):
    """Raised when user not found."""
    pass

class ErrorAddingUser(UserManagerError):
    """Raised when error adding user account."""
    pass

class ErrorGettingUserAccount(UserManagerError):
    """Raised when error getting user account."""
    pass

class UserRegistrationError(UserManagerError):
    """Raised when error during user registration."""
    pass

class AuthenticationError(UserManagerError):
    """Raised when error during authenticating user's account login credentials."""
    pass

class AccountRegistrationError(Exception):
    """Raised when error with registering new user account."""
    pass

class LoginError(Exception):
    """Base class for when login related errors."""
    pass

class AuthenticationError(LoginError):
    """Raises error if error during authentication."""
    pass

class AccountCreationError(Exception):
    """Base class for errors during creating new account."""
    pass


# Custom classes exceptions (base Exception)
class JournalCreationError(Exception):
    """Raised when error during journal entry creation."""
    pass