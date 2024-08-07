import os
import sys
from collections import defaultdict
from multiprocessing import Process, Pipe
import importlib

mods_dict = defaultdict()
keywords_dict = defaultdict(lambda: [])

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

if __name__ == "__main__":

    # Start listener process
    dump = open("Modules/dump.txt", 'r')
    receiver, sender = Pipe()
    listener = Process(
        target=mods_dict["listener"].run, kwargs={'conn': sender})

    listener.start()

    while listener.is_alive():

        msg = receiver.recv()
        if msg == "exit":
            listener.join()
            listener.terminate()

        if "computer" in msg:
            print("YAY")
