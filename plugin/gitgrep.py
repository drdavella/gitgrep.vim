import vim
import time
import random

def gitgrep():
    while(True):
        char = vim.command('let gitgrep:char nr2char(getchar())')
        print('vars:',vim.vars.get('gitgrep:char'))
        print('vvars:',vim.vvars.get('gitgrep:char'))

