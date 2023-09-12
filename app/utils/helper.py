import os
from dotenv import load_dotenv

load_dotenv()

def conflict_handler(msg, field):
    data = {
        "msg": msg,
        "field": field
    }
    return data


def get_env(key):
    try:
        return os.environ[key]
    except Exception as e:
        print(f'{type(e).__name__}: {e}')

def parse_leave_request_object(leave_request_obj):
    result = leave_request_obj.serialize()
    result['firstName'] = leave_request_obj.user.first_name
    result['lastName'] = leave_request_obj.user.last_name
    result['emailAddress'] = leave_request_obj.user.email_address
    return result

def remove_password(obj):
    del obj['password']
    return obj


def parse_calendar_events(model_obj):
    event = model_obj.serialize()
    return {
        'title': event['eventType'],
        'start': event['leaveStart'],
        'end': event['leaveEnd']
    }
