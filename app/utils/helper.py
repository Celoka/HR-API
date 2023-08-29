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
