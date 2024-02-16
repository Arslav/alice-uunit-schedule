import json


def _get_teacher_name(item: dict) -> str:
    teacher_name = None
    if 'teacher_fullname' in item:
        teacher_name = str(item['teacher_fullname']).split()[0]
    elif 'teacher' in item and not item['teacher_id'] == 0:
        teacher_name = str(item['teacher']).split()[0]
    return teacher_name


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
    
    def __init__(self, week, weekday):
        self.week = week + 18
        self.weekday = weekday

    def _is_current_day_item(self, item):
        return str(self.week) in item['schedule_weeks'] and item['schedule_weekday_id'] == self.weekday

    def parse(self):
        schedule = []

        #TODO: Сделать загрузку файла
        with open('tests/data.json', 'r') as data_file:
            json_data = data_file.read()

        data = json.loads(json_data)

        for item in data:
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
