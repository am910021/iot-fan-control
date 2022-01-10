import sys

def unloadModule(mod):
    # removes module from the system
    mod_name = mod.__name__
    if mod_name in globals():
        del globals()[mod_name]

