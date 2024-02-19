import commands._pronouncing as pronouncing
from utils import DateTime
from uunit import Pair


class RenderInterface:
    def render(self, *args) -> str:
        pass


class DefaultRender(RenderInterface):
    _nextTitle = [
        'Расписание занятий на понедельник, {}:',
        'Расписание занятий на вторник, {}:',
        'Расписание занятий на среду, {}:',
        'Расписание занятий на четверг, {}:',
        'Расписание занятий на пятницу, {}:',
        'Расписание занятий на субботу, {}:',
        'Расписание занятий на воскресение, {}:',
    ]
    _todayTitle = 'Расписание занятий на сегодня'
    _tomorrowTitle = 'Расписание занятий на завтра'
    _default = [
        'Поздравляю! Сегодня вы отдыхаете!',
        'Поздравляю! Завтра вы отдыхаете!',
        'Поздравляю! В этот день вы отдыхаете!',
    ]

    def render(self, *args) -> str:
        data: list[Pair] = args[0]
        datetime_obj: DateTime = DateTime.from_datetime(args[1])

        if not data:
            return self._get_default_by_date(datetime_obj)

        text = self._get_header_by_date(datetime_obj) + '\n'

        for item in data:
            text += self._format(item) + '\n'

        return text

    def _get_title(self, datetime_obj: DateTime) -> str:
        weekday = datetime_obj.weekday()
        title = self._nextTitle[weekday]
        date = pronouncing.date(datetime_obj)

        return title.format(date)

    def _get_default_by_date(self, datetime_obj: DateTime) -> str:
        if datetime_obj.is_today():
            return self._default[0]
        elif datetime_obj.is_tomorrow():
            return self._default[1]

        return self._default[2]

    def _get_header_by_date(self, datetime_obj: DateTime) -> str:
        if datetime_obj.is_today():
            return self._todayTitle
        elif datetime_obj.is_tomorrow():
            return self._tomorrowTitle

        return self._get_title(datetime_obj)

    def _format(self, item: Pair) -> str:
        return f'{pronouncing.pair_number(item.number)} - {item.type} - "{item.title}"'


class ByRoomRender(DefaultRender):
    def _format(self, item: Pair) -> str:
        return f'{pronouncing.pair_number(item.number)} - "{item.room}"'


class FirstPairRender(RenderInterface):
    _nextTitle = [
        'Понедельник, {}, занятия начинаются в {}, {}',
        'Вторник, {}, занятия начинаются в {}, {}',
        'Среда, {}, занятия начинаются в {}, {}',
        'Четверг, {}, занятия начинаются в {}, {}',
        'Пятница, {}, занятия начинаются в {}, {}',
        'Суббота, {}, занятия начинаются в {}, {}',
        'Воскресение, {}, занятия начинаются {}, {}',
    ]
    _todayTitle = 'Сегодня занятия начинаются в {}, {}'
    _tomorrowTitle = 'Завтра занятия начинаются в {}, {}'
    _default = [
        'Поздравляю! Сегодня можете спать спокойно. Занятий не будет!',
        'Поздравляю! Завтра вы можете спать спокойно. Занятий не будет!',
        'Поздравляю! В этот день вы можете спать спокойно. Занятий не будет!',
    ]

    def render(self, *args) -> str:
        data: list[Pair] = args[0]
        datetime_obj: DateTime = DateTime.from_datetime(args[1])

        if not data:
            return self._get_default_by_date(datetime_obj)

        time = data[0].time.split('-')[0]
        pair = pronouncing.pair_number(data[0].number).lower()

        return self._get_header_by_date(datetime_obj, time, pair)

    def _get_header_by_date(self, datetime_obj: DateTime, start_time: str, pair: str) -> str:
        if datetime_obj.is_today():
            return self._todayTitle.format(start_time, pair)
        elif datetime_obj.is_tomorrow():
            return self._tomorrowTitle.format(start_time, pair)

        return self._get_title(datetime_obj, start_time, pair)

    def _get_title(self, datetime_obj: DateTime, start_time: str, pair: str) -> str:
        weekday = datetime_obj.weekday()
        title = self._nextTitle[weekday]
        date = pronouncing.date(datetime_obj)

        return title.format(date, start_time, pair)

    def _get_default_by_date(self, datetime_obj: DateTime) -> str:
        if datetime_obj.is_today():
            return self._default[0]
        elif datetime_obj.is_tomorrow():
            return self._default[1]

        return self._default[2]


def factory_by_is_room(is_by_room: bool) -> RenderInterface:
    return DefaultRender() if not is_by_room else ByRoomRender()
