import os
from Modules import update_sys_info as usi, dump

keywords = ['say']


def run():
    say(dump.get_logs()[0][2])


def say(message):
    usi.update("can_record", False)
    # print("TTS TEST", usi.get("can_record"))
    os.system(f'echo """{message}""" | say ')
    usi.update("can_record", True)
    # print("TTS TEST", usi.get("can_record"))

    dump.log_event("tts", message)
