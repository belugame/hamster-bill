#!/usr/bin/env python
import argparse
import datetime
import os
import operator
from calendar import monthrange
from collections import defaultdict

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
from reader import HamsterDBReader


class HamsterReport:
    hours_after_midnite_to_include = 4

    def __init__(self, client, month, year):
        assert client in config.CUSTOMER.keys(), \
            "Unknown customer '{}', please add it to config.py first.".format(client)
        self.client = client
        self.month = month
        self.year = year
        self.billing_period = self.determine_billing_period()

        with HamsterDBReader(config.HAMSTER_DB) as db:
            self.facts = db.get_facts(*self.billing_period, self.client)

        total_duration = datetime.timedelta()
        _, self.total_hours = self.get_durations_by_day(self.facts)
        print("---------------------")
        print("Total:       {:.2f} h in {}/{}".format(self.total_hours,
                                                    self.month, self.year))

    def determine_billing_period(self):
        """Include activities of following day until 4am"""
        start_time = datetime.datetime(self.year, self.month, 1, 0, 0, 0)
        _, last = monthrange(self.year, self.month)
        end_time = start_time + datetime.timedelta(days=last, hours=self.hours_after_midnite_to_include)
        now = datetime.datetime.now()
        end_time = end_time if now > end_time else now
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
        for day, duration in days:
            print("{}  {:6.2f} h".format(day, duration.total_seconds()/3600))
        return days, total


if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('yearmonth', nargs="?")
    parser.add_argument('client')  # = hamster tag
    args = parser.parse_args()

    client = args.client
    if args.yearmonth:
        year, month = (int(i) for i in args.yearmonth.split("-"))
    else:
        today = datetime.date.today()
        year, month = today.year, today.month

    HamsterReport(client, month, year)
