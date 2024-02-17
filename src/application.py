from importlib import import_module

from intents import *


class Application:
    _intents: dict = {
        'schedule': ScheduleIntent.__name__
    }

    _helloMessage = 'Привет! Давай я посмотрю расписание УУНИТа для тебя? Задай свой вопрос'
    _defaultMessage = 'Извини, не расслышал, повтори еще раз'

    def hello(self):
        return self._helloMessage

    def intent(self, nlu: dict):
        for intent_key in nlu['intents']:
            if intent_key not in self._intents:
                continue
            class_obj = getattr(import_module('intents'), self._intents[intent_key])
            intent: AbstractIntent = class_obj(
                tokens=nlu['tokens'],
                entities=nlu['entities'],
                slots=nlu['intents'][intent_key]['slots'],
            )
            try:
                return intent.run()
            except IntentError:
                break

        return self._defaultMessage
