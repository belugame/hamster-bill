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

    def get_workdays(self):
        all_days = [day for day in Calendar().itermonthdates(self.year, self.month)
                    if day.month == self.month]
        return [x for x in all_days if not any([x in config.HOLIDAYS,
                                                x.weekday() in [5, 6]])]

    def __repr__(self):
        workdays = self.get_workdays()
        today = date.today()
        total_workdays = len(workdays)
        left_workdays = len(workdays[workdays.index(today):])
        percent_days = left_workdays / total_workdays
        current_hours = self.report.get_durations_by_day(self.report.facts)[1]
        needed_hours = len(workdays) * config.WORKDAY_HOURS
        percent_fulfillment = current_hours / needed_hours

        data = dict(
            month=today.strftime("%B %Y"),
            total_workdays=total_workdays,
            left_workdays=left_workdays,
            current_hours=current_hours,
            percent_days=percent_days,
            needed_hours=needed_hours,
            percent_fulfillment=percent_fulfillment
        )

        return """
        {month}:
        ------------------------
        {left_workdays} out of {total_workdays} workdays left ({percent_days:.1%} left).
        {current_hours:.0f} out of {needed_hours} needed hours worked ({percent_fulfillment:.1%} fulfilled).
        """.format(**data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('client', nargs="?")  # = hamster tag
    args = parser.parse_args()

    client = args.client
    today = date.today()

    print(HamsterProgress(today.year, today.month, client))
