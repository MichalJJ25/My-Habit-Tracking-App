import datetime

class Habit :
    def __init__(self, name, frequency, start_date = None) :
        """Constructor to initialize a habit, with a name, frequency and a start date."""
        self.name = name
        self.frequency = frequency # e.g., daily, weekly
        # If a start date was entered, it saves this value, if this field stays empty, today's date will automatically be assigned
        self.start_date = start_date if start_date else datetime.date.today()
        self.completed_dates = [] # Store completion dates

    def mark_as_done(self) :
        """Method to mark the habit as done on the current date, and adds the newest date to the "completed dates"-list."""
        today = datetime.date.today()
        self.completed_dates.append(today)

    def get_start_date(self) :
        """Method to return the start date of the habit."""
        return self.start_date

    def print_start_date(self) :
        """Printing the start date of a habit."""
        print(f"Start date of '{self.name}' : {self.start_date}")