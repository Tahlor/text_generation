import os

def make_dir(path):
    try:
        os.makedirs(path)
    except:
        pass