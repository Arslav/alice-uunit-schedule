from application import Application

app = Application()


def handler(event, context) -> dict:
    text = app.hello()

    request = event.get('request', {})
    nlu = request.get('nlu', {})
    if request.get('command', None):
        text = app.intent(nlu)

    return {
        'version': event['version'],
        'session': event['session'],
        'response': {
            'text': text,
            'end_session': 'false'
        },
    }
