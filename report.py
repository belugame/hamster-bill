#!/usr/bin/env python
import argparse
import datetime
import os
from calendar import monthrange

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
            facts = db.get_facts(*self.billing_period, self.client)

        total_duration = datetime.timedelta()
        for f in facts:
            d = {
                "description": ", ".join(t for t in (f.activity.name, f.description) if t),
                "start": f.start_time.strftime("%d.%m %H:%M"),
                "end": f.end_time.strftime("%d.%m %H:%M"),
                "duration": f.duration
            }
            print("{} - {}  {}".format(f.start_time, f.end_time, f.activity.name))

            total_duration += f.duration

        self.total_hours = total_duration.total_seconds() / 3600.0
        print("Total: {:.2f} hours in {}/{}".format(self.total_hours,
                                                    self.month, self.year))

    def determine_billing_period(self):
        """Include activities of following day until 4am"""
        start_time = datetime.datetime(self.year, self.month, 1, 0, 0, 0)
        _, last = monthrange(self.year, self.month)
        end_time = start_time + datetime.timedelta(days=last, hours=self.hours_after_midnite_to_include)
        now = datetime.datetime.now()
        end_time = end_time if now > end_time else now
        return start_time, end_time


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
