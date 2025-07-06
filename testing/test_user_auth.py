# test_user_auth.py

# PYTEST UNIT TESTING
# Testing functions in user_auth_models.py using Pytest (https://docs.pytest.org/en/stable/getting-started.html)

import sys
import os
from pathlib import Path
import bcrypt
import pytest

# Add the project root to the Python path so we can import from core
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.user_auth_models import UserManager, UserAccount, UserNotFoundError
from core.file_paths import USER_ACCOUNTS_JSON_FILE

def test_register_and_authenticate_user(tmp_path: Path):
    """
    This test function checks if a user can be registered and authenticated successfully.
    tmp_path = Pytest temporary path to test data (isolated from actual app data files when running Pytests)

    Test run for:
    1. Registering a new user
    2. Check if the user exists after new user registration
    3. Retrieve the user account data (username) from JSON
    4. Authenticating the user with correct login credentials (returns UserAccount instance for correct password)
    4a. Checks password directly using verify_password() (returns True for correct password)
    5. Authenticating the user with wrong password (Fails the authentication, returns None for wrong password)
    5a. Checks password directly using verify_password() (returns False for wrong password)
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
    assert user_manager.register_user(username, password)

    # 2. Check if the user exists (after registering user)
    assert user_manager.is_existing_user(username)

    # 3. Retrieving stored user account (object) and confirm username
    user_account = user_manager.get_user_account(username)
    assert user_account.username == username

    # 4. Successful authentication (returns UserAccount if correct password)
    assert user_manager.authenticate_user(user_account, password) is not None

    # 4a. Directly test verify_password() (returns True if correct password)
    assert user_account.verify_password(password)

    # 5. Attempt unsuccessful authentication (returns None if wrong password)
    assert user_manager.authenticate_user(user_account, "wrongpass") is None

    # 5a. Directly test verify_password() for (returns False if wrong password - doesn't match stored hashed pw)
    assert not user_account.verify_password("wrongpass")


def test_add_user_account_directly(tmp_path: Path):
    """
    This test function manually adds a dummy user account by directly calling the add_user_account() method, bypassing register_user().
    This isolates the data saving logic to confirm:

    1. A dummy UserAccount object can be created with a hashed password
    2. add_user_account() stores the user data in the JSON file
    3. The saved data can be reloaded and verified
    4. verify_password() still works correctly with the reloaded dummy user
    """

    # Setup and created a temporary empty test JSON file in temp file path
    test_json_path = tmp_path / "test_user_accounts.json"

    # Creates an empty JSON file for testing
    test_json_path.write_text("{}")

    # Init UserManager with this test file
    user_manager = UserManager(test_json_path)

    # 1. Hash password and create dummy UserAccount instance
    dummy_username = "dummyuser123"
    dummy_password = "dummypassword123"
    hashed = bcrypt.hashpw(dummy_password.encode(), bcrypt.gensalt()).decode()
    dummy_account = UserAccount(dummy_username, hashed)

    # 2. Add dummy UserAccount instance to save to test JSON file (bypasses register_user)
    assert user_manager.add_user_account(dummy_account)

    # 3. Retrieve the dummy user from storage and check username
    stored_account = user_manager.get_user_account(dummy_username)
    assert stored_account.username == dummy_username

    # 4. Check password verification works with the reloaded dummy user
    assert stored_account.verify_password(dummy_password)


def test_register_duplicate_user(tmp_path: Path):
    """
    This test checks that duplicate user registrations are prevented.
    It verifies:
    1. A dummy user can be registered successfully the first time
    2. A second attempt with the same username returns False (registration should fail)
    """

     # Setup and created a temporary empty test JSON file in temp file path
    test_json_path = tmp_path / "test_user_accounts.json"

    # Creates an empty JSON file for testing
    test_json_path.write_text("{}")

    # Init UserManager with this test file
    user_manager = UserManager(test_json_path)

    # Dummy test user
    dummy_username = "dummyduplicate"
    dummy_password = "originalpass"

    # 1. First registration should succeed
    assert user_manager.register_user(dummy_username, dummy_password)

    # 2. Second registration with same username should fail
    assert not user_manager.register_user(dummy_username, "differentpass")
