import logging
from typing import Dict, List

from app import db
from app.udaconnect.models import Person

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("api-person")


class PersonService:
    @staticmethod
    def create(person: Dict) -> Person:
        logger.info(f"Creating person from {person}")
        new_person = Person()
        new_person.first_name = person["first_name"]
        new_person.last_name = person["last_name"]
        new_person.company_name = person["company_name"]

        db.session.add(new_person)
        db.session.commit()

        return new_person

    @staticmethod
    def retrieve(person_id: int) -> Person:
        logger.info(f"Retrieving person_id: {person_id}")
        person = db.session.query(Person).get(person_id)
        return person

    @staticmethod
    def retrieve_all() -> List[Person]:
        logger.info("Retrieving all registered attendees")
        return db.session.query(Person).all()
