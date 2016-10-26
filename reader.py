from sqlalchemy import create_engine
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
        facts = self.session.query(Fact).filter(Fact.start_time >= start,
                                                Fact.end_time <= end)
        if tag:
            facts = facts.filter(Fact.tags.any(name=tag))
        return facts.order_by(Fact.start_time)
