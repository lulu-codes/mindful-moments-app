<!-- Setup Guide -->

# Setup Guide

### Table of Contents
* [Requirements](#requirements)
* [User Guide to use Mindful Moments App](#user-guide-to-use-mindful-moments-app)
* [Application Flow & Functionality Features](#application-flow--functionality-features)
    * [Launch App](#launch-app-main-entry-point)
    * [Welcome Menu](#welcome-menu)
    * [Login](#login)
    * [Create New User Account](#create-new-user-account)
    * [Exit App](#exit-app)


## Requirements
- Python version
- Command Line terminal
- 

## User Guide to use Mindful Moments App

<ol>
    <li> Step 1
    <li> Step 2
    <li> Step 3
    <li> Step 4
</ol>


## Help & Support



## Application Flow & Functionality Features

### Launch App (Main Entry Point)

```
        MAIN APP START POINT
                    └── Display Welcome Banner (ASCII art) → Press CTRL + C to continue
                        └── Launch/Run app
```

| Functionality Features | Function |
| -------------------- | --------- |
| Script to run program in main.py file | `if __name__ == "__main__":` |
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
| Load stored user accounts | `UserManager.load_json_file(ACCOUNTS_JSON_FILE)` |
| Check if user exists | `UserManager.user_exists(username)` |
| Verify password using bcrypt | `UserAccount.verify_password(password)` |
| Handle login prompt logic | `login()` |
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
                            └── If Passwords match → Hash password & save to JSON file
                                        └── Confirm User Account created successfully + redirect to Login
```

| Functionality Features | Functions |
| -------------------- | --------- |
| Check if username already exists | `UserManager.user_exists(username)` |
| Validates password & confirmation | |
| Hash the password | `UserManager.create_password_hash()` |
| Create new UserAccount instance | `UserAccount(username, hashed_password)` |
| Add new user to file | `UserManager.add_user(account: UserAccount)` |
| Calls to Save updated data | `BaseDataManager.save_file()` |
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
| Calls function to safely close and exit app | `sys.exit()` |

---