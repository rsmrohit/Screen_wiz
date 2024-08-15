import os
from Modules import dump

keywords = ["screenshot", "screen"]


def run():

    tag, msg = (0, 0)
    defaultsave = 'capture.jpg'

    # Get the exacty message with
    for log in dump.get_logs(start=0, amt=3):
        tag, msg = log[2:]

        if "voice" in tag and "screenshot" in msg:
            break

    configs = ['-c']

    copy = True
    if "save" in msg:
        configs = []
        copy = False
    if "part" in msg or "section" in msg:
        configs.append('-i')

    configs = " ".join(configs)

    os.system(f"screencapture {configs} {defaultsave}")
    dump.log_event('img', defaultsave if not copy else 'clipboard')
