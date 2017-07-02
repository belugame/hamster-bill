#!/usr/bin/env python
from calendar import Calendar
from datetime import date, datetime, timedelta
import argparse

from ascii_graph import Pyasciigraph
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


    def __init__(self, year, month, client):
        self.client = client
        self.month = month
        self.year = year
        self.report = HamsterReport(year, month, client)


    def __repr__(self):
        self.days, self.workdays = Utils.get_days(self.year, self.month)
        today = date.today()
        now = datetime.now()
        start_of_month = datetime(self.year, self.month, 1, 0, 0, 0)
        seconds_of_month_passed = (now - start_of_month).total_seconds()
        total_seconds_of_month = len(self.days) * 24 * 60 * 60
        percentage_of_month_gone = seconds_of_month_passed / total_seconds_of_month
        total_workdays = len(self.workdays)
        current_hours = self.report.get_durations_by_day(self.report.facts)[1]
        total_needed_hours = Utils.calculate_needed_hours(self.year, self.month)
        if current_hours == 0:
            percentage_of_workhours_done = 0
        else:
            percentage_of_workhours_done = current_hours / total_needed_hours

        performance = (percentage_of_workhours_done - percentage_of_month_gone) * 100 * (total_needed_hours/100)
        performance = "{:.1f} h {}".format(abs(performance),
                                           "ahead" if performance >= 0 else "behind")

        graph = Pyasciigraph(float_format='{0:.1%}', graphsymbol='֍', line_length=20)
        graph = "\n        ".join(graph.graph(None, [("Passed", percentage_of_month_gone),
                                                     ("Fulfilled", percentage_of_workhours_done)]))

        data = dict(
            month=today.strftime("%B %Y"),
            total_workdays=total_workdays,
            current_hours=current_hours,
            total_needed_hours=total_needed_hours,
            needed_hours_left=total_needed_hours - current_hours,
            percentage_of_workhours_done=percentage_of_workhours_done,
            percentage_of_month_gone=percentage_of_month_gone,
            graph=graph,
            performance=performance
        )

        return """
        {month}:
        -----------------------------------------------------
        Workdays: {total_workdays:3}
        Hours: {current_hours:.1f} / {total_needed_hours} ({needed_hours_left:.1f} left)
        Status: {performance}

        {graph}
        """.format(**data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('client', nargs="?")  # = hamster tag
    args = parser.parse_args()

    client = args.client
    today = date.today()

    print(HamsterProgress(today.year, today.month, client))
