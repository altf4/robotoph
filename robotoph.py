#!/usr/bin/python3
import os
import imp
import inspect
import fnmatch

import melee
import pygame


pygame.init()
console = melee.Console(slippi_address='127.0.0.1',
                        slippi_port=51441)

print("Connecting to console...")
if not console.connect():
    print("Could not connect to Slippi. Is it running?")
    sys.exit(1)
print("Connected")

triggers = []

def load_all_triggers():
    dir_path = os.path.dirname(os.path.realpath(__file__)) + "/triggers/"
    pattern = "*.py"
    for path, subdirs, files in os.walk(dir_path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                found_module = imp.find_module(name[:-3], [path])
                module = imp.load_module(name, found_module[0], found_module[1], found_module[2])
                for mem_name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj) and inspect.getmodule(obj) is module:
                        triggers.append(obj())

load_all_triggers()

while True:
    gamestate = console.step()
    for trigger in triggers:
        trigger.check(gamestate)
