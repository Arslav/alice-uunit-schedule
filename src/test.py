import json
from unittest.mock import patch

from freezegun import freeze_time

import main
import uunit


def get_from_sample(name: str) -> dict:
    with open(f'tests/samples/{name}', 'r') as data_file:
        json_data = data_file.read()

    return json.loads(json_data)


def get_response_text(data: dict) -> str:
    return data['response']['text']


@freeze_time("2024-02-16")
def test_weekday_by_room() -> None:
    expected = ('Расписание занятий на понедельник, девятнадцатое февраля:\n'
                'Первая пара - "7-401"\n'
                'Вторая пара - "Спортивный зал"\n'
                'Третья пара - "7-206"\n')

    with patch.object(
            uunit.Fetcher,
            'get_group_schedule',
            return_value=get_from_sample('uunit/group_schedule.json')
    ):
        request = get_from_sample('requests/schedule/monday_room.json')
        response = main.handler(request, None)

    actual = get_response_text(response)

    assert actual == expected


@freeze_time("2024-02-16")
def test_today_by_room() -> None:
    expected = ('Расписание занятий на сегодня\n'
                'Первая пара - "9-403"\n'
                'Вторая пара - "9-403"\n'
                'Третья пара - "7-406"\n'
                'Четвертая пара - "7-204"\n')

    with patch.object(
            uunit.Fetcher,
            'get_group_schedule',
            return_value=get_from_sample('uunit/group_schedule.json')
    ):
        request = get_from_sample('requests/schedule/today_room.json')
        response = main.handler(request, None)

    actual = get_response_text(response)

    assert actual == expected


@freeze_time("2024-02-16")
def test_tomorrow() -> None:
    expected = ('Расписание занятий на завтра\n'
                'Третья пара - Лабораторная работа - "Техническая и вычислительная физика"\n'
                'Третья пара - Лабораторная работа - "Техническая и вычислительная физика"\n'
                'Четвертая пара - Лабораторная работа - "Техническая и вычислительная физика"\n'
                'Четвертая пара - Лабораторная работа - "Техническая и вычислительная физика"\n')

    with patch.object(
            uunit.Fetcher,
            'get_group_schedule',
            return_value=get_from_sample('uunit/group_schedule.json')
    ):
        request = get_from_sample('requests/schedule/tomorrow.json')
        response = main.handler(request, None)

    actual = get_response_text(response)

    assert actual == expected


def test_by_date() -> None:
    expected = ('Расписание занятий на пятницу, двенадцатое апреля:\n'
                'Первая пара - Практика (семинар) - "Высшая математика"\n'
                'Вторая пара - Практика (семинар) - "Высшая математика"\n'
                'Четвертая пара - Лекция - "Основы проектной деятельности"\n'
                'Пятая пара - Практика (семинар) - "Основы саморазвития"\n')

    with patch.object(
            uunit.Fetcher,
            'get_group_schedule',
            return_value=get_from_sample('uunit/group_schedule.json')
    ):
        request = get_from_sample('requests/schedule/date.json')
        response = main.handler(request, None)

    actual = get_response_text(response)

    assert actual == expected


def test_by_date_2() -> None:
    expected = ('Расписание занятий на четверг, двадцать второе февраля:\n'
                'Третья пара - Практика (семинар) - "Иностранный язык"\n'
                'Четвертая пара - Лекция - "История России"\n'
                'Пятая пара - Физвоспитание - "Физическая культура и спорт"\n')

    with patch.object(
            uunit.Fetcher,
            'get_group_schedule',
            return_value=get_from_sample('uunit/group_schedule.json')
    ):
        request = get_from_sample('requests/schedule/date2.json')
        response = main.handler(request, None)

    actual = get_response_text(response)

    assert actual == expected


def test_non_exist_day() -> None:
    expected = 'Извини, не расслышал, повтори еще раз'

    request = get_from_sample('requests/schedule/not_exist_day.json')
    response = main.handler(request, None)

    actual = get_response_text(response)

    assert actual == expected


def test_empty() -> None:
    expected = 'Привет! Давай я посмотрю расписание УУНИТа для тебя? Задай свой вопрос'

    request = get_from_sample('requests/empty.json')
    response = main.handler(request, None)

    actual = get_response_text(response)

    assert actual == expected


