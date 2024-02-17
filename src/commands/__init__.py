from datetime import datetime

import commands._render as render
from uunit import Parser, Fetcher, FetcherException


class CommandInterface:
    def execute(self):
        pass


class ByDateCommand(CommandInterface):
    datetime_obj: datetime
    render: render.RenderInterface

    def __init__(self, datetime_obj: datetime, is_by_class: bool = False) -> None:
        self.render = render.factory_by_is_class(is_by_class)
        self.datetime_obj = datetime_obj

    def execute(self) -> str:
        calendar = self.datetime_obj.isocalendar()

        try:
            data = Fetcher().get_group_schedule()
            parser = Parser(data, calendar.week, calendar.weekday)
            schedule = parser.parse()

            return self.render.render(schedule, self.datetime_obj)
        except FetcherException:
            return 'Произошла ошибка, попробуй еще раз!'
