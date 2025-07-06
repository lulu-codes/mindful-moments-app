# Testing Requirements Reference

This document outlines the key tests completed across the Mindful Moments project.
Testing included a combination of manual testing, unit tests with pytest, and simulated end-to-end user flows to verify the authentication system, journal features, and data persistence.


## Testing Tools Used

* [pytest](https://docs.pytest.org/en/stable/getting-started.html).
* Reference: [Real Python Pytest Tutorial](https://realpython.com/pytest-python-testing/)

## Test File: `test_user_auth.py` - (unit tests using pytest for user account registration and authentication)

| Test Function/Method | Testing Purpose | Expected Outcome Details | Type of Testing | Test Status |
|----------------------|-----------------|-------------|-----------------|-------------|
| `register_user()` | Create new user accounts | - Registers new user <br> - Saves user data to test JSON file | Unit Testing | PASSED |
| `is_existing_user()` | Check if a user is in stored data | - Returns True for registered user <br> - Returns False if user not found | Unit Testing | PASSED |
| `get_user_account()` | Retrieves user data from JSON file | - Returns UserAccount instance when username exists - Raises UserNotFoundError if user's username not found | Unit Testing | PASSED |
| `add_user_account()` | Add user directly (bypassing registration) | - Manually adds a UserAccount instance with hashed pw <br> - Data is saved and reloads correctly from test JSON | Unit Testing | PASSED |
| `authenticate_user()` | Authenticate login with valid credentials | - Returns UserAccount when password is correct <br> - Returns None if password is incorrect | Unit Testing | PASSED |
| `UserAccount.verify_password()` | Verifies passwords match with `bcrypt` logic |- Returns True if password is correct <br> - Returns false if password is wrong | Unit Testing | PASSED |
| `hash_password()` | Bcrpt logic | Checks password is securely hashed | - Password is hashed (not stored as plain text) <br> - Result is stored hash password is a valid string | Unit Testing | PASSED |


## Test File: `user_accounts.json` - (manual test of JSON loading/saving)

| Function/Method | Testing Purpose | Expected Outcome Details  | Type of Testing | Test Status |
|----------------------|-----------------|-------------|-----------------|-------------|
| `load_json_file()` | Load existing user data | User data loads correctly from JSON during app startup and login | Manual Testing | Passed |
| `save_json_file()` | Save new/updated user data | New user data is saved after registration and journal entry submission | Manual Testing | Passed |


## Test File: `main.py` - (simulated end-to-end app use)

| Function/Logic Flow | Testing Purpose | Expected Outcome Details | Type of Testing | Test Status |
|----------------------|-----------------|-------------|-----------------|-------------|
| Full user login/registration flow via CLI | Ensure user experience works | - Logged in as `usertest` and created journal entries <br> - Partner tested as new user `usertest2` | Manual Testing | PASSED |


## Test File: `journal.py` - (journal entries - add/view)

| Test Function / Method | Testing Purpose | Expected Outcome Details | Type of Testing | Test Status |
|----------------------|-----------------|-------------|-----------------|-------------|
| `add_journal_entry()` | Add new journal entry | - Journal entry saved to JSON file <br> Confirmed contents + timestamp stored correctly in journal_entries.JSON | Manual Testing | PASSED |
| `view_journal_entries()` | View added journal entries | Entries displayed for the correct user only (usertest) | Manual Testing | PASSED |


## Test File: `journal_entries.json` - (data storage confirmation)

| File/Data Storage | Testing Purpose | Expected Outcome Details | Type of Testing | Test Status |
|----------------------|-----------------|-------------|-----------------|-------------|
| JSON journal storage | Verify entries stored correctly | Confirmed entries from CLI stored in JSON file with username tag and correct format | Manual Testing | PASSED |


## Test File: `test_helpers.py`

| Test Function / Method | Testing Purpose | Expected Outcome Details | Type of Testing | Test Status |
|----------------------|-----------------|-------------|-----------------|-------------|
| (To be added)        |                  |                            |                  |              |


## Test File: `test_journal_models.py`

| Test Function / Method | Testing Purpose | Expected Outcome Details | Type of Testing | Test Status |
|----------------------|-----------------|-------------|-----------------|-------------|
| (To be added)        |                  |                            |                  |              |


## Other Modules (e.g. `file_paths.py`, `exception_classes.py`, `quotes.py`)

| Test Function / Method | Testing Purpose | Expected Outcome Details | Type of Testing | Test Status |
|----------------------|-----------------|-------------|-----------------|-------------|
| (To be added)        |                  |                            |                  |              |
