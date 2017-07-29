import vim
import time
import random

def gitgrep():
    while(True):
        char = vim.command('let inputchar = nr2char(getchar())')
        print('vars:',vim.vars.get('inputchar'))
        print('vvars:',vim.vvars.get('inputchar'))

