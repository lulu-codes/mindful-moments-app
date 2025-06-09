# DEV1001 T1A2 - Programming Project: "Mindful Moments" App

### Table of Contents
* [Project Overview](#project-overview)
    * [Key Concepts Demonstrated in Project](#key-concepts-demonstrated-in-this-project-include)
* [Purpose of "Mindful Moments" App](#purpose-of-mindful-moments-app)
* [Features of "Mindful Moments" App](#features-of-mindful-moments-app)
* [Setup & Requirements](#setup-and-requirements)
* [Third-Party Libraries - Software Licensing & Security](#third-party-libraries---software-licensing--security)
* [Tech Stack Used](#tech-stack-used)
* [References & Resources](#references-and-resources-used)

## Project Overview

This is my individual programming project to demonstrate my skills as a Student Developer to design and build a functional command-line interface (CLI) application using the Python programming language.

The application showcases my abilities and skills to develop and implement the use of key programming principles, structures and apply appropriate use of code styles and conventions.

### Key concepts demonstrated in this project include

- Writing and using functions and classes
- Applying of Python language features including appropriate use of syntax and structures
- Handling of inputs and outputs for a functional user experience
- Applying DRY coding coding principles and use of reusable functions
- Approporiate use of code styles and conventions in Python [PEP 8](https://peps.python.org/pep-0008/)
- Documentation including user help guide and instructions on how to use application
- Implementing control structures to manage control flow
- Applying error handling to manage exceptions and errors
- Using third-party libraries and use of modules and functions
- Using file handling, including reading and writing files/data to JSON

##
Mindful Moments" App

The **"Mindful Moments"** CLI app is designed to help users track their daily emotional-wellbeing through mood ratings and journal reflections. It allow users to log and view their journal entries about "Mindful Moments" to encourage personal reflections on their daily mood and wins and challenges of the day.

The app will include user input prompts and allow users to create simple journal entries based off these prompts.
Over time, the app will capture a history of data files to provide a text-based mood trend summary and allow users to identify emotional patterns to promote self-awareness, self-reflection and support the practice of mindfulness well-being.

## Features of "Mindful Moments" App

- **Main menu** - User input and output to handle navigating the terminal interface
- **Secure Access** - Password-protected journal to keep reflections private
- **Mood Logging** - Users selects a mood rating from predefined options represented with descriptive text/emojis for quick and intuitive input
- **Daily Reflections** - Users are prompted with input to enter wins and challenges for the day to promote self-reflection and mindfulness.
- **Gratitude Entry** _(Optional)_ - A quick prompt for “one thing you are grateful for today” aimed to cultivate a positive and grateful mindset
- **Mood Trends Summary** - A text-based display of recent mood history with counts of mood occurrences and simple insights (e.g., “In the last week, you've mostly had positive moods!”).
- **Random Affirmations** - After entries, users receive a motivational affirmation quote randomly selected from a built-in list (OR EXTERNAL LIBRARY - need to find) to help enhance user experience and engagement.

## Setup and Requirements
* [README](README.md)
* [Setup Guide](setup_guide.md)
* Add "installation guide" including instructions describing steps to install the application and dependencies required.
* Setup & Installation Requirements

## Third-Party Libraries - Software Licensing & Security

- A list of most third-party software used by project
- Third-party software purpose and Licences (no conflicted licences)
- Security impact of third-party software
- Licence ethical/non-ethical info

This application project uses the following third-party Python libraries.
The combination of the following libraries and tools were used to enhance the application's functionality, security and user experience in the "Mindful Moments" app:

### Main Libraries Used

| Library | Purpose | Licence Type | Security & Ethical Considerations  |
|---------|---------|--------------|------------------------------------|
| [`json`](https://docs.python.org/3/library/json.html) | Read/write and store structured journal data | Built-in | Used to support consistent and readable structured data storage. No security or ethical concerns. |
| [`pathlib`](https://docs.python.org/3/library/pathlib.html) | File system path handling | Built-in | Used to manage file path navigation. No security or ethical concerns.|
| [`datetime`](https://docs.python.org/3/library/datetime.html)| Log and track timestamps on journal entries | Built-in | Used securely to log timestamp. |
| [`random`](https://docs.python.org/3/library/random.html) | Randomly selects motivational affirmations to promote positive user engagement | Built-in | Used only for random selection - to choose and display motivational affiramtions. Content is appropriate and consists of positive quotes. |
| [`bcrypt`](https://pypi.org/project/bcrypt/) | Secure password protection to keep journal access private | Apache Licence | Used for the user account login feature to strengthen security by hashing passwords with random salt instead of storing passwords as plain text. Chose to use 'bcrypt' library over 'getpass' for enhanced password protection. |
| [`rich`](https://rich.readthedocs.io/en/stable/#)| Add colour to terminal UI with styled text and enhance visual insights | MIT Licence | Open source and widely trusted library however relies on dependencies so need to ensure that library is up to date to avoid any potential vulnerabilities |
| [`rich-pyfiglet`](https://pypi.org/project/rich-pyfiglet/) | Add decorative ASCII art fonts integrated with `rich` library to enhance CLI aesthetics | MIT Licence | Appropriate use of selected styled ASCII art, it will also be checked to avoid inappropriate characters that may cause errors. No security or ethical concerns. |
| [`tabulate`](https://pypi.org/project/tabulate/) | (Use for nice to have feature for mood trend summary) Provides a table format display to visualise data (e.g. mood trends summary) or journal entries table. | MIT Licence | This library will mainly be used for enhancing visual display for navigation menu and displaying mood trends summary. |

<br>

### Dependency Libraries for Main Libraries Used

| Library | Purpose | Licence Type |
|---------|---------|--------------|
| `Pygments` | Dependency of `rich` used for syntax highlighting when rendering formatted text in CLI. | BSD Licence |
| `markdown-it-py` | Dependency of `rich` to enable rendering of Markdown formatted text (eg. for headings and lists) in the CLI. | MIT Licence |
| `mdurl` | Sub-dependency of `markdown-it-py` specifically used to parse and validate URLs in Markdown content. | MIT Licence |
| `click` | Dependency of `rich-pyfiglet` used for creating CLI commands and options. | BSD Licence |


### License Versions

Each library is open-source and Licenced to allow for educational and personal use under their respective Licences.
I acknowledge and respect the work of the open-source community in making these tools available.
For more details on each Licence, please visit the respective project pages on [PyPI](https://pypi.org/) or via their official repositories.

## Tech Stack Used

- **Markdown** - Documentation for [README](README.md) and [User Guide](user_guide.md)
- **Python** _(version 3.13.3)_ - Python programming language version
- **Visual Studio Code** - Development environment for code, use of terminal line and console output for debugging
- **GitHub** - Git version control

## References and Resources Used

* [PEP 8](https://peps.python.org/pep-0008/) - For following Python styles and conventions

* [Exceptions](https://docs.python.org/3/library/exceptions.html#) - For handling exceptions

* [Emoji](https://unicode.org/emoji/charts/full-emoji-list.html) (Most CLI-safe. Raw Unicode and official reference) - <br>
    Used to add expressive Emoji characters to convey mood rating tracking to enhance UI visual in CLI interface. As these Emojis are supported natively by [Unicode](https://cldr.unicode.org/#TOC-What-is-CLDR-), I used this directly as strings and assigned to relevant variables for reuse. I avoided adding external dependencies to keep project lightweight and more simple to maintain. Other considerations taken into account was that when saving to JSON, the files wouldn't require special processing to convert between reading/writing to files.

* [Geeksforgeeks](https://www.geeksforgeeks.org/hashing-passwords-in-python-with-bcrypt/) - Support guide with using bcrypt to hash passwords with bcrypt


