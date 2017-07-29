import vim
import time
import random

ESCAPE_CHAR = 27

def gitgrep():
    while(True):
        try:
            vim.command('let inputchar = nr2char(getchar())')
            char = vim.eval('inputchar')
            # Handle escape
            if char == None or char == '':
                continue
            if ord(char) == ESCAPE_CHAR:
                break
            vim.current.buffer[0] = char
            vim.command('redraw!')
        except KeyboardInterrupt:
            break
