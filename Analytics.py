import datetime

class Analytics :
    def __init__(self, habits) :
        """Constructor to initialize the habits."""
        self.habits = habits

    def list_current_habits(self) :
        """This method returns all currently tracked habits."""
        return [habit.name for habit in self.habits]

    def list_habits_by_periodicity(self, frequency) :
        """This method returns habits with a given frequency, using list comprehension."""
        return [habit.name for habit in self.habits if habit.frequency == frequency]

    def get_current_streak(self, habit) :
        """This method calculates the current streak for a habit,
        daily, weekly and monthly streaks have to be calculated separately."""
        if not habit.completed_dates : # in case there are no completed dates
            return 0

        completed_dates = sorted(habit.completed_dates) # creates and ascending list of the completed dates
        today = datetime.date.today() # today's date
        current_streak = 0


        # Gets the current streak for a daily habit using a for-loop, starting with the most recent entry -> "reversed",
        # and adding 1 every time there is a completed date for the day before, "breaks" if there isn't
        if habit.frequency == 'daily' :
            for date in reversed(completed_dates) :
                if (today - date).days == current_streak :
                    current_streak += 1
                else :
                    break

        # calculation for weekly habits
        elif habit.frequency == 'weekly' :
            current_week = today - datetime.timedelta(days = today.weekday()) # gets the start of the current week -> Monday
            for date in reversed(completed_dates) :
                week_start = date - datetime.timedelta(days = date.weekday()) # gets the start of the week for each completed date
                if week_start == current_week :
                    current_streak = 1 # adds 1 if there is a completed date for this week
                elif week_start == current_week - datetime.timedelta(weeks = current_streak) :
                    current_streak += 1 # adds 1 each time there is a(nother) completed date in the week before
                else :
                    break

        # This calculates the method for monthly habits, but on a 30-day-basis
        # To use calendar months, you'd have to include the "relativedelta"-package
        elif habit.frequency == 'monthly' :
            current_month = today.replace(day = 1) # get the beginning of the month
            for date in reversed(completed_dates) :
                month_start = date.replace(day = 1)
                if month_start == current_month :
                    current_streak = 1
                    # Can't use "months" the same way "weeks" were used above, so have to multiply by 30 to jump 30 days
                elif month_start == current_month - datetime.timedelta(days = 30 * current_streak) :
                    current_streak += 1
                else :
                    break

        return current_streak

    def get_longest_streak(self, habit) :
        """This method calculates the longest streak for a habit and again,
        daily, weekly and monthly habits have to be treated separately.
        Unlike in the method above, it starts with the oldest entries, since it has to go through all dates anyway.
        Within the for-loops, it checks whether there is a completed date
        for the day/week/month after the currently looked at date"""
        if not habit.completed_dates :
            return 0

        completed_dates = sorted(habit.completed_dates)
        longest_streak = 1 # if there are no completed dates, it returns 0, that's why 1 is assigned
        ongoing_streak = 1 # assigned 1, because the tested object is the first "completed" date of a possible new streak

        for i in range(1, len(completed_dates)) :
            if habit.frequency == "daily" :
                if (completed_dates[i] - completed_dates[i - 1]).days == 1 :
                    ongoing_streak += 1
                else :
                    # Using the max-function to compare the newest calculated streak,
                    # to the, so far, longest calculated streak, and replacing the value of the longest streak
                    # with the ongoing streak if the 2nd one is bigger.
                    longest_streak = max(longest_streak, ongoing_streak)
                    ongoing_streak = 1

            elif habit.frequency == "weekly" :
                # Calculating the start of the week for the ongoing and previous week, for easier comparison
                week_start_ongoing = completed_dates[i] - datetime.timedelta(completed_dates[i].weekday())
                week_start_previous = completed_dates[i - 1] - datetime.timedelta(completed_dates[i - 1].weekday())
                if (week_start_ongoing - week_start_previous).days == 7 :
                    ongoing_streak += 1
                else :
                    longest_streak = max(longest_streak, ongoing_streak)
                    ongoing_streak = 1

            elif habit.frequency == "monthly" :
                # Calculating the start of the month for the ongoing and previous month, month = 30 days
                month_start_ongoing = completed_dates[i].replace(day = 1)
                month_start_previous = completed_dates[i - 1].replace(day = 1)
                if (month_start_ongoing - month_start_previous).days == 30 :
                    ongoing_streak += 1
                else :
                    longest_streak = max(longest_streak, ongoing_streak)
                    ongoing_streak = 1

        return max(longest_streak,ongoing_streak)

    def get_longest_streak_for_all(self) :
        """Calculate and return the longest streak across all habits, and the habit itself,
        using the get_longest_streak-method from above in a for-loop to find and return the
        habit with the longest streak."""
        longest_streak = 0
        longest_streak_habit = None

        for habit in self.habits:
            # This is where the above-method is being used, getting the longest streak of one/each habit in the habit-list.
            current_longest_streak = self.get_longest_streak(habit)
            if current_longest_streak > longest_streak :
                longest_streak = current_longest_streak
                longest_streak_habit = habit
        return longest_streak_habit, longest_streak

    def longest_streak_for_specific_habit(self, habit_name) :
        """Return the longest streak for a specific habit,
        accessible through the CLI under "View statistics"""
        for habit in self.habits:
            if habit.name == habit_name:
                return self.get_longest_streak(habit)
        return None  # Added return for non-existent habits

    def get_missed_habits(self, habit) :
        """Returns the number of missed habits based on frequency,
        taking into account, that the current day/week/month should NOT
        be shown or calculated as a missed day yet, but should be calculated
        as a completed date, if marked as done"""
        today = datetime.date.today()
        missed = 0
        if habit.frequency == 'daily' :
            # gets the number of dates since the start, "+ 1" to include today's date.
            # Could theoretically add it within the else-case :
            # "days + 1 if today in habit.completed_dates else days"
            days = (today - habit.start_date).days + 1
            if days == 0 :
                missed = 0
            else :
                counted_days = days if today in habit.completed_dates else days - 1
                # a safeguard, in case there would e.g. suddenly be
                # more completed_dates than counted_days, don't want a negative result
                missed = max(0, counted_days - len(habit.completed_dates))
        elif habit.frequency == 'weekly' :
            weeks = (today - habit.start_date).days // 7
            # includes the current partial week
            total_weeks = weeks + 1
            if total_weeks == 0 :
                missed = 0
            else :
                # creates a set of week-"indices", so if completed 3 times in 3 weeks - {0, 1, 2}
                completed_weeks = {
                    (date - habit.start_date).days // 7 for date in habit.completed_dates
                }
                # checks whether the current week (or rather it's index) is in the completed_weeks-list or not
                counted_weeks = total_weeks if weeks in completed_weeks else total_weeks - 1
                missed = max(0, counted_weeks - len(completed_weeks))
        elif habit.frequency == 'monthly' :
            months = (today - habit.start_date).days // 30
            total_months = months + 1
            if total_months == 0 :
                missed = 0
            else :
                completed_months = {
                    (date - habit.start_date).days // 30 for date in habit.completed_dates
                }
                counted_months = total_months if months in completed_months else total_months - 1
                missed = max(0, counted_months - len(completed_months))
        return missed

    def get_all_missed_habits(self) :
        """Return the total number of missed habits/dates across all existing habits"""
        total_missed = 0
        for habit in self.habits :
            total_missed += self.get_missed_habits(habit)
        return total_missed

    def get_statistics(self) :
        """Returns statistics for all habits, like the current streak, longest streak,
        whether it's been missed recently and the completed_dates"""
        stats = {}
        try :
            for habit in self.habits :
                # Converting potential strings into datetime.date objects.
                completed_dates = []
                for date in habit.completed_dates :
                    # checking whether the "date" is a string, converting to datetime object in case it is
                    if isinstance(date, str) :
                        try :
                            date_object = datetime.datetime.strptime(date, '%Y-%m-%d').date()
                            completed_dates.append(date_object)
                        except ValueError :
                            print(f"Warning : Invalid date format found : {date}")
                            continue
                    # Checking whether it's already a datetime.date object, in this case it'll get directly appended
                    elif isinstance(date, datetime.date) :
                        completed_dates.append(date)

                # Update a habit's completed dates with converted dates
                habit.completed_dates = completed_dates
                # calling the methods needed to get the desired statistics/numbers for each line,
                # dates are sorted in reverse, to show the newest date first, not the oldest
                stats[habit.name] = {
                    'current_streak' : self.get_current_streak(habit),
                    'longest_streak': self.get_longest_streak(habit),
                    'missed' : self.get_missed_habits(habit),
                    'completed_dates' : sorted(habit.completed_dates, reverse = True)
                }
            return stats
        except Exception as e :
            print(f"Error generating statistics : {str(e)}")
            return {}