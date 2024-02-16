import json

from freezegun import freeze_time

import main


def get_request_from_sample(name: str) -> dict:
    with open(f'tests/samples/{name}', 'r') as data_file:
        json_data = data_file.read()

    return json.loads(json_data)


def get_response_text(data: dict) -> str:
    return data['response']['text']


@freeze_time("2024-02-16")
def test_weekday_by_auditory():
    expected = ('Расписание занятий на понедельник, девятнадцатое февраля:\n'
                'Первая пара - "7-401"\n'
                'Вторая пара - "Спортивный зал"\n'
                'Третья пара - "7-206"\n')

    request = get_request_from_sample('sample1.json')
    response = main.handler(request, None)
    actual = get_response_text(response)

    assert actual == expected


@freeze_time("2024-02-16")
def test_today_by_auditory():
    expected = ('Расписание занятий на сегодня\n'
                'Первая пара - "9-403"\n'
                'Вторая пара - "9-403"\n'
                'Третья пара - "7-406"\n'
                'Четвертая пара - "7-204"\n')

    request = get_request_from_sample('sample2.json')
    response = main.handler(request, None)
    actual = get_response_text(response)

    assert actual == expected


@freeze_time("2024-02-16")
def test_tomorrow():
    expected = ('Расписание занятий на завтра\n'
                'Третья пара - Лабораторная работа - "Техническая и вычислительная физика"\n'
                'Третья пара - Лабораторная работа - "Техническая и вычислительная физика"\n'
                'Четвертая пара - Лабораторная работа - "Техническая и вычислительная физика"\n'
                'Четвертая пара - Лабораторная работа - "Техническая и вычислительная физика"\n')

    request = get_request_from_sample('sample3.json')
    response = main.handler(request, None)
    actual = get_response_text(response)

    assert actual == expected


def test_by_date_test():
    expected = ('Расписание занятий на пятницу, двенадцатое апреля:\n'
                'Первая пара - Практика (семинар) - "Высшая математика"\n'
                'Вторая пара - Практика (семинар) - "Высшая математика"\n'
                'Четвертая пара - Лекция - "Основы проектной деятельности"\n'
                'Пятая пара - Практика (семинар) - "Основы саморазвития"\n')

    request = get_request_from_sample('sample4.json')
    response = main.handler(request, None)
    actual = get_response_text(response)

    assert actual == expected


def test_by_date_2_test():
    expected = ('Расписание занятий на четверг, двадцать второе февраля:\n'
                'Третья пара - Практика (семинар) - "Иностранный язык"\n'
                'Четвертая пара - Лекция - "История России"\n'
                'Пятая пара - Физвоспитание - "Физическая культура и спорт"\n')

    request = get_request_from_sample('sample5.json')
    response = main.handler(request, None)
    actual = get_response_text(response)

    assert actual == expected


def test_non_exist_day():
    expected = 'Извини, не расслышал, повтори еще раз'

    request = get_request_from_sample('not_exist_day.json')
    response = main.handler(request, None)
    actual = get_response_text(response)

    assert actual == expected


def test_empty():
    expected = 'Привет! Давай я посмотрю расписание УУНИТа для тебя? Задай свой вопрос'

    request = get_request_from_sample('empty.json')
    response = main.handler(request, None)
    actual = get_response_text(response)

    assert actual == expected


def test_tuesday():
    expected = ('Расписание занятий на вторник, двадцатое февраля:\n'
                'Третья пара - Лекция - "Карьера: проектирование и управление"\n'
                'Четвертая пара - Лекция - "Техническая и вычислительная физика"\n'
                'Седьмая пара - Лекция - "Экология и устойчивое развитие (Green Class)"\n')

    request = get_request_from_sample('tuesday.json')
    response = main.handler(request, None)
    actual = get_response_text(response)

    assert actual == expected
