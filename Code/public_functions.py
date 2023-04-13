import os
import matplotlib.pyplot as plt

def create_folder(fd):
    if not os.path.exists(fd):
        os.makedirs(fd)