@freeze_time("2024-02-16")
def test_tuesday() -> None:
    expected = ('Расписание занятий на вторник, двадцатое февраля:\n'
                'Третья пара - Лекция - "Карьера: проектирование и управление"\n'
                'Четвертая пара - Лекция - "Техническая и вычислительная физика"\n'
                'Седьмая пара - Лекция - "Экология и устойчивое развитие (Green Class)"\n')

    with patch.object(
            uunit.Fetcher,
            'get_group_schedule',
            return_value=get_from_sample('uunit/group_schedule.json')
    ):
        request = get_from_sample('requests/schedule/tuesday.json')
        response = main.handler(request, None)

    actual = get_response_text(response)

    assert actual == expected


def test_today_request_without_stub() -> None:
    request = get_from_sample('requests/schedule/today_room.json')
    response = main.handler(request, None)

    actual = get_response_text(response)

    assert 'Расписание занятий' in actual or 'Поздравляю!' in actual


def test_fetcher_error() -> None:
    with patch.object(
            uunit.Fetcher,
            'get_group_schedule',
            return_value=get_from_sample('uunit/group_schedule.json')
    ) as method:
        method.side_effect = uunit.FetcherException()
        request = get_from_sample('requests/schedule/today_room.json')
        response = main.handler(request, None)

    actual = get_response_text(response)

    assert actual == 'Произошла ошибка, попробуй еще раз!'


def test_first_lesson_date() -> None:
    with patch.object(
            uunit.Fetcher,
            'get_group_schedule',
            return_value=get_from_sample('uunit/group_schedule.json')
    ):
        request = get_from_sample('requests/first_lesson/date.json')
        response = main.handler(request, None)

    actual = get_response_text(response)

    assert actual == 'Вторник, двадцать седьмое февраля, занятия начинаются в 11:35, третья пара'


@freeze_time("2024-02-19")
def test_first_lesson_in_saturday_free() -> None:
    with patch.object(
            uunit.Fetcher,
            'get_group_schedule',
            return_value=get_from_sample('uunit/group_schedule.json')
    ):
        request = get_from_sample('requests/first_lesson/saturday.json')
        response = main.handler(request, None)

    actual = get_response_text(response)

    assert actual == 'Поздравляю! В этот день вы можете спать спокойно. Занятий не будет!'


@freeze_time("2024-02-16")
def test_first_lesson_in_saturday_tomorrow() -> None:
    with patch.object(
            uunit.Fetcher,
            'get_group_schedule',
            return_value=get_from_sample('uunit/group_schedule.json')
    ):
        request = get_from_sample('requests/first_lesson/saturday.json')
        response = main.handler(request, None)

    actual = get_response_text(response)

    assert actual == 'Завтра занятия начинаются в 11:35, третья пара'


@freeze_time("2024-02-12")
def test_first_lesson_in_saturday() -> None:
    with patch.object(
            uunit.Fetcher,
            'get_group_schedule',
            return_value=get_from_sample('uunit/group_schedule.json')
    ):
        request = get_from_sample('requests/first_lesson/saturday.json')
        response = main.handler(request, None)

    actual = get_response_text(response)

    assert actual == 'Суббота, семнадцатое февраля, занятия начинаются в 11:35, третья пара'


@freeze_time("2024-02-13")
def test_first_lesson_tomorrow() -> None:
    with patch.object(
            uunit.Fetcher,
            'get_group_schedule',
            return_value=get_from_sample('uunit/group_schedule.json')
    ):
        request = get_from_sample('requests/first_lesson/tomorrow.json')
        response = main.handler(request, None)

    actual = get_response_text(response)

    assert actual == 'Завтра занятия начинаются в 08:00, первая пара'


@freeze_time("2024-02-13")
def test_first_lesson_today() -> None:
    with patch.object(
            uunit.Fetcher,
            'get_group_schedule',
            return_value=get_from_sample('uunit/group_schedule.json')
    ):
        request = get_from_sample('requests/first_lesson/today.json')
        response = main.handler(request, None)

    actual = get_response_text(response)

    assert actual == 'Сегодня занятия начинаются в 11:35, третья пара'


@freeze_time("2024-02-13")
def test_first_lesson_no_timeslot() -> None:
    with patch.object(
            uunit.Fetcher,
            'get_group_schedule',
            return_value=get_from_sample('uunit/group_schedule.json')
    ):
        request = get_from_sample('requests/first_lesson/without_timeslot.json')
        response = main.handler(request, None)

    actual = get_response_text(response)

    assert actual == 'Сегодня занятия начинаются в 11:35, третья пара'
