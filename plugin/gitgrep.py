import vim
import time
import random

def gitgrep():
    while(True):
        char = vim.command('call nr2char(getchar())')
        print(char)

