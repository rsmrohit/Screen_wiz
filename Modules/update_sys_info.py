import json

# Every time an update is made entire file is changed - could use optimization


def update(key, value):
    """Stores system information in JSON format with \
    key and value which can be any object"""
    sys_info = {}
    with open("Modules/info.json", 'r') as openfile:
        sys_info = json.load(openfile)
    sys_info[key] = value
    with open("Modules/info.json", "w") as outfile:
        json.dump(sys_info, outfile)


def get(key):

    with open("Modules/info.json", 'r') as openfile:
        sys_info = json.load(openfile)
        if key in sys_info:
            return sys_info[key]
        return None
