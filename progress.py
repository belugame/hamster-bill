#!/usr/bin/env python
from calendar import Calendar
from datetime import date
import argparse

from report import HamsterReport
import config


class HamsterProgress:

    def __init__(self, year, month, client):
        self.client = client
        self.month = month
        self.year = year
        self.report = HamsterReport(year, month, client)

    def get_days(self):
        all_days = [day for day in Calendar().itermonthdates(self.year, self.month)
                    if day.month == self.month]
        return all_days, [x for x in all_days if not any([x in config.HOLIDAYS,
                                                          x.weekday() in [5, 6]])]

    def __repr__(self):
        days, workdays = self.get_days()
        today = date.today()
        total_workdays = len(workdays)
        left_days = len(days[days.index(today):])
        left_workdays = len(workdays[workdays.index(next(w for w in workdays if w >= today)):])
        percent_days = 1 - (left_days / len(days))
        percent_workdays = 1 - (left_workdays / total_workdays)
        current_hours = self.report.get_durations_by_day(self.report.facts)[1]
        needed_hours = len(workdays) * config.WORKDAY_HOURS
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
            delta_hours=delta_hours,
            behind_ahead="behind" if delta_hours > 0 else "ahead of"
        )

        return """
        {month}:
        -----------------------------------------------------
        {left_days:4} out of {total_days:3} days left           ({percent_days:.1%} passed)
        {left_workdays:4} out of {total_workdays:3} workdays left       ({percent_workdays:.1%} passed)
        {current_hours:3.1f} out of {needed_hours:3} needed hours worked ({percent_fulfillment:.1%} fulfilled)
        {delta_hours:3.1f} hours {behind_ahead} schedule.
        """.format(**data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('client', nargs="?")  # = hamster tag
    args = parser.parse_args()

    client = args.client
    today = date.today()

    print(HamsterProgress(today.year, today.month, client))
