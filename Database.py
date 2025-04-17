import sqlite3 # SQLite database library, to connect and manage databases
import datetime # library to handle dates and times

# "Database" class, to manage and store data related to the habits
class Database :
    # Constructor to initialize a database object, database name chosen is optional
    def __init__(self, db_name = "habit_tracker.db") :
        self.connection = sqlite3.connect(db_name) # Connect to the database (or create one)
        self.cursor = self.connection.cursor() # Creates a "cursor" object, to be able to execute SQL commands
        self._create_tables() # Method to create necessary tables

    # Method to create the required tables for storing habit data
    def _create_tables(self) :
        # SQL statement, creates a "habits" table to store habit information
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS habits (
                                id INTEGER PRIMARY KEY,
                                name TEXT,
                                frequency TEXT,
                                start_date TEXT)''')
        # SQL statement, creates a "completion" table to record completions
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS completions (
                                habit_id INTEGER,
                                completion_date TEXT,
                                FOREIGN KEY (habit_id) REFERENCES habits (id))''')
        # Commit changes to the database to save the table creation
        self.connection.commit()

    def convert_to_date(self, date_str) :
        """Convert string date to datetime.date object."""
        try :
            return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        except (ValueError, TypeError) :
            print(f"Warning : Invalid date format : {date_str}")
            return datetime.date.today()

    def save_habit(self, habit) :
        """Save a habit to the database, making sure that the date is in the correct format"""
        start_date = habit.start_date
        if isinstance(start_date, datetime.date) :
            start_date = start_date.strftime('%Y-%m_%d')
        self.cursor.execute("INSERT INTO habits (name, frequency, start_date) VALUES (?, ?, ?)",
                            (habit.name, habit.frequency, start_date))
        self.connection.commit()

    def load_habit(self) :
        """Load all habits from the database."""
        self.cursor.execute("SELECT * FROM habits")
        # This returns a list of so called "tuples", 1 tuple per row, habit_id being assigned row[0]
        rows = self.cursor.fetchall()
        habits = []
        for row in rows :
            from Habit import Habit
            # convert start_date string to datetime.date
            start_date = self.convert_to_date(row[3])
            habit = Habit(name = row[1], frequency = row[2], start_date = start_date)
            # Load and convert completion dates
            self.cursor.execute("SELECT completion_date FROM completions WHERE habit_id = ?",
                                (row[0],))
            completion_dates = [self.convert_to_date(date[0]) for date in self.cursor.fetchall()]
            habit.completed_dates = completion_dates
            habits.append(habit)
        return habits

    def save_completion(self, habit, date) :
        """Saving a habit completion."""
        if isinstance(date, datetime.date) :
            date = date.strftime('%Y-%m-%d')
        try :
            self.cursor.execute("SELECT id FROM habits WHERE name = ?", (habit.name,))
            # unlike fetchall, fetchone is only loading 1 habit/tuple (with habit_id, name, frequency and start_date), not all of them
            result = self.cursor.fetchone()
            if result is None :
                print(f"Error : Habit '{habit.name}' not found in the database")
                return False
            habit_id = result[0] # accessing the first element of the tuple
            self.cursor.execute("INSERT INTO completions (habit_id, completion_date) VALUES (?, ?)",
                                (habit_id, date))
            self.connection.commit()
            print(f"Completion for habit '{habit.name}' saved on {date}")
            return True
        except sqlite3.Error as e :
            print(f"Database error : {e}")
            return False


    def get_completions(self, habit, date) :
        """Fetching completions for a given habit."""
        self.cursor.execute("""
            SELECT completion_date 
            FROM completions 
            WHERE habit_id = (SELECT id FROM habits WHERE name = ?)""", (habit.name,))
        return [self.convert_to_date(row[0]) for row in self.cursor.fetchall()]

    def delete_habit(self, habit_name) :
        """Delete a habit from the database, including its completions."""
        # Delete completions related to the habit first
        try :
            self.cursor.execute("SELECT id FROM habits WHERE name = ?",(habit_name,))
            result = self.cursor.fetchone()
            if result is None :
                print(f"Habit '{habit_name}' not found in database !")
                return False
            habit_id = result[0]
            self.cursor.execute("DELETE FROM completions WHERE habit_id = ?", (habit_id,))
            # Then delete the habit itself
            self.cursor.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
            self.connection.commit()
            return True
        except sqlite3.Error as e :
            print(f"Database error : {e}")
            return False