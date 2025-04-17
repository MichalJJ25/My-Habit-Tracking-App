# MJ Habit-Tracker App

A simple (but effective) habit tracker application to help you build and maintain positive or necessary habits. 
Allows you to track your daily, weekly, or monthly habits, see your streaks and/or when you missed doing your habits.

---

## Table of Contents
1. [Features](#features)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Database Setup](#database-setup)
5. [Running the App](#running-the-app)
6. [Testing](#testing)
7. [License](#license)
8. [Acknowledgement](#acknowledgement)

---

## Features
- **Add Habits**: Create new habits with a name and frequency (daily, weekly or monthly), or choose from 5 predefined habits.
- **Mark Habits as Done**: Enter your completions to track your progress.
- **View Statistics**: Analyse (current and longest) streaks and your missed habits.
- **Persistent Data**: Habits and completions are saved in an SQLite database.
- **Command Line Interface (CLI)**: Simple, but easy-to-use menu for managing habits.

---

## Installation

### Prerequisites
- Python 3.x
- `sqlite3` (usually included in Python 3.x-versions)

### Steps

Either put all the files into a new project, using a python-specific integrated development environment like e.g. "PyCharm", or

1. **Clone the Repository**:
   ```bash
   git clone [https://github.com/MichalJJ25/My-Habit-Tracking-App]
   cd My-Habit-Tracking-App
   ```

2. **Set Up a Virtual Environment (optional)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   - This project only uses Python's standard library, so no additional installations should be required.

---

## Database Setup
The app uses an SQLite database to store habits and completions. 
The database is automatically created when you run the app for the first time.

- **Database File**: `habits.db` (created in the project directory).
- **Tables**:
  - `habits`: Stores habit details (name, frequency and start date).
  - `completions`: Stores completions (as a number) and completion dates for each habit.

---

## Running the App

Either start the main.py through the start-button of your IDE, or through command lines :

1. Navigate to the project directory:
   ```bash
   cd My-Habit-Tracking-App
   ```

2. Run the app:
   ```bash
   python Main.py
   ```

Then follow the CLI menu to:
   - Add habits.
   - Mark habits as done.
   - View statistics.
   - Remove habits.

---

## Usage
### Adding a Habit
1. Select **Add a new habit** from the menu.
2. Choose a predefined habit or enter a custom name.
3. Set the frequency (daily, weekly, or monthly).

### Marking a Habit as Done
1. Select **Mark habit as done** from the menu.
2. Choose the habit you want to mark as completed (either by name or number).

### Viewing Statistics
1. Select **View statistics** from the menu.
2. See your current streak, longest streak, and missed habits for each habit.

---

## Testing
The app includes unit tests to ensure functionality. To run the tests:

1. Navigate to the project directory.
2. Run the test suite:
   ```bash
   python -m unittest discover
   ```

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments
- Thanks to the people behind [Python](https://www.python.org/) for creating the programming language used.
- Also thanks to [JetBrains] for developing the IDE "PyCharm" (https://www.jetbrains.com/pycharm/), which I used for this project.
- Inspired by the need to finish a certificate and learn to code better.

---

### **Key Sections Explained**
1. **Features**: Highlights what your app does.
2. **Installation**: Provides clear steps to set up the app.
3. **Database Setup**: Explains how the database works.
4. **Running the App**: Explains how to start the app.
5. **Usage**: Describes how to use the app’s features.
6. **Testing**: Explains how to run unit tests.
7. **License**: Specifies the license for your project.
8. **Acknowledgments**: Adds a personal touch.

