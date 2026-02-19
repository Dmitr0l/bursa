import json

MSG_JOIN = "join" 
MSG_WELCOME = "welcome" 
MSG_INPUT = "input"
MSG_SNAPSHOT = "snap" 

def encode(msg_type, **kwargs):
    kwargs["type"] = msg_type
    return json.dumps(kwargs).encode('utf-8')

def decode(raw_data):
    try:
        return json.loads(raw_data.decode('utf-8'))
    except:
        return None