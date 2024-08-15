import os
from Modules import dump

keywords = ["screenshot", "screen", "picture"]


def run():

    tag, msg = (0, 0)
    defaultsave = 'capture.jpg'

    # Get the exacty message with
    for log in dump.get_logs(start=0, amt=3):
        # print(log)
        tag, msg = log[2:]

        if "voice" in tag:
            break

    configs = ['screencapture', defaultsave]

    if "save" not in msg:  # I STILL SAVE IT FOR NOW EVEN THOUGH 'SAVE' ISNT THERE
        configs.insert(1, '-c')
    if "part" in msg or "section" in msg:
        configs.insert(1, '-i')

    os.system(' '.join(configs))
    print(' '.join(configs))
    dump.log_event('img', defaultsave)
