from functools import cache

import requests as requests


def _get_teacher_name(item: dict) -> str:
    teacher_name = None
    if 'teacher_fullname' in item:
        teacher_name = str(item['teacher_fullname']).split()[0]
    elif 'teacher' in item and not item['teacher_id'] == 0:
        teacher_name = str(item['teacher']).split()[0]
    return teacher_name


class FetcherException(Exception):
    pass


class Fetcher:
    host: str = 'https://dev.uust-time.ru/api/v/742198/'
    site: str = 'uust-time'
    headers: dict = {
        'Origin': 'https://uust-time.ru'
    }

    @cache
    def get_groups(self):
        return self._request('GET', self.host + f'groups?site={self.site}')

    @cache
    def get_departments(self):
        return self._request('GET', self.host + f'departments?site={self.site}')

    @cache
    def get_teachers(self):
        return self._request('GET', self.host + f'teachers?site={self.site}')

    @cache
    def get_organizations(self):
        return self._request('GET', self.host + f'organizations?site={self.site}')

    @cache
    def get_group_schedule(self, group_id=4381, semester_id=232):
        return self._request('GET', self.host + f'schedule/0/{group_id}/semester/{semester_id}?site={self.site}')

    def _request(self, method: str, url: str, *, params=None, data=None) -> dict:
        try:
            response = requests.request(method, url, params=params, data=data, headers=self.headers)
            if not response.status_code == 200:
                raise FetcherException(response.reason)

            return response.json()
        except Exception:
            raise FetcherException()


class Parser:
    _pairTimes = {
        '08:00-09:20': 1,
        '09:35-10:55': 2,
        '11:35-12:55': 3,
        '13:10-14:30': 4,
        '15:10-16:30': 5,
        '16:45-18:05': 6,
        '18:20-19:40': 7,
    }

    def __init__(self, data, week, weekday):
        self.data = data
        self.week = week + 18
        self.weekday = weekday

    def _is_current_day_item(self, item) -> bool:
        return str(self.week) in item['schedule_weeks'] and item['schedule_weekday_id'] == self.weekday

    def parse(self) -> list[tuple]:
        schedule = []

        for item in self.data:
            if self._is_current_day_item(item):
                schedule.append((
                    self._pairTimes[item['schedule_time_title']],
                    item['schedule_subject_title'],
                    item['room_title'],
                    _get_teacher_name(item),
                    item['type']
                ))

        schedule.sort(key=lambda a: a[0])

        return schedule
