import os
import sys
from collections import defaultdict
from multiprocessing import Process, Pipe
import multiprocessing as mp
import importlib
import time
from Modules import tts, dump, llm

mods_dict = defaultdict()
keywords_dict = defaultdict(lambda: [])


class ButtonTimer():

    def __init__(self, idle=5, active=False):
        self.idle = idle
        self._active = active
        self.idle_time = idle+time.time()

    def activate(self):
        self._active = True
        self.idle_time = time.time() + self.idle

    def reset_timer(self):
        self.idle_time = time.time() + self.idle

    def deactivate(self):
        self._active = False

    def is_active(self):
        if time.time() > self.idle_time:
            self._active = False
        return self._active

    def __eq__(self, value: object) -> bool:
        return self.is_active() == value


# Import all modules
for py in [f[:-3] for f in os.listdir("Modules") if f.endswith('.py') and f != '__init__.py']:
    mod = importlib.import_module('Modules.' + py)
    mods_dict[py] = mod

# Store keywords for easy access, memory consumption will take a small toll
# Maybe use a db next time?
for mod_name in mods_dict:
    mod = mods_dict[mod_name]
    if hasattr(mod, "keywords"):
        for k in mod.keywords:
            keywords_dict[k] = mod_name

listening = False
if __name__ == "__main__":

    def simple_split_prompt(q):
        prompt = f"****Exercise****\n If the sentence is complex or compound, split it into simple sentences (each sentence must be followed by a '/') remember to write END once done"\
            f"\n\nSentence:'''{q}.'''"\
            f"\nAnswer: "
        return prompt

    # Clear log
    dump.clear_table()

    # Start listener process
    receiver, sender = Pipe()
    listener = Process(
        target=mods_dict["listener"].run, kwargs={'conn': sender})

    listener.start()

    # Button timer for listening
    idle_timer = ButtonTimer(idle=10)

    while listener.is_alive():

        # Receive messages from the listener,
        msg = receiver.recv()
        if msg:
            idle_timer.reset_timer()

        if msg == "exit":
            listener.join()
            listener.terminate()

        listening = idle_timer.is_active()
        # Once computer is mentioned, begin the listening process
        if "computer" in msg and not listening:
            idle_timer.activate()
            tts.say("What is up")

        elif listening:

            # cmds = llm.prompt(simple_split_prompt(msg)).split("/")
            cmds = [msg]

            for msg in cmds:
                for m in msg.split():
                    mod = keywords_dict[m]
                    if mod == []:
                        del keywords_dict[m]
                        continue

                    dump.log_event('voice', msg)
                    tts.say("running " + mod + " mod")
                    mod = mods_dict[mod]
                    mod.run()
                    print(msg)
                # break  # For now, will only do one cmd at a time

        # dump.write_to_file()
    # dump.write_to_file()
