"""This class represents the CLI, the interface the user will interact with,
in order to add/remove habits, mark them as done, and view several types of statistics,
including a general overview"""
import datetime
from Habit import Habit
from Analytics import Analytics

class CLI :
    def __init__(self, user, db, analytics) :
        self.user = user
        self.db = db
        self.analytics = analytics

    def display_menu(self) :
        """Creating the 'welcome'-menu"""
        print("\nHabit Tracker CLI")
        print("1. Add a new habit")
        print("2. Remove a habit")
        print("3. Mark habit as done")
        print("4. View statistics")
        print("5. List all habits")
        print("6. List habits with a specific periodicity (daily/weekly/monthly)")
        print("7. Quit")

    def display_menu_statistics(self):
        """Creating the statistics-menu"""
        print("\nHabit Tracker CLI")
        print("1. General overview")
        print("2. Longest streak for a specific habit")
        print("3. Longest streak across all habits")
        print("4. Total amount of missed dates across all habits")
        print("5. Return to main menu")

    def input_command(self) :
        """Handling the inputs and making sure, the correct method is being used"""
        while True :
            self.display_menu()
            choice = input("Enter choice : ")
            try :
                if choice == "1" :
                    self.add_habit()
                elif choice == "2" :
                    self.remove_habit()
                elif choice == "3" :
                    self.mark_habit_done()
                elif choice == "4" :
                    self.display_menu_statistics()
                    choice_statistics = input("Enter choice (number) : ")
                    if choice_statistics == "1" :
                        self.view_statistics()
                    elif choice_statistics == "2" :
                        self.view_longest_streak_for_specific_habit()
                    elif choice_statistics == "3" :
                        self.view_longest_streak_across_all_habits()
                    elif choice_statistics == "4" :
                        self.view_total_amount_of_missed_habits()
                    elif choice_statistics == "5" :
                        print("\nReturning to main menu")
                    else :
                        print("Invalid choice, try again !")
                elif choice == "5" :
                    self.list_all_habits()
                elif choice == "6" :
                    self.view_habits_with_same_periodicity()
                elif choice == "7" :
                    print("Have a great day !")
                    break
                else :
                    print("Invalid choice, try again !")
            except Exception as e :
                print(f"An error occurred : {str(e)} \nPlease try again.")

    def add_habit(self) :
        """Adding a habit through the CLI, can choose from predefined habits,
        either by typing the assigned number of the habit or by typing the name,
        but can also add an entirely new habit,
        and in either case choosing between the frequencies daily, weekly and monthly.
        Using the add_habit-method from the user-class,
        and using the save_habit-method from the database-class"""
        habit_daily1 = Habit("Exercise", "daily")
        habit_daily2 = Habit("Chores", "daily")
        habit_weekly1 = Habit("Plan the week", "weekly")
        habit_weekly2 = Habit("Time for your hobby", "weekly")
        habit_monthly1 = Habit("Paying the bills", "monthly")
        predefined_habits = [habit_daily1, habit_daily2, habit_weekly1, habit_weekly2, habit_monthly1]
        # Show predefined habits
        print("\nPredefined habits : ")
        for i, habit in enumerate(predefined_habits, 1) :
            print(f"{i}. {habit.name} ({habit.frequency})")
        # Asking whether the User wants to choose a predefined habit or add a new one, and assign it to a variable
        choice = input("You can choose a habit from the list (type in number),\nor enter your own habit : ")
        # If the user selects a predefined habit, it will automatically assign the frequency
        # If a number has been typed, it will check whether a number like this exists
        if choice.isdigit() :
            choice_num = int(choice)
            if 1 <= choice_num <= len(predefined_habits) :
                habit = predefined_habits[choice_num - 1]
            else :
                print("There is no predefined habit with this number.")
                return
        # if there isn't a number given, it will check whether the field is empty,
        # and when it's not, ask about the frequency, and also check whether it's a valid frequency
        else :
            name = choice
            if not name :
                print("Habit name cannot be empty ! :P")
                return
            while True:
                frequency = input("Enter frequency (daily/weekly/monthly) : ").strip().lower()
                if frequency in ['daily', 'weekly', 'monthly']:
                    break
                else:
                    print("Invalid choice, please choose daily, weekly or monthly.")
            habit = Habit(name, frequency)
        # Checking if the habit already exists in the user-habits-list
        if any(h.name == habit for h in self.user.habits) :
            print(f"A habit with name '{habit}' already exists !")
            return
        # adding the habit to the user-list, and to the database
        self.user.add_habit(habit)
        self.db.save_habit(habit)
        print(f"Habit '{habit.name}' added successfully !")

    def remove_habit(self) :
        """Method to remove a habit, from both the database and the habits-list,
        using the remove_habit-method from the user-class,
        and the delete_habit-method from the database-class"""
        # Check whether there are actually habits which can be removed
        if not self.user.habits :
            print("Sorry, no habits to remove !")
            return
        # Show a numbered list of the current habits
        print("\nCurrent habits :")
        for index, habit in enumerate(self.user.habits, 1) :
            print(f"{index}. {habit.name}")
        choice = input("\nEnter habit number or name to remove : ")
        # Handling both a numeric and a text input
        habit_name = None
        if choice.isdigit() :
            choice_num = int(choice)
            if 1 <= choice_num <= len(self.user.habits) :
                habit_name = self.user.habits[choice_num - 1].name
        else :
            habit_name = choice
        # Checking whether there is (or rather isn't) a habit name,
        # and whether it can (or rather can not) be found in the habits-list
        if not habit_name or not any(h.name == habit_name for h in self.user.habits) :
            print(f"Habit not found.")
            return
        # Checking whether the user really wants to delete the habit
        confirm = input(f"Are you sure you want to remove '{habit_name}' ?"
                        f" (y/n) : ").lower()
        # I could also write "confirm == 'n'", but this way,
        # any input that isn't a 'y', is going to lead to a cancellation
        if confirm != 'y' :
            print("Habit removal cancelled.")
            return
        if self.db.delete_habit(habit_name) :
            self.user.remove_habit(habit_name)
            print(f"Habit '{habit_name}' removed successfully !")
        else :
            print(f"Error removing habit '{habit_name}' from database.")

    def mark_habit_done(self) :
        """A method used to mark a habit as done, asking for the number or the name,
        and checking whether there is such a habit in the list"""
        # Check whether there are habits which can be marked as done
        if not self.user.habits:
            print("Sorry, no habits to mark as done !")
            return
        # Show a numbered list of the current habits
        print("\nCurrent habits :")
        for index, habit in enumerate(self.user.habits, 1):
            print(f"{index}. {habit.name}")
        choice = input("Enter habit number or name : ")
        ''' habit = next((habit for habit in self.user.habits if habit.name == name), None)'''
        # Handle both numeric and text input
        selected_habit = None
        if choice.isdigit():
            choice_num = int(choice)
            if 1 <= choice_num <= len(self.user.habits):
                selected_habit = self.user.habits[choice_num - 1]
            else:
                print("Invalid number, please try again !")
                return
        else:
            selected_habit = next((h for h in self.user.habits if h.name == choice), None)
            if not selected_habit:
                print(f"Habit '{choice}' not found !")
                return
        if selected_habit :
            selected_habit.mark_as_done()
            self.db.save_completion(selected_habit, datetime.date.today())
            print(f"Habit '{selected_habit.name}' marked as done !")
        else :
            print("Habit not found.")

    def view_statistics(self) :
        """A method which shows a general overview of your habit-statistics in CLI-form,
        showing the name, current streak, longest streak, potentially missed days,
        and the newest completed dates, using the get_statistics-method from the analytics-class"""
        try :
            stats = self.analytics.get_statistics()
            if not stats :
                print("\nNo habits to show statistics for !")
                return

            print("\n=== Habit Statistics ===")
            for habit_name, data in stats.items() :
                current_streak = data.get('current_streak', 0)
                longest_streak = data.get('longest_streak', 0)
                missed = data.get('missed', 0)
                completed_dates = data.get('completed_dates', [])
                habit = self.user.get_habit_by_name(habit_name)
                frequency = habit.frequency
                start_date = habit.start_date
                print(f"\nHabit : {habit_name}")
                print(f"Frequency : {frequency.capitalize()}")
                print(f"Start date : {start_date}")
                if frequency == 'daily' :
                    print(f"Current streak : {current_streak} days")
                    print(f"Longest streak : {longest_streak} days")
                    print(f"Number of missed days : {missed}")
                elif frequency == 'weekly' :
                    print(f"Current streak : {current_streak} weeks")
                    print(f"Longest streak : {longest_streak} weeks")
                    print(f"Number of missed weeks : {missed}")
                elif frequency == 'monthly' :
                    print(f"Current streak : {current_streak} months")
                    print(f"Longest streak : {longest_streak} months")
                    print(f"Number of missed Months : {missed}")
                if completed_dates :
                    print("Recent completions : ")
                    # the [:7] cuts off the completed_dates after 7 entries,
                    # could theoretically remove it and show all completed dates,
                    # but don't know whether you'd want to see 50 or 100 entries for one habit,
                    # given enough "marks"
                    for date in completed_dates[:7]:
                        print(f"  - {date}")
                # printing 30 "-" as a separator
                print("-" * 30)
        # Not really needed here, but an Exception-case including an Error-message
        # for a "real world"-application-problem, we've all run into those using Computers, Phones or tablets lol
        except Exception as e :
            print(f"\nError displaying statistics: {str(e)}")
            print("Please try again or contact support if the issue persists.")

    def view_longest_streak_for_specific_habit(self) :
        """Displaying the longest streak for a specific habit,
        using the longest_streak_for_specific-habit-method from the analytics-class"""
        print("\nHabits to choose from :")
        for index, habit in enumerate(self.user.habits, 1):
            print(f"{index}. {habit.name}")
        choice = input("Number or name of the habit : ")
        selected_habit = None
        if choice.isdigit() :
            choice_num = int(choice)
            if 1 <= choice_num <= len(self.user.habits) :
                selected_habit = self.user.habits[choice_num - 1]
            else :
                print("Invalid number, please try again !")
                return
        else :
            selected_habit = next((h for h in self.user.habits if h.name == choice), None)
            if not selected_habit :
                print(f"Habit '{choice}' not found !")
                return
        longest_streak = self.analytics.longest_streak_for_specific_habit(selected_habit.name)

        # Handling the day/days, week/weeks etc.-problem
        unit = ""
        if selected_habit.frequency == "daily" :
            unit = "day" if longest_streak == 1 else "days"
        elif selected_habit.frequency == "weekly" :
            unit = "week" if longest_streak == 1 else "weeks"
        elif selected_habit.frequency == "monthly" :
            unit = "month" if longest_streak == 1 else "months"

        print(f"The longest streak for the habit '{selected_habit.name}' is : {longest_streak} {unit}")

    def view_longest_streak_across_all_habits(self) :
        """Showing the longest streak across all habits,
        using the get_longest_streak_for_all-method from the analytics-class"""
        longest_streak_habit, longest_streak_all = self.analytics.get_longest_streak_for_all()
        if longest_streak_habit is None :
            print("No habits have been marked es done yet !")
            return
        unit = ""
        if longest_streak_habit.frequency == "daily":
            unit = "day" if longest_streak_all == 1 else "days"
        elif longest_streak_habit.frequency == "weekly":
            unit = "week" if longest_streak_all == 1 else "weeks"
        elif longest_streak_habit.frequency == "monthly":
            unit = "month" if longest_streak_all == 1 else "months"

        print(f"The longest streak across all habits is :\n{longest_streak_habit.name} : {longest_streak_all} {unit}")

    def view_total_amount_of_missed_habits(self) :
        """Displaying the the total amount of missed habits,
        using the get_all_missed-habits-method from the analytics-class"""
        total_missed = self.analytics.get_all_missed_habits()
        print(f"\nThe total of missed dates across all habits : {total_missed}")

    def view_habits_with_same_periodicity(self) :
        """Show habits with the same periodicity/frequency,
        using the list_habits_by_periodicity-method from the analytics-class"""
        frequency = input("Enter the chosen frequency (daily, weekly or monthly) : ")
        if frequency not in ["daily", "weekly", "monthly"] :
            print("Invalid frequency. Please choose daily, weekly or monthly")
            return

        habits = self.analytics.list_habits_by_periodicity(frequency)
        if not habits :
            print(f"No {frequency} habits found !")
            return

        print(f"\n {frequency.capitalize()} habits : ")
        for habit_name in habits :
            print(f"- {habit_name}")

    def list_all_habits(self) :
        """Displaying all habits in the user-habit-list"""
        if not self.user.habits :
            print("\nNo habits created yet !")
            return

        print("Current Habits : ")
        for index, habit in enumerate(self.user.habits, 1) :
            print(f"{index}. {habit.name}")