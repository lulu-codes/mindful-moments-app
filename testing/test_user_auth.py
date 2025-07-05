# test_user_auth.py

# Manual testing already done.
# Tested creating new user and logging in with testuser and testuser2.
# Successfully created new user, logging in and user account data storage in user_accounts JSON file.

# Need to do unit testing using pytest for helper functions

# PYTEST
# Testing functions in user_auth_models.py using Pytest (https://docs.pytest.org/en/stable/getting-started.html)

from core.user_auth_models import UserManager
from core.file_paths import USER_ACCOUNTS_JSON_FILE
from pathlib import Path
import sys
import os

def test_register_and_authenticate_user(tmp_path):
    """
    This test function checks if a user can be registered and authenticated successfully.
    tmp_path used by pytest to read/write/load from test_user_accounts.json file that I created in data_storage folder,
    (so that it doesn't overwrite the stored user data when running the test.)

    Test run for:
    1. Registering a new user
    2. Check if the user exists after new user account registration (create new account)
    3. Retrieve the user account data
    4. Authenticate the user with correct login credentials (correct username and password)
    5. Fail the authentication when the wrong password is entered
    """
    test_json_path = tmp_path / "test_user_accounts.json"
    user_manager = UserManager(test_json_path)

    username = "pytestuser123"
    password = "pytestpassword123"

    # 1. Test for: Registering a new user
    assert user_manager.register_user(username, password) == True

    # 2. Test for: Check if the user exists (after new user account registration)
    assert user_manager.is_existing_user(username) == True

    # 3. Test for: Retrieving user account username
    user_account = user_manager.get_user_account(username)
    assert user_account.username == username

    # 4. Test for: Authenticating the user with correct login credentials (correct username and password)
    assert user_manager.authenticate_user(user_account, password) is not None

    # 5. Test for: Fail the authentication when the wrong password is entered (wrong password should fail)
    assert user_manager.authenticate_user(user_account, "wrongpass") is None
