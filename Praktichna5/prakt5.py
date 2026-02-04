import json
import os


def save_state(path, state):
    try:
        tmp = path + ".tmp"
        f = open(tmp, "w")
        json.dump(state, f, indent=2)
        f.close()
        os.replace(tmp, path)
        return True
    except:
        return False


def load_state(path, default):
    if not os.path.exists(path):
        return default.copy()

    try:
        f = open(path, "r")
        data = json.load(f)
        f.close()
    except:
        return default.copy()

    if type(data) != dict:
        return default.copy()

    result = default.copy()

    for key in default:
        if key in data:
            result[key] = data[key]

    return result