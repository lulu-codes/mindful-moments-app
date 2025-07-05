# Testing Requirements Reference

This document outlines the key tests completed for the functions and methods in project modules using a combination of manual testing, unit testing, functional testing, integration testing and end-to-end testing.

These tests ensure that core logic flows and user related authentication, account login, journal entries and data storage are functioning correctly.

## Testing Tools Used

* [pytest](https://docs.pytest.org/en/stable/getting-started.html).
* Reference: [Real Python Pytest Tutorial](https://realpython.com/pytest-python-testing/)

## Test File: `test_user_auth.py`

| Test Function/Method | Testing Purpose | Testing For | Type of Testing | Test Status |
|----------------------|-----------------|-------------|-----------------|-------------|
| `register_user()` | Core logic for adding new users | - Registers new user <br> - Saves to JSON file correctly | Unit Testing | PASSED |
| `is_existing_user()` | Check if a user is in stored data | - Returns True for existing user <br> - Returns False if user not found | Type of Testing | Test Status |
| `get_user_account()` | Retrieves user data from JSON file | - Returns UserAccount instance by username if exists - Raises error if user's username not found | Type of Testing | Test Status |
| `add_user_account()` | Check if a user is in stored data | - Returns True for existing user <br> - Returns False if user not found | Type of Testing | Test Status |
| `authenticate_user()` | Check login authentication logic |     | Type of Testing | Test Status |
| `UserAccount.verify_password()` | Verifies passwords match with `bcrypt` logic |- Returns True for correct matching password <br> - Returns false for wrong password | Type of Testing | Test Status |
| `hash_password()` | Bcrpt logic | Checks password is securely hashed | - Password not stored as original plain password <br> - Stored hash password is a valid string | Type of Testing | Test Status |


## Test File: `test_user_accounts.json`

test_json_path = tmp_path / "test_user_accounts.json"
test_json_path.write_text("{}")

Init UserManager with this test file
user_manager = UserManager(test_json_path)

| Test Function/Method | Testing Purpose | Testing For | Type of Testing | Test Status |
|----------------------|-----------------|-------------|-----------------|-------------|
| `load_json_file()` | Checks data loaded succesfully | Testing Purpose | | Type of Testing | Test Status |
| `save_json_file()` | Checks data stored succesfully | Testing Purpose | | Type of Testing | Test Status |
---

## Test File: `test_main.py`

| Test Function/Method | Testing Purpose | Testing For | Type of Testing | Test Status |
|-----------|----------------------|-----------------|-----------------|-------------|
| `test_main.py` | Test Function/Method | Testing Purpose | Type of Testing | Test Status |


## Test File: `test_helpers.py`

| Test Function/Method | Testing Purpose | Testing For | Type of Testing | Test Status |
|-----------|----------------------|-----------------|-----------------|-------------|
| `test_helpers.py` | Test Function/Method | Testing Purpose | Type of Testing | Test Status |


## Test File: `test_journal.py`

| Test Function/Method | Testing Purpose | Testing For | Type of Testing | Test Status |
|-----------|----------------------|-----------------|-----------------|-------------|
| `test_journal.py` | Test Function/Method | Testing Purpose | Type of Testing | Test Status |


## Test File: `test_journal_models.py`

| Test Function/Method | Testing Purpose | Testing For | Type of Testing | Test Status |
|-----------|----------------------|-----------------|-----------------|-------------|
| `test_journal_models.py` | Test Function/Method | Testing Purpose | Type of Testing | Test Status |

## Test File: `test_journal_entries.json`

| Test Function/Method | Testing Purpose | Testing For | Type of Testing | Test Status |
|-----------|----------------------|-----------------|-----------------|-------------|
| `test_journal_entries.json` | Test Function/Method | Testing Purpose | Type of Testing | Test Status |

| Test Function/Method | Testing Purpose | Testing For | Type of Testing | Test Status |
|-----------|----------------------|-----------------|-----------------|-------------|
| `test_file_paths.py` | Test Function/Method | Testing Purpose | Type of Testing | Test Status |
| `exception_classes.py` | Test Function/Method | Testing Purpose | Type of Testing | Test Status |
| `quotes.py` | Test Function/Method | Testing Purpose | Type of Testing | Test Status |
