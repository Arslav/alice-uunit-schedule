from datetime import datetime

import commands._render as render
from uunit import Parser, Fetcher, FetcherException


class CommandInterface:
    def execute(self):
        pass


class AbstractScheduleCommand(CommandInterface):
    datetime_obj: datetime
    render: render.RenderInterface

    def __init__(self):
        pass

    def _fetch_schedule(self):
        calendar = self.datetime_obj.isocalendar()
        data = Fetcher().get_group_schedule()
        parser = Parser(data, calendar.week, calendar.weekday)
        schedule = parser.parse()

        return schedule

    def execute(self) -> str:
        try:
            schedule = self._fetch_schedule()
        except FetcherException:
            return 'Произошла ошибка, попробуй еще раз!'

        return self.render.render(schedule, self.datetime_obj)


class ByDateCommand(AbstractScheduleCommand):
    datetime_obj: datetime
    render: render.RenderInterface

    def __init__(self, datetime_obj: datetime, is_by_room: bool = False) -> None:
        super().__init__()
        self.render = render.factory_by_is_room(is_by_room)
        self.datetime_obj = datetime_obj


class FirstLessonCommand(AbstractScheduleCommand):
    def __init__(self, datetime_obj: datetime) -> None:
        super().__init__()
        self.datetime_obj = datetime_obj
        self.render = render.FirstPairRender()
