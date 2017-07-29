import vim
import time
import random

def gitgrep():
    for x in range(10):
        vim.current.buffer[:] = [str(random.random()) for x in range(20)]
        vim.command('edit')
        time.sleep(2)

