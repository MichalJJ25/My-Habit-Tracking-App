"""This class is initializing the app, connecting all the necessary classes."""
from Database import Database
from User import User
from Analytics import Analytics
from CLI import CLI

def main():

    # Initializing the database and the user
    db = Database("habits.db")
    user = User("default_user")

    # Loading the existing habits from the database, using a for-loop
    saved_habits = db.load_habit()
    for habit in saved_habits:
        user.add_habit(habit)

    # Initializing analytics
    analytics = Analytics(user.habits)

    # Creating and starting CLI
    cli = CLI(user, db, analytics)

    print("Welcome to Habit Tracker!")
    print(f"Loaded {len(saved_habits)} existing habits.")

    # Starting the CLI interface
    cli.input_command()

# Making sure it runs only when executed directly
if __name__ == "__main__":
    main()