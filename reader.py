from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker

from models import Fact


class HamsterDBReader:
    """Provide ORM access to facts in a hamster-indicator database."""

    def __init__(self, db):
        self.db = db
        engine = create_engine(self.db)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()

    def get_facts(self, start, end, tag=None):
        self.assert_max_one_not_ended_record()
        facts = self.session.query(Fact).filter(Fact.start_time >= start,
                                                or_(Fact.end_time == None,
                                                    Fact.end_time <= end))

        if tag:
            facts = facts.filter(Fact.tags.any(name=tag))
        return facts.order_by(Fact.start_time)

    def assert_max_one_not_ended_record(self):
        facts = self.session.query(Fact).filter(Fact.end_time == None)
        assert facts.count() < 2, "More than one record has no end time!"

