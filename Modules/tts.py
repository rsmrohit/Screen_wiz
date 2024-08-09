import os
from Modules import update_sys_info as usi, dump


def say(message):
    usi.update("can_record", False)
    print("TTS TEST", usi.get("can_record"))
    os.system("say " + message)
    usi.update("can_record", True)
    print("TTS TEST", usi.get("can_record"))

    dump.add("tts", message)
