# test_user_auth.py

# Manual testing already done.
# Tested creating new user and logging in with testuser and testuser2.
# Successfully created new user, logging in and user account data storage in user_accounts JSON file.

# Need to do unit testing using pytest for helper functions

# PYTEST UNIT TESTING
# Testing functions in user_auth_models.py using Pytest (https://docs.pytest.org/en/stable/getting-started.html)

import sys
import os
from pathlib import Path
import bcrypt

# Add the project root to the Python path so we can import from core
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.user_auth_models import UserManager
from core.file_paths import USER_ACCOUNTS_JSON_FILE

def test_register_and_authenticate_user(tmp_path):
    """
    This test function checks if a user can be registered and authenticated successfully.
    tmp_path = Pytest temporary path to test data (isolated from actual app data files when running Pytests)

    Test run for:
    1. Registering a new user
    2. Check if the user is stored and exists after new user registration
    3. Retrieve the user account data (username)
    4. Authenticating the user with correct login credentials (returns UserAccount instance with successful authentication)
    4a. Checks password directly using verify_password() with bcrypt (with correct password - method is used in authenticate_user())
    5. Authenticating the user with wrong password (Fails the authentication with wrong password)
    5a. Checks password directly using verify_password() with bcrypt (with wrong password)
    """

    # Setup and created a temporary empty test JSON file in temp file path
    test_json_path = tmp_path / "test_user_accounts.json"

    # Creates an empty JSON file for testing
    test_json_path.write_text("{}")

    # Init UserManager with this test file
    user_manager = UserManager(test_json_path)

    username = "pytestuser123"
    password = "pytestpassword123"

    # 1. Registering a new user
    assert user_manager.register_user(username, password) == True

    # 2. Check if the user exists (after registering user)
    assert user_manager.is_existing_user(username) == True

    # 3. Retrieving stored user account username
    user_account = user_manager.get_user_account(username)
    assert user_account.username == username

    # 4. Successful authentication (with correct password)
    assert user_manager.authenticate_user(user_account, password) is not None

    # 4a. Directly test verify_password() with bcrypt = True for correct password
    assert user_account.verify_password(password) == True

    # 5. Unsuccessful authentication (with wrong password)
    assert user_manager.authenticate_user(user_account, "wrongpass") is None

    # 5a. Directly test verify_password() with bcrypt = False for wrong password
    assert user_account.verify_password("wrongpass") == False


    # Write Test for `add_user_account()` | Check if a user is in stored data
