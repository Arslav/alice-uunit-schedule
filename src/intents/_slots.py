from datetime import datetime, timedelta
from typing import Optional

from intents import EntityRepository

_weekdays = {
    'monday': 1,
    'tuesday': 2,
    'wednesday': 3,
    'thursday': 4,
    'friday': 5,
    'saturday': 6,
    'sunday': 7,
}


class Slot:
    def __init__(self, slot):
        self.slot = slot

    @property
    def value(self) -> dict:
        return self.slot['value']


class WeekdaySlot(Slot):
    @property
    def weekday(self) -> int:
        return _weekdays[self.value]

    @property
    def datetime(self) -> Optional[datetime]:
        now = datetime.now()

        date = now - timedelta(days=now.isoweekday())
        date += timedelta(days=self.weekday + (7 if self.weekday < now.isoweekday() else 0))

        return date


class DateSlot(Slot):
    def date_from_entities(self, entity_repository: EntityRepository) -> Optional[datetime]:
        entity = entity_repository.find_yandex_datetime()
        if not entity:
            return None
        return entity.get_datetime()


def create_slot_by_value(slot: dict) -> Slot:
    value = slot['value']
    if value in _weekdays:
        return WeekdaySlot(slot)
    elif value == 'date':
        return DateSlot(slot)

    return Slot(slot)


class SlotRepository:
    def __init__(self, slots: dict) -> None:
        self._slots = slots

    def has_slot(self, slot_name: str):
        return slot_name in self._slots

    def get_slot(self, slot_name: str) -> Optional[Slot]:
        if not self.has_slot(slot_name):
            return None

        return create_slot_by_value(self._slots[slot_name])
