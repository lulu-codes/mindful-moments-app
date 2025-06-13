<!-- Setup Guide -->

# Setup Guide

### Table of Contents
* [Requirements](#requirements)
* [Installation Guide](#installation-guide)
* [User Guide to use Mindful Moments App](#user-guide-to-use-mindful-moments-app)
* [Application Flow & Functionality Features](#application-flow--functionality-features)
    * [Launch App](#launch-app-main-entry-point)
    * [Welcome Menu](#welcome-menu)
    * [Login](#login)
    * [Create New User Account](#create-new-user-account)
    * [Exit App](#exit-app)
    * [Journal Entry Flow](#journal-entry-flow)
* [Back to README file](README.md)

---

## Requirements
* **Python version** - 3.10 or later (Recommended version 3.13.3)
* **Command Line terminal** - Linux Shell, Windows PowerShell or macOS Terminal
* **pip** - Python package installer
* **Internet** - To download and install dependencies

---

## Installation Guide

1. Clone or download the repository to your local machine:
    ```bash
    git clone https://github.com/lulu-codes/mindful-moments-app.git
    cd mindful-moments
    ```
2. Create and activate a virtual environment (recommended)
    * On Windows:
    ```powershell
    python -m venv .venv
    .\.venv\Scripts\activate
    ```
    * On Linux or macOS:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
3. Install the required Python packages and dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Run the application:
    ```bash
    python main.py
    ```
    NOTE: Main entry app point is through `main.py` to be able to access `journal.py` as required to save and load user's account data and entries.

---

## User Guide to use Mindful Moments App
1. **Install Dependencies** - Ensure that the dependencies have been installed as per [Installation Guide](#installation-guide.
2. **Launch the app** by running the main script:  
    ```bash
    python main.py
    ```
3. **Navigate the Welcome Menu** to either log in (existing users) or create a new user account (new users)
4. **Navigate the Journal Menu (after successful login)** Log or view journal entries for mood and reflection entries
5. **Logout & Exit App** After saving and finished with journal entries, log out and exit app.

---

## Application Flow & Functionality Features

### Launch App (Main Entry Point)

```
        MAIN APP START POINT
                    └── Display Welcome Banner (ASCII art) → Press CTRL + C to continue
                        └── Launch/Run app
```

| Functionality Features | Function |
| -------------------- | --------- |
| Run program in main.py file | `if __name__ == "__main__":` |
| App's welcome banner, use of `rich-pyfiglet` module to enhance visual UI | `display_welcome_banner()` |
| Launches the start of main app | `run_app()` |

---

### Welcome Menu

```
        Infinite Loop:
            └── Display Welcome Menu Options
                └── Prompt user to select an option from Welcome Menu Options [1-3]:
                        [1] Login
                        [2] Create an Account
                        [3] Exit App
                    └── Validates user selection → Calls selected menu option
```

| Functionality Features | Purpose |
| -------------------- | --------- |
| Dictionary-based menu | Welcome Menu Options uses a dictionary to show numbered menu options and menu descriptions |
| Validation Loop | Ensures the user enters a valid menu option, otherwise prompts again |
| Action Routing | Once menu option selected and validated → Calls `login()`, `create_new_account()` or `exit_app()` |

---

### Login
```
        Option [1] User chooses to "Login"
                └── Prompt for username & password
                    └── Check if username exists
                        ├── No → Show error + suggest creating account
                        └── Yes → Verify password
                            ├── Incorrect → Retry prompt
                            └── Correct → Load Journal App
```

| Functionality Features | Functions |
| -------------------- | --------- |
| Load stored user accounts | `UserManager.load_json_file(USER_ACCOUNTS_JSON_FILE)` |
| Check if user exists | `UserManager.is_existing_user(username)` |
| Verify password using bcrypt | `UserAccount.verify_password(password)` |
| Login flow logic | `login()` |
| Launch journal menu | `run_journal()` |

---

### Create New User Account
```
        Option [2] User chooses "Create New User Account"
                └── Prompt for new username
                    └── Check if username exists
                        ├── If Username is taken → Asks again for new username
                        └── If Username available → Prompt to create password + confirm
                            ├── If Passwords do not match → Ask again, prompt to create password + confirm
                            └── If Passwords match → Hash password and save user
                                        └── Confirm User Account created successfully + redirect to Login
```

| Functionality Features | Functions |
| -------------------- | --------- |
| Check if username already exists | `UserManager.is_existing_user(username)` |
| Validates password & confirmation | |
| Hash the password | `UserManager.create_password_hash()` |
| Create new UserAccount instance | `UserAccount(username, hashed_password)` |
| Add new user to file | `UserManager.add_user(account: UserAccount)` |
| Calls to Save updated data | `BaseDataManager.save_json_file()` |
| Handle logic & user input | `create_new_account()` |
| Calls to Login once UserAccount created successfuly | `login()` |

---

### Exit App
```
        Option [3] User chooses "Exit App"
                └── Exits and closes application
```

| Functionalities Used | Functions |
| -------------------- | --------- |
| Calls function to safely close and exit app | `sys.exit(0)` |

---

### JOURNAL ENTRY FLOW

```
(Once User successfully logs in)
            └── Load Journal Menu
                ├── Option [1] Create New Journal Entry
                │       └── Prompt user for daily reflection on:
                │             ├─ Mood rating
                │             ├─ Random choice of 'encouragement quote' returned based on mood rating category
                │             ├─ Wins of the day
                │             ├─ Challenges of the day
                │             ├─ Gratitude entry
                │             └─ Random choice of motivational quote to close out journal entry
                │       └── Creates JournalEntry instance and saves entry to user's username in journal file
                │       └── Confirmation message of journal entry saved
                │
                ├── Option [2] View Past Entries
                │       └── Load journal file
                │       └── Display list of entries
                │             └── Options:
                │                   ├─ View full entry
                │                   └─ Return to menu
                │
                ├── Option [3] Logout App
                        └── Save any changes if needed
                        └── Return to Login Menu
                        └── Select another Menu option or Exit App once done
```
