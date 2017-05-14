#!/usr/bin/env python
from calendar import Calendar
from datetime import date, datetime, timedelta
import argparse

from report import HamsterReport
import config


class Utils:

    @classmethod
    def get_days(cls, year, month):
        """Return tuple with list of all days, and all workdays of the month."""
        all_days = [day for day in Calendar().itermonthdates(year, month)
                    if day.month == month]
        return all_days, [x for x in all_days if cls.is_workday(x)]

    @classmethod
    def is_workday(self, day):
        return not any([day in config.HOLIDAYS, day.weekday() in [5, 6]])

    @classmethod
    def calculate_needed_hours(cls, year, month):
        """Return amount of needed work hours of the month."""
        _, workdays = Utils.get_days(year, month)
        return len(workdays) * config.WORKDAY_HOURS


class HamsterProgress:

    cutoff_hour = 18  # after this hour the day is considered finished

    def __init__(self, year, month, client):
        self.client = client
        self.month = month
        self.year = year
        self.report = HamsterReport(year, month, client)

    def next_workday(self, day):
        return self.find_workday(day, reverse=False)

    def previous_workday(self, day):
        return self.find_workday(day, reverse=True)

    def find_workday(self, day, reverse=False):
        days = self.days.copy()
        if reverse:
            days.reverse()
        try:
            foo = next(d for d in days[days.index(day):] if Utils.is_workday(d))
            return foo
        except StopIteration:
            return None

    def get_cutoff_day(self):
        t = date.today()
        tmr = today + timedelta(days=1)
        if not Utils.is_workday(t) or not Utils.is_workday(tmr):
            return self.previous_workday(t)
        elif t == self.days[-1] or datetime.now().hour < self.cutoff_hour:
            return t
        return self.next_workday(t)

    def __repr__(self):
        self.days, self.workdays = Utils.get_days(self.year, self.month)
        today = date.today()
        cutoff_day = self.get_cutoff_day()

        try:
            left_workdays = len(self.workdays[self.workdays.index(cutoff_day):])
        except:
            raise
            left_workdays = 0

        total_workdays = len(self.workdays)
        left_days = len(self.days[self.days.index(cutoff_day):])

        percent_days = 1 - (left_days / len(self.days))
        percent_workdays = 1 - (left_workdays / total_workdays)
        current_hours = self.report.get_durations_by_day(self.report.facts)[1]
        needed_hours = Utils.calculate_needed_hours(self.year, self.month)
        percent_fulfillment = current_hours / needed_hours
        delta_hours = ((total_workdays-left_workdays) * config.WORKDAY_HOURS) - current_hours
        needed_hours_left = needed_hours - current_hours
        needed_hours_per_day_left = needed_hours_left / left_days
        needed_hours_per_workday_left = needed_hours_left / left_workdays if left_workdays else 0

        data = dict(
            month=today.strftime("%B %Y"),
            total_days=len(self.days),
            total_workdays=total_workdays,
            left_days=left_days,
            left_workdays=left_workdays,
            current_hours=current_hours,
            percent_days=percent_days,
            percent_workdays=percent_workdays,
            needed_hours=needed_hours,
            percent_fulfillment=percent_fulfillment,
            delta_hours=abs(delta_hours),
            behind_ahead="behind" if needed_hours_per_workday_left > config.WORKDAY_HOURS else "ahead of",
            needed_hours_left=needed_hours_left,
            needed_hours_per_day_left=needed_hours_per_day_left,
            needed_hours_per_workday_left=needed_hours_per_workday_left
        )

        return """
        {month}:
        -----------------------------------------------------
        {left_days:4} out of {total_days:3} days left           ({percent_days:.1%} passed)
        {left_workdays:4} out of {total_workdays:3} workdays left       ({percent_workdays:.1%} passed)
        {current_hours:4.1f} out of {needed_hours:3} needed hours worked ({percent_fulfillment:.1%} fulfilled)
        {delta_hours:4.1f} hours {behind_ahead} schedule ({needed_hours_left:4.1f} left)
        {needed_hours_per_day_left:4.1f} hours/day left.
        {needed_hours_per_workday_left:4.1f} hours/workday left.
        """.format(**data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('client', nargs="?")  # = hamster tag
    args = parser.parse_args()

    client = args.client
    today = date.today()

    print(HamsterProgress(today.year, today.month, client))
