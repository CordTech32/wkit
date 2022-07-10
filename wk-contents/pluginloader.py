import os
import sys
import importlib

for x in os.listdir("wk-contents/uploads"):
    if x.endswith(".plugin"):
        sys.path.insert(0, f"wk-contents/uploads/{x}")
def load_pl(app, plugin_name):
    plug = importlib.import_module(plugin_name.replace(".plugin",""))
    plug.setup(app)
    return plug

