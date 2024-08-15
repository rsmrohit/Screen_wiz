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

    diff = 50 if "lot" in msg else 30

    current_vol = get_vol()
    new_vol = current_vol
    if "increase" in msg:
        tts.say("increasing volume")
        new_vol = min(100, current_vol + diff, current_vol + diff/2)

    elif "decrease" in msg:
        tts.say("decreasing volume")
        new_vol = max(0, current_vol - diff, current_vol - diff/2)

    osascript.osascript("set volume output volume "+str(new_vol))

    return


def get_vol():
    current_vol = osascript.osascript("get volume settings")[1]
    current_vol = int(re.search('([0-9]+),*', current_vol)[0][:-1])
    return current_vol
