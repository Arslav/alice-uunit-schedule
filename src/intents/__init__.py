import datetime as _datetime
from typing import Optional

from commands import *
from intents.exceptions import *


class AbstractIntent:
    def __init__(self, tokens: dict, entities: dict, slots: dict) -> None:
        self._tokens = tokens
        self._entities = entities
        self._slots = slots

    def run(self) -> str:
        pass


def _is_yandex_datetime_type(entity) -> bool:
    return entity['type'] == 'YANDEX.DATETIME'


def _has_date_attribute(value) -> bool:
    return 'month' in value and 'day' in value


def _is_relative_day(value) -> bool:
    return 'day_is_relative' in value and value['day_is_relative']


def _get_yandex_date(value: dict) -> Optional[_datetime.datetime]:
    try:
        if _is_relative_day(value):
            date = _datetime.datetime.now()
            delta = _datetime.timedelta(days=value['day'])

            return date + delta

        if _has_date_attribute(value):
            return _datetime.datetime.now().replace(day=value['day'], month=value['month'])

    except ValueError:
        return None

    return None


class ScheduleIntent(AbstractIntent):
    _weekdays = {
        'monday': 1,
        'tuesday': 2,
        'wednesday': 3,
        'thursday': 4,
        'friday': 5,
        'saturday': 6,
        'sunday': 7,
    }

    def run(self) -> str:
        self._raise_if_not_time_slot()

        date: datetime
        if self._is_date_slot():
            date = self._absolute_date_intent()
        else:
            date = self._weekday_intent()

        if not date:
            raise NotRecognizedDateError()

        command = ByDateCommand(date, self._has_class_slot())

        return command.execute()

    def _has_class_slot(self) -> bool:
        return 'class' in self._slots

    def _weekday_intent(self) -> _datetime.datetime:
        weekday = self._get_weekday_from_slot()

        now = _datetime.datetime.now()

        date = now - _datetime.timedelta(days=now.isoweekday())
        date += _datetime.timedelta(days=weekday + 7 if weekday < now.isoweekday() else 0)

        return date

    def _absolute_date_intent(self) -> Optional[_datetime.datetime]:
        entity = self._find_yandex_datetime()
        if not entity:
            return None

        return _get_yandex_date(entity['value'])

    def _get_weekday_from_slot(self) -> int:
        return self._weekdays[self._slots['time']['value']]

    def _is_date_slot(self) -> bool:
        return self._slots['time']['value'] == 'date'

    def _raise_if_not_time_slot(self) -> None:
        if 'time' not in self._slots:
            raise IntentError()

    def _find_yandex_datetime(self) -> Optional[dict]:
        for entity in self._entities:
            if _is_yandex_datetime_type(entity):
                return entity
        
        return None
