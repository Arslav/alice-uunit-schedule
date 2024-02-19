import datetime as _datetime
from typing import Optional


class Entity:
    def __init__(self, entity):
        self.entity = entity

    @property
    def value(self):
        return self.entity['value']

    def is_yandex_datetime_type(self) -> bool:
        return self.entity['type'] == 'YANDEX.DATETIME'

    def has_date_attribute(self) -> bool:
        return 'month' in self.value and 'day' in self.value

    def is_relative_day(self) -> bool:
        return 'day_is_relative' in self.value and self.value['day_is_relative']

    def get_datetime(self) -> Optional[_datetime.datetime]:
        try:
            if self.is_relative_day():
                date = _datetime.datetime.now()
                delta = _datetime.timedelta(days=self.value['day'])

                return date + delta

            if self.has_date_attribute():
                return _datetime.datetime.now().replace(day=self.value['day'], month=self.value['month'])

        except ValueError:
            return None

        return None


class EntityRepository:
    _entities: list[Entity]

    def __init__(self, entities: dict) -> None:
        self._entities = []
        for entity in entities:
            self._entities.append(Entity(entity))

    def find_yandex_datetime(self) -> Optional[Entity]:
        for entity in self._entities:
            if entity.is_yandex_datetime_type():
                return entity

        return None
