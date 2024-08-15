import os
import pytesseract
from Modules import dump, tts
import numpy as np
from PIL import Image


keywords = ["read"]


def run():

    tag, msg = ("", "")
    imgtag, imgmsg = ("", "")

    # Get the exacty message with
    for log in dump.get_logs(start=0, amt=5):

        if log[2] == "voice" and tag == "":
            tag, msg = log[2:]

        if log[2] == "img" and imgtag == "":
            imgtag, imgmsg = log[2:]

    if not imgmsg.endswith('jpg'):
        dump.log_event('reader', 'no image given to read')
        tts.say("Please save screenshot before reading")
        return

    img = np.array(Image.open(imgmsg))
    text = pytesseract.image_to_string(img)
    dump.log_event('reader', text)


def log_text(img):
    img = np.array(Image.open(img))
    text = pytesseract.image_to_string(img)
    dump.log_event('reader', text)


def get_objects(img):
    img = np.array(Image.open(img))
    dicts = pytesseract.image_to_data(img)
    return dicts
