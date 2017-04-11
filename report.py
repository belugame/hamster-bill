#!/usr/bin/env python
import argparse
import datetime
import operator
from calendar import monthrange
from collections import defaultdict
from time import strptime

from ascii_graph import Pyasciigraph

import config
from reader import HamsterDBReader


class HamsterReport:
    hours_after_midnite_to_include = 4

    def __init__(self, year, month=None, client=None):
        if client:
            assert client in config.CUSTOMER.keys(), \
                "Unknown customer '{}', please add it to config.py first.".format(client)
        self.client = client
        self.month = month
        self.year = year
        self.billing_period = self.determine_billing_period()
        with HamsterDBReader(config.HAMSTER_DB) as db:
            self.facts = db.get_facts(*self.billing_period, self.client)

    def determine_billing_period(self):
        """Include activities of following day until 4am"""
        if self.month:  # 1 month
            start_time = datetime.datetime(self.year, self.month, 1, 0, 0, 0)
            _, last = monthrange(self.year, self.month)
            end_time = start_time + datetime.timedelta(days=last, hours=self.hours_after_midnite_to_include)
            now = datetime.datetime.now()
            end_time = end_time if now > end_time else now
        else:  # whole year
            start_time = datetime.datetime(self.year, 1, 1, 0, 0, 0)
            end_time = datetime.datetime(self.year + 1, 1, 1, self.hours_after_midnite_to_include, 0, 0)
        return start_time, end_time

    def get_durations_by_activity(self, facts):
        activities = defaultdict(datetime.timedelta)
        for f in facts:
            activities[f.activity.name] += f.duration
        total = sum([a.total_seconds() for a in activities.values()])/3600
        activities = sorted(activities.items(), key=operator.itemgetter(1))
        activities.reverse()
        for name, duration in activities:
            print("{:60} {:6.2f} h".format(name, duration.total_seconds()/3600))
        print("Total: {:.2f} h".format(total))
        return activities

    def get_durations_by_day(self, facts):
        days = defaultdict(datetime.timedelta)
        for f in facts:
            days[f.start_time.date()] += f.duration
        total = sum([d.total_seconds() for d in days.values()])/3600
        days = sorted(days.items(), key=operator.itemgetter(0))
        return days, total

    def get_durations_by_month(self, facts):
        months = defaultdict(datetime.timedelta)
        for f in facts:
            months[f.start_time.date().strftime("%B")] += f.duration
        total = sum([d.total_seconds() for d in months.values()])/3600
        months = sorted(months.items(), key=lambda x: strptime(x[0], "%B"))
        return months, total

    def make_monthly_report(self):
        total_duration = datetime.timedelta()
        months, total_hours = self.get_durations_by_month(self.facts)
        title = 'Total hours in {}: {:.2f}'.format(self.year, total_hours)
        self.make_bar_chart(months, title)

    def make_daily_report(self):
        total_duration = datetime.timedelta()
        days, total_hours = self.get_durations_by_day(self.facts)
        title = 'Total hours in {}/{}: {:.2f}'.format(self.month, self.year, total_hours)
        self.make_bar_chart(days, title)

    def make_bar_chart(self, data, title):
        items = [(str(date), timedelta.total_seconds()/3600) for date, timedelta in data]
        graph = Pyasciigraph(float_format='{0:,.2f}', graphsymbol='֍')
        for line in graph.graph(title, items):
            print(line)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('period', nargs="?")
    parser.add_argument('client', nargs="?")  # = hamster tag
    args = parser.parse_args()

    client = args.client
    month = None
    if args.period:
        if "-" in args.period:
            year, month = (int(i) for i in args.period.split("-"))
        else:
            year = int(args.period)
    else:
        today = datetime.date.today()
        year, month = today.year, today.month

    if month:
        HamsterReport(year, month, client).make_daily_report()
    else:
        HamsterReport(year, client=client).make_monthly_report()
