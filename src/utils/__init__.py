from datetime import datetime


class DateTime(datetime):
    @classmethod
    def from_datetime(cls, datetime_obj: datetime):
        return cls.fromtimestamp(datetime_obj.timestamp())

    def is_today(self) -> bool:
        return datetime.now().date() == self.date()

    def is_tomorrow(self) -> bool:
        now = datetime.now()
        return self.date() == now.replace(day=now.day + 1).date()
