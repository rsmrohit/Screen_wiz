import osascript
import re
from Modules import tts, dump

keywords = ["volume"]


def run():

    # THERE IS AN EASIER WAY TO DO THIS WITH NEWER SQL IMPLEMENTATIOn
    _, __, tag, msg = dump.get_logs(start=0)[0]
    logs = dump.get_logs(start=0, amt=2)
    i = 0
    for log in logs:
        tag, msg = log[2:]
        i += 1

        if tag == "voice":
            break

    if "volume" not in msg or tag != "voice":
        return "error"

    current_vol = get_vol()
    if "increase" in msg or "more" in msg:
        tts.say("increasing volume")
        new_vol = min(100, current_vol + 20, current_vol + 10)

    elif "decrease" in msg or "less" in msg:
        tts.say("decreasing volume")
        new_vol = max(0, current_vol - 20, current_vol - 10)

    osascript.osascript("set volume output volume "+str(new_vol))

    return "exit"


def get_vol():
    current_vol = osascript.osascript("get volume settings")[1]
    current_vol = int(re.search('([0-9]+),*', current_vol)[:-1])
    return current_vol
