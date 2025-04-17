"""This class is testing a variety of methods from other classes,
mainly the analytics-class and database-class"""
import unittest
import datetime
from Habit import Habit
from User import User
from Analytics import Analytics
from Database import Database

class TestHabitTracker(unittest.TestCase) :
    def setUp(self):
        """Set up test fixtures.
        2 daily habits, 2 weekly habits and 1 monthly habit.
        A user, a database and loading analytics"""
        self.habit_daily = Habit("Exercise", "daily")
        self.habit_daily2 = Habit("Chores", "daily")
        self.habit_weekly = Habit("Plan the week", "weekly")
        self.habit_weekly2 = Habit("Time for your hobby", "weekly")
        self.habit_monthly = Habit("Paying the bills", "monthly")
        self.user = User("test_user")
        self.db = Database(":memory:")  # Use in-memory database for testing
        self.analytics = Analytics(self.user.habits)

    def tearDown(self) :
        """This method cleans up the created data after each individual test."""
        del self.habit_daily
        del self.habit_daily2
        del self.habit_weekly
        del self.habit_weekly2
        del self.habit_monthly
        del self.user
        del self.db
        del self.analytics

    # Test Habit Class
    def test_habit_creation(self) :
        """Testing if a habit is created correctly."""
        self.assertEqual(self.habit_daily.name, "Exercise")
        self.assertEqual(self.habit_daily.frequency, "daily")
        self.assertEqual(self.habit_weekly.name, "Plan the week")
        self.assertEqual(self.habit_weekly.frequency, "weekly")
        self.assertEqual(self.habit_monthly.name, "Paying the bills")
        self.assertEqual(self.habit_monthly.frequency, "monthly")

    def test_mark_habit_as_done(self) :
        """Testing marking a habit as done."""
        today = datetime.date.today()
        self.habit_daily.mark_as_done()
        self.assertIn(today, self.habit_daily.completed_dates)

    # Test Analytics Class
    def test_list_current_habits(self):
        """Testing listing the current habits."""
        self.user.add_habit(self.habit_daily)
        self.user.add_habit(self.habit_daily2)
        self.user.add_habit(self.habit_weekly)
        self.user.add_habit(self.habit_weekly2)
        self.user.add_habit(self.habit_monthly)
        self.assertEqual(["Exercise", "Chores", "Plan the week", "Time for your hobby", "Paying the bills"],
                             self.analytics.list_current_habits())

    def test_list_habits_by_periodicity(self) :
        """Testing listing the habits by periodicity/frequency,
        using the add_habit-method from the user-class"""
        self.user.add_habit(self.habit_daily)
        self.user.add_habit(self.habit_daily2)
        self.user.add_habit(self.habit_weekly)
        self.user.add_habit(self.habit_weekly2)
        self.user.add_habit(self.habit_monthly)
        # comparing the expected value, with the actual value, calling the list_habits_by_periodicity-method from the analytics-class
        self.assertEqual(["Plan the week", "Time for your hobby"], self.analytics.list_habits_by_periodicity("weekly"))

    def test_get_current_daily_streak(self) :
        """Testing streak calculation for a daily habit, expected result should be 4.,
        using the get_current_streak-method from the analytics-class"""
        # Add some completed dates
        self.habit_daily.completed_dates = [
            datetime.date.today() - datetime.timedelta(days = 134),
            datetime.date.today() - datetime.timedelta(days = 133),
            datetime.date.today() - datetime.timedelta(days = 132),
            datetime.date.today() - datetime.timedelta(days = 131),
            datetime.date.today() - datetime.timedelta(days = 130),
            datetime.date.today() - datetime.timedelta(days = 129),
            datetime.date.today() - datetime.timedelta(days = 3),  # current streak started here
            datetime.date.today() - datetime.timedelta(days = 2),
            datetime.date.today() - datetime.timedelta(days = 1),
            datetime.date.today()                                  # and ends here
        ]
        # comparing the expected value, with the actual value, calling the get_current_streak-method from the analytics-class
        self.assertEqual(4, self.analytics.get_current_streak(self.habit_daily))

    def test_get_current_weekly_streak(self) :
        """Testing streak-calculation for a weekly habit, expected result should be 5."""
        self.habit_weekly.completed_dates = [
            datetime.date.today() - datetime.timedelta(days = 280),
            datetime.date.today() - datetime.timedelta(days = 273),
            datetime.date.today() - datetime.timedelta(days = 266),
            datetime.date.today() - datetime.timedelta(days = 259),
            datetime.date.today() - datetime.timedelta(days = 252),
            datetime.date.today() - datetime.timedelta(days = 245),
            datetime.date.today() - datetime.timedelta(days = 28),  # current streak started here
            datetime.date.today() - datetime.timedelta(days = 21),
            datetime.date.today() - datetime.timedelta(days = 14),
            datetime.date.today() - datetime.timedelta(days = 7),
            datetime.date.today()                                   # and ends here
        ]
        # comparing the expected value, with the actual value
        self.assertEqual(5, self.analytics.get_current_streak(self.habit_weekly))

    def test_longest_daily_streak(self) :
        """Testing streak-calculation for a habit, trying to find the longest streak,
        expected result should be 4,
        using the get_longest_streak-method from the analytics-class."""
        self.habit_daily.completed_dates = [ # adding a list with completed dates
            datetime.date.today() - datetime.timedelta(days = 31),
            datetime.date.today() - datetime.timedelta(days = 30),
            datetime.date.today() - datetime.timedelta(days = 29),
            datetime.date.today() - datetime.timedelta(days = 7), # The longest streak starts here
            datetime.date.today() - datetime.timedelta(days = 6),
            datetime.date.today() - datetime.timedelta(days = 5),
            datetime.date.today() - datetime.timedelta(days = 4), # and ends here
            datetime.date.today() - datetime.timedelta(days = 2),
            datetime.date.today() - datetime.timedelta(days = 1),
            datetime.date.today()
        ]
        # Comparing the expected value with the actual value, calling the get_longest_streak()-method from the analytics-class
        self.assertEqual(4, self.analytics.get_longest_streak(self.habit_daily))

    def test_longest_weekly_streak(self) :
        """Testing the longest-streak-calculation for a weekly habit,
        expected result should be 5."""
        self.habit_weekly.completed_dates = [  # adding a list with completed dates
            datetime.date.today() - datetime.timedelta(days = 91),
            datetime.date.today() - datetime.timedelta(days = 84),
            datetime.date.today() - datetime.timedelta(days = 70), # The longest streak starts here
            datetime.date.today() - datetime.timedelta(days = 63),
            datetime.date.today() - datetime.timedelta(days = 56),
            datetime.date.today() - datetime.timedelta(days = 49),
            datetime.date.today() - datetime.timedelta(days = 42), # and ends here
            datetime.date.today() - datetime.timedelta(days = 28),
            datetime.date.today() - datetime.timedelta(days = 14),
            datetime.date.today() - datetime.timedelta(days = 7),
            datetime.date.today()
        ]
        # Comparing the expected value to the actual value
        self.assertEqual(5, self.analytics.get_longest_streak(self.habit_weekly))

    def test_longest_streak_across_all_habits_1(self) :
        """Testing the longest-streak-calculation across all habits, expected result is 6,
        using the get_longest_streak_for_all-method from the analytics-class"""
        self.user.add_habit(self.habit_daily)
        self.user.add_habit(self.habit_daily2)
        self.habit_daily.completed_dates = [
            datetime.date.today() - datetime.timedelta(days = 3),
            datetime.date.today() - datetime.timedelta(days = 2),
            datetime.date.today() - datetime.timedelta(days = 1),
            datetime.date.today()
        ]
        # This is the longer streak
        self.habit_daily2.completed_dates = [
            datetime.date.today() - datetime.timedelta(days = 101),
            datetime.date.today() - datetime.timedelta(days = 100),
            datetime.date.today() - datetime.timedelta(days = 99),
            datetime.date.today() - datetime.timedelta(days = 98),
            datetime.date.today() - datetime.timedelta(days = 97),
            datetime.date.today() - datetime.timedelta(days = 96)
        ]
        longest_streak_habit, longest_streak = self.analytics.get_longest_streak_for_all()
        self.assertEqual(("Chores", 6), (longest_streak_habit.name, longest_streak))

    def test_longest_streak_across_all_habits_2(self) :
        """Testing the longest-streak-calculation across all habits, but with one daily and one weekly habit,
        expected result is 5 (from the weekly habit),
        using the get_longest_streak_for_all-method from the analytics-class"""
        self.user.add_habit(self.habit_daily)
        self.user.add_habit(self.habit_weekly)
        self.habit_daily.completed_dates = [
            datetime.date.today() - datetime.timedelta(days = 5),
            datetime.date.today() - datetime.timedelta(days = 3),
            datetime.date.today() - datetime.timedelta(days = 2),
            datetime.date.today() - datetime.timedelta(days = 1),
            datetime.date.today()
        ]
        self.habit_weekly.completed_dates = [
            datetime.date.today() - datetime.timedelta(days = 56), # the longest streak starts here
            datetime.date.today() - datetime.timedelta(days = 49),
            datetime.date.today() - datetime.timedelta(days = 42),
            datetime.date.today() - datetime.timedelta(days = 35),
            datetime.date.today() - datetime.timedelta(days = 28), # ands ends here
            datetime.date.today() - datetime.timedelta(days = 14),
            datetime.date.today() - datetime.timedelta(days = 7),
            datetime.date.today()
        ]
        longest_streak_habit, longest_streak = self.analytics.get_longest_streak_for_all()
        self.assertEqual(("Plan the week", 5), (longest_streak_habit.name, longest_streak))

    def test_longest_streak_for_specific_habit(self) :
        """Testing the longest-streak-calculation for a specific habit, expected result is 6,
        using the longest_streak_for_specific_habit-method from the analytics-class"""
        self.user.add_habit(self.habit_daily)
        self.user.add_habit(self.habit_daily2)
        self.habit_daily.completed_dates = [
            datetime.date.today() - datetime.timedelta(days = 3),
            datetime.date.today() - datetime.timedelta(days = 2),
            datetime.date.today() - datetime.timedelta(days = 1),
            datetime.date.today()
        ]
        # This should be the longest streak
        self.habit_daily2.completed_dates = [
            datetime.date.today() - datetime.timedelta(days = 5),
            datetime.date.today() - datetime.timedelta(days = 4),
            datetime.date.today() - datetime.timedelta(days = 3),
            datetime.date.today() - datetime.timedelta(days = 2),
            datetime.date.today() - datetime.timedelta(days = 1),
            datetime.date.today()
        ]
        self.assertEqual(6, self.analytics.longest_streak_for_specific_habit(self.habit_daily2.name))

    def test_get_missed_habits_daily(self) :
        """Testing the missed-habits-calculation for a daily habit, started 5 days ago, missed 2 times/twice,
        using the get_missed_habits-method from the analytics-class"""
        self.user.add_habit(self.habit_daily)
        self.habit_daily.start_date = datetime.date.today() - datetime.timedelta(days = 5)
        self.habit_daily.completed_dates = [
            datetime.date.today() - datetime.timedelta(days = 5),
            datetime.date.today() - datetime.timedelta(days = 3),
            datetime.date.today() - datetime.timedelta(days = 1),
            datetime.date.today()
        ]
        self.assertEqual(2, self.analytics.get_missed_habits(self.habit_daily))

    def test_get_missed_habits_weekly(self) :
        """Testing the missed-habits-calculation for a weekly habit, started 7 weeks ago, missed it 3 times,
        using the get_missed_habits-method from the analytics class"""
        self.user.add_habit(self.habit_weekly)
        self.habit_weekly.start_date = datetime.date.today() - datetime.timedelta(days = 49)
        self.habit_weekly.completed_dates = [
            datetime.date.today() - datetime.timedelta(days = 49),
            datetime.date.today() - datetime.timedelta(days = 42),
            datetime.date.today() - datetime.timedelta(days = 14),
            datetime.date.today() - datetime.timedelta(days = 7),
            datetime.date.today()
        ]
        self.assertEqual(3, self.analytics.get_missed_habits(self.habit_weekly))

    def test_get_missed_habits_monthly(self) :
        """Testing the missed-habits-calculation for a monthly habit, started 7 months ago, missed it 3 times,
        again using the get_missed_habits-method from the analytics class"""
        self.user.add_habit(self.habit_monthly)
        self.habit_monthly.start_date = datetime.date.today() - datetime.timedelta(days = 210)
        self.habit_monthly.completed_dates = [
            datetime.date.today() - datetime.timedelta(days = 180), # didn't finish it the first month after adding the habit
            datetime.date.today() - datetime.timedelta(days = 150),
            datetime.date.today() - datetime.timedelta(days = 90),
            datetime.date.today() - datetime.timedelta(days = 60),
            datetime.date.today()
        ]
        self.assertEqual(3, self.analytics.get_missed_habits(self.habit_monthly))

    def test_get_all_missed_habits(self) :
        """Test to try and get all missed dates across daily/weekly/monthly habits,
        missed 2 dates for the 1st daily habit, 3 for the 2nd daily, 1 for the weekly, and 2 for the monthly habit -> 8 overall"""
        self.user.add_habit(self.habit_daily)
        self.user.add_habit(self.habit_daily2)
        self.user.add_habit(self.habit_weekly)
        self.user.add_habit(self.habit_monthly)
        self.habit_daily.start_date = datetime.date.today() - datetime.timedelta(days = 4)
        self.habit_daily.completed_dates = [
            datetime.date.today() - datetime.timedelta(days = 4),
            datetime.date.today() - datetime.timedelta(days = 2),
            datetime.date.today()
        ]
        self.habit_daily2.start_date = datetime.date.today() - datetime.timedelta(days = 8)
        self.habit_daily2.completed_dates = [
            datetime.date.today() - datetime.timedelta(days = 7),
            datetime.date.today() - datetime.timedelta(days = 6),
            datetime.date.today() - datetime.timedelta(days = 5),
            datetime.date.today() - datetime.timedelta(days = 4),
            datetime.date.today() - datetime.timedelta(days = 1),
            datetime.date.today()
        ]
        self.habit_weekly.start_date = datetime.date.today() - datetime.timedelta(days = 35)
        self.habit_weekly.completed_dates = [
            datetime.date.today() - datetime.timedelta(days = 35),
            datetime.date.today() - datetime.timedelta(days = 28),
            datetime.date.today() - datetime.timedelta(days = 14),
            datetime.date.today() - datetime.timedelta(days = 7),
            datetime.date.today()
        ]
        self.habit_monthly.start_date = datetime.date.today() - datetime.timedelta(days = 150)
        self.habit_monthly.completed_dates = [
            datetime.date.today() - datetime.timedelta(days = 150),
            datetime.date.today() - datetime.timedelta(days = 120),
            datetime.date.today() - datetime.timedelta(days = 60),
            datetime.date.today()
        ]
        self.assertEqual(8, self.analytics.get_all_missed_habits())

    # Test User Class
    def test_add_habit_to_user(self) :
        """Testing adding a habit to a user,
        2nd line is checking whether the "habit_daily" has been added to the user's habits"""
        self.user.add_habit(self.habit_daily)
        self.assertIn(self.habit_daily, self.user.habits)

    def test_remove_habit_from_user(self) :
        """Test removing a habit from a user,
        3rd line is checking whether the "habit_daily" has been removed from the user's habits"""
        self.user.add_habit(self.habit_daily)
        self.user.remove_habit("Exercise")
        self.assertNotIn(self.habit_daily, self.user.habits)

    def test_user_statistics(self) :
        """Testing user-statistics-generation,
        using the get_statistics-method from the analytics-class"""
        self.user.add_habit(self.habit_daily)
        self.habit_daily.start_date = datetime.date.today() - datetime.timedelta(days = 5)
        self.habit_daily.completed_dates = [
            datetime.date.today() - datetime.timedelta(days = 5),
            datetime.date.today() - datetime.timedelta(days = 4),
            datetime.date.today() - datetime.timedelta(days = 3),
            datetime.date.today() - datetime.timedelta(days = 1),
            datetime.date.today()
        ]
        stats = self.analytics.get_statistics()
        self.assertIn("Exercise", stats)
        self.assertEqual(2, stats["Exercise"]["current_streak"])
        self.assertEqual(3, stats["Exercise"]["longest_streak"])
        self.assertEqual(1, stats["Exercise"]["missed"])

    # Test Database Class
    def test_save_and_load_habit(self) :
        """Testing the saving and loading a habit from the database,
        using the save_habit- and load_habit-methods from the database-class"""
        self.db.save_habit(self.habit_daily)
        self.db.save_habit(self.habit_weekly)
        self.db.save_habit(self.habit_monthly)
        loaded_habits = self.db.load_habit()
        self.assertEqual(3, len(loaded_habits))
        self.assertEqual(loaded_habits[0].name, "Exercise")
        self.assertEqual(loaded_habits[2].name, "Paying the bills")

    def test_save_completion(self) :
        """Testing the saving of a habit-completion in the database,
        using the save_habit-method from the database-class"""
        self.db.save_habit(self.habit_daily)
        today = datetime.date.today()
        self.assertTrue(self.db.save_completion(self.habit_daily, today))

    def test_delete_habit(self) :
        """Testing the deleting of a habit from the database,
        using the save_habit- and delete_habit-methods from the database-class"""
        self.db.save_habit(self.habit_daily)
        self.assertTrue(self.db.delete_habit("Exercise"))

if __name__ == "__main__":
    unittest.main()