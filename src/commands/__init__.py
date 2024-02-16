from uunit import Parser
from ._render import *


class CommandInterface:
    def execute(self):
        pass


class ByDateCommand(CommandInterface):
    datetime_obj: datetime

    def __init__(self, datetime_obj: datetime, by_class: bool = False) -> None:
        self.render = DefaultRender() if not by_class else ByClassRender()
        self.datetime_obj = datetime_obj

    def execute(self) -> str:
        calendar = self.datetime_obj.isocalendar()
        parser = Parser(calendar.week, calendar.weekday)

        return self.render.render(parser.parse(), self.datetime_obj)
