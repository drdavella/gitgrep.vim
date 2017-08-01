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
    current_line = _run_and_return('line(".")')
    current_col = _run_and_return('col(".")')
    top_line = _run_and_return('line("w0")')
    return (current_line, current_col, top_line)

def _set_cursor(line, col):
    vim.command('call cursor({}, {})'.format(line, col))

def _restore_screen_state(screen_state):
    vim.command('bdelete!')
    current_line, current_col, top_line = screen_state
    _set_cursor(top_line, 1)
    vim.command('normal! zt')
    _set_cursor(current_line, current_col)

def _get_user_input():
    return _run_and_return('nr2char(getchar())')

def _display_and_handle(results):
    # Open new buffer
    vim.command('enew')
    # Populate buffer with results
    vim.current.buffer[:] = results
    vim.command('redraw!')
    # Set the cursor position
    _set_cursor(1, 1)
    vim.command('normal! zt')

    current_line = 0
    max_line = len(results) - 1

    while(True):
        try:
            char = _get_user_input()
            # Handle escape
            if char == None or char == '':
                continue
            elif char == 'q' or ord(char) == ESCAPE_CHAR:
                break
            elif char == 'j' and current_line > 0:
                current_line -= 1
            elif char == 'k' and current_line < max_line:
                current_line += 1
            _set_cursor(current_line, 1)
        except KeyboardInterrupt:
            break

def gitgrep():
    results = _run_gitgrep()
    if not results:
        return

    screen_state = _save_screen_state()
    _display_and_handle(results)
    _restore_screen_state(screen_state)
