"""This class is testing the CLI-input, using "mock"-inputs to simulate a user's entries"""
import unittest
from unittest.mock import patch
from io import StringIO
from Habit import Habit
from User import User
from Database import Database
from Analytics import Analytics
from CLI import CLI

class TestCLI(unittest.TestCase):
    def setUp(self):
        """Setting up test environment, creating a user, a database, loading the analytics-class
        and using them as CLI-constructor-inputs"""
        self.user = User("test_user")
        self.db = Database(":memory:")  # Use in-memory database for testing
        self.analytics = Analytics(self.user.habits)
        self.cli = CLI(self.user, self.db, self.analytics)

    def tearDown(self):
        """Cleaning up after each test."""
        del self.user
        del self.db
        del self.analytics
        del self.cli

    # The "patches" are mocking real input into the CLI.
    # In this case, after starting the app, you first choose "1", which is adding a habit,
    # then you type in the habit-name and the frequency, and then you exit the CLI with "7"
    @patch('builtins.input', side_effect = ["1", "Exercise", "daily", "7"])  # Simulating the user input
    # sys.stdout is the standard output stream, capturing the results as strings
    @patch('sys.stdout', new_callable = StringIO)  # Capturing the output
    def test_add_habit(self, mock_stdout, mock_input):
        """Testing adding a habit via CLI."""
        # Simulates the user typing in the commands
        self.cli.input_command()
        # and this is capturing the output from the input
        output = mock_stdout.getvalue()
        # Comparing the expected result (or string in this case) to the actual result/string
        self.assertIn("Habit 'Exercise' added successfully !", output)
        # Testing the amount of habits in the user-habits-list, should be 1
        self.assertEqual( 1, len(self.user.habits))

    # Adding and removing a habit
    @patch('builtins.input', side_effect=["1", "Exercise", "daily", "2", "1", "y", "7"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_remove_habit(self, mock_stdout, mock_input):
        """Testing the removal of a habit via CLI."""
        self.cli.input_command()
        output = mock_stdout.getvalue()
        self.assertIn("Habit 'Exercise' removed successfully !", output)
        self.assertEqual(0, len(self.user.habits))

    # Adding and marking a habit as done
    @patch('builtins.input', side_effect=["1", "Exercise", "daily", "3", "1", "7"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_mark_habit_done(self, mock_stdout, mock_input):
        """Testing the marking of a habit as done via the CLI."""
        self.cli.input_command()
        output = mock_stdout.getvalue()
        self.assertIn("Habit 'Exercise' marked as done !", output)
        # Comparing the expected result (1) to the completed dates from the habit with the index "0" in the list
        self.assertEqual( 1, len(self.user.habits[0].completed_dates))

    # Adding a habit and viewing the statistics
    @patch('builtins.input', side_effect=["1", "Exercise", "daily", "4", "1", "7"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_view_statistics(self, mock_stdout, mock_input):
        """Testing viewing the general statistics via CLI."""
        self.cli.input_command()
        output = mock_stdout.getvalue()
        self.assertIn("=== Habit Statistics ===", output)
        self.assertIn("Habit : Exercise", output)

    # Adding 2 habits and listing all habits
    @patch('builtins.input', side_effect=["1", "Exercise", "daily", "1", "Take a break", "daily", "5", "7"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_list_all_habits(self, mock_stdout, mock_input):
        """Testing listing all habits via CLI."""
        self.cli.input_command()
        output = mock_stdout.getvalue()
        self.assertIn("Current Habits :", output)
        self.assertIn("1. Exercise\n2. Take a break", output)

if __name__ == "__main__":
    unittest.main()