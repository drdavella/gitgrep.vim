import vim
import time
import random

def gitgrep():
    while(True):
        vim.command('let inputchar = nr2char(getchar())')
        char = vim.eval('inputchar')
        # Handle escape
        if ord(char) == 27:
            break
        vim.current.buffer[0] = char
        vim.command('redraw!')
