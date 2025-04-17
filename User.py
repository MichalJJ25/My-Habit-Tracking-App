"""This class represents a user, with a username and habits."""
class User :

    def __init__(self, username) :
        """Constructor to initialize a "user", "self" is referencing that "user"."""
        self.username = username # sets the username
        self.habits = [] # an empty list to store habits or habit objects

    def add_habit(self, habit) :
        """Method to add a new habit to the user's habit list."""
        self.habits.append(habit) # adds (or appends) a new habit to the habit list

    def remove_habit(self, habit_name) :
        """Method to remove a habit from the user's habit list, using the habit name."""
        # List comprehension, creating a new list filtering out the named habit
        self.habits = [habit for habit in self.habits if habit.name != habit_name]


    def get_habit_by_name(self, name) :
        """Method to find a habit by its name, using a for-loop."""
        for habit in self.habits :
            if habit.name == name :
                return habit
        return None # If habit is not found