import datetime as _datetime
from typing import Optional

from commands import *
from intents._entities import EntityRepository
from intents._slots import SlotRepository, WeekdaySlot, DateSlot
from intents.exceptions import *


class AbstractIntent:
    def __init__(self, tokens: dict, entities: dict, slots: dict) -> None:
        self._tokens = tokens
        self.entity_repository = EntityRepository(entities)
        self.slot_repository = SlotRepository(slots)

    def run(self) -> str:
        pass


class ScheduleIntent(AbstractIntent):
    def run(self) -> str:
        date: Optional[datetime] = None

        self._raise_if_has_not_time_slot()
        slot = self.slot_repository.get_slot('time')

        if isinstance(slot, WeekdaySlot):
            date = slot.datetime
        elif isinstance(slot, DateSlot):
            date = slot.date_from_entities(self.entity_repository)
        else:
            raise NotRecognizedDateError()

        if not date:
            raise NotRecognizedDateError()

        command = ByDateCommand(date, self.slot_repository.has_slot('class'))

        return command.execute()

    def _raise_if_has_not_time_slot(self) -> None:
        if not self.slot_repository.has_slot('time'):
            raise IntentError()


class FirstLessonIntent(AbstractIntent):
    def run(self) -> str:
        date: Optional[datetime] = None
        slot = self.slot_repository.get_slot('time')

        if not slot:
            date = _datetime.datetime.now()
        elif isinstance(slot, WeekdaySlot):
            date = slot.datetime
        elif isinstance(slot, DateSlot):
            date = slot.date_from_entities(self.entity_repository)
        else:
            raise NotRecognizedDateError()

        if not date:
            raise NotRecognizedDateError()

        command = FirstLessonCommand(date)

        return command.execute()
