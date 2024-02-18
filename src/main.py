from application import Application

app = Application()


def handler(event, context) -> dict:
    text = app.hello()

    nlu = event.get('request', {}).get('nlu', {})
    if nlu.get('intents', {}):
        text = app.intent(nlu)

    return {
        'version': event['version'],
        'session': event['session'],
        'response': {
            'text': text,
            'end_session': 'false'
        },
    }
