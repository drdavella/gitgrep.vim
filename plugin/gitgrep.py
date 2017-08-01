import vim
import time
import random

ESCAPE_CHAR = 27

def _run_and_return(command):
    varname = 'tempvar'
    vim.command('let {} = {}'.format(varname, command))
    return vim.eval(varname)

def _run_gitgrep():
    # Just populate with dummy data for now
    return ['hello', 'world', 'file', 'whatever', 'blurg']

def _save_screen_state():
    vim.command('silent 1,$delete _')
    current_line = _run_and_return('line(".")')
    current_col = _run_and_return('col(".")')
    top_line = _run_and_return('line("w0")')
    return (current_line, current_col, top_line)

def _restore_screen_state(screen_state):
    vim.command('silent 1,1delete _')
    current_line, current_col, top_line = screen_state
    vim.command('call cursor({}, 1)'.format(top_line))
    vim.command('normal! zt')
    vim.command('call cursor({}, {})'.format(current_line, current_col))

def _get_user_input():
    return _run_and_return('nr2char(getchar())')

def _display_and_handle(results):
    vim.current.buffer[:] = results
    vim.command('redraw!')

    while(True):
        try:
            char = _get_user_input()
            # Handle escape
            if char == None or char == '':
                continue
            if ord(char) == ESCAPE_CHAR:
                break
            vim.current.buffer.append(char)
            vim.command('redraw!')
        except KeyboardInterrupt:
            break

def gitgrep():
    results = _run_gitgrep()
    if not results:
        return

    screen_state = _save_screen_state()
    _display_and_handle(results)
    _restore_screen_state(screen_state)
