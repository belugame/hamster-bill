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
        return all_days, [x for x in all_days if not any([x in config.HOLIDAYS,
                                                          x.weekday() in [5, 6]])]

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

    def __repr__(self):
        days, workdays = Utils.get_days(self.year, self.month)
        today = date.today()
        cutoff_day = today if datetime.now().hour < self.cutoff_hour else today + timedelta(days=1)
        total_workdays = len(workdays)
        left_days = len(days[days.index(cutoff_day):])
        left_workdays = len(workdays[workdays.index(next(w for w in workdays if w >= cutoff_day)):])
        percent_days = 1 - (left_days / len(days))
        percent_workdays = 1 - (left_workdays / total_workdays)
        current_hours = self.report.get_durations_by_day(self.report.facts)[1]
        needed_hours = Utils.calculate_needed_hours(self.year, self.month)
        percent_fulfillment = current_hours / needed_hours
        delta_hours = (needed_hours * percent_days) - current_hours

        data = dict(
            month=today.strftime("%B %Y"),
            total_days=len(days),
            total_workdays=total_workdays,
            left_days=left_days,
            left_workdays=left_workdays,
            current_hours=current_hours,
            percent_days=percent_days,
            percent_workdays=percent_workdays,
            needed_hours=needed_hours,
            percent_fulfillment=percent_fulfillment,
            delta_hours=abs(delta_hours),
            behind_ahead="behind" if delta_hours > 0 else "ahead of"
        )

        return """
        {month}:
        -----------------------------------------------------
        {left_days:4} out of {total_days:3} days left           ({percent_days:.1%} passed)
        {left_workdays:4} out of {total_workdays:3} workdays left       ({percent_workdays:.1%} passed)
        {current_hours:4.1f} out of {needed_hours:3} needed hours worked ({percent_fulfillment:.1%} fulfilled)
        {delta_hours:4.1f} hours {behind_ahead} schedule.
        """.format(**data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('client', nargs="?")  # = hamster tag
    args = parser.parse_args()

    client = args.client
    today = date.today()

    print(HamsterProgress(today.year, today.month, client))
