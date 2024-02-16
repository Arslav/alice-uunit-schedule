from datetime import datetime


class RenderInterface:
    def render(self, *args) -> str:
        pass


class DefaultRender(RenderInterface):
    _pairs: list = [
        'Первая пара',
        'Вторая пара',
        'Третья пара',
        'Четвертая пара',
        'Пятая пара',
        'Шестая пара',
        'Седьмая пара',
    ]
    _dayList = [
        'первое', 'второе', 'третье', 'четвёртое', 'пятое',
        'шестое', 'седьмое', 'восьмое', 'девятое', 'десятое',
        'одиннадцатое', 'двенадцатое', 'тринадцатое', 'четырнадцатое',
        'пятнадцатое', 'шестнадцатое', 'семнадцатое', 'восемнадцатое',
        'девятнадцатое', 'двадцатое', 'двадцать первое', 'двадцать второе',
        'двадцать третье', 'двадацать четвёртое', 'двадцать пятое',
        'двадцать шестое', 'двадцать седьмое', 'двадцать восьмое',
        'двадцать девятое', 'тридцатое', 'тридцать первое'
    ]
    _monthList = [
        'января', 'февраля', 'марта',
        'апреля', 'мая', 'июня',
        'июля', 'августа', 'сентября',
        'октября', 'ноября', 'декабря'
    ]
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
    _default = 'Поздравляю! Сегодня вы отдыхаете!'

    def render(self, *args) -> str:
        data: list = args[0]
        datetime_obj: datetime = args[1]

        if not data:
            return self._default

        text = ''
        text += self._get_header_by_date(datetime_obj) + '\n'

        for item in data:
            text += f"{self._get_pair_number(item[0])} - {item[4]} - \"{item[1]}\"\n"

        return text

    def _get_date_text(self, datetime_obj: datetime):
        date_text = self._dayList[datetime_obj.day - 1] + ' ' + self._monthList[datetime_obj.month - 1]
        return date_text

    def _get_header_by_date(self, datetime_obj: datetime):
        now = datetime.now()
        if datetime_obj.date() == now.date():
            return self._todayTitle
        elif datetime_obj.date() == now.replace(day=now.day + 1).date():
            return self._tomorrowTitle
        else:
            date_text = self._get_date_text(datetime_obj)
            title = self._nextTitle[datetime_obj.isocalendar().weekday - 1]
            return title.format(date_text)

    def _get_pair_number(self, number: int) -> str:
        return self._pairs[number - 1]


class ByClassRender(DefaultRender):
    def render(self, *args) -> str:
        data: list = args[0]
        datetime_obj: datetime = args[1]

        if not data:
            return self._default

        text = ''
        text += self._get_header_by_date(datetime_obj) + '\n'
        for item in data:
            text += f"{self._get_pair_number(item[0])} - \"{item[2]}\"\n"

        return text
