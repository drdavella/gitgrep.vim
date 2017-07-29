import vim
import time
import random

def gitgrep():
    while(True):
        vim.command('let inputchar = nr2char(getchar())')
        char = vim.eval('inputchar')
        print(char)

