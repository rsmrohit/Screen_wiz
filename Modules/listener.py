import argparse
import queue
import sys
import sounddevice as sd
import json
from vosk import Model, KaldiRecognizer
from Modules import update_sys_info as usi, dump

q = queue.Queue()


def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    if usi.get("can_record"):
        q.put(bytes(indata))


device_info = sd.query_devices(kind="input")
samplerate = int(device_info["default_samplerate"])
model = Model(lang="en-us")

usi.update("can_record", True)


def run(conn=None):
    global dump
    try:
        with sd.RawInputStream(samplerate=samplerate, blocksize=8000,
                               dtype="int16", channels=1, callback=callback):

            rec = KaldiRecognizer(model, samplerate)
            text = ""
            while True:
                data = q.get()

                if rec.AcceptWaveform(data):

                    new_text = json.loads(rec.Result())["text"]

                    if new_text != text:
                        text = new_text
                        # dump.log_event("listener", text) # TODO: Separate log for listener

                        if conn:
                            conn.send(text)

                elif "stop" in json.loads(rec.PartialResult())["partial"]:
                    break
    except KeyboardInterrupt:
        print("Done")
    if conn:
        conn.send("exit")
        conn.close()


if __name__ == "__main__":
    run()
