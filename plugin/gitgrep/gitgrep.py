import vim
import time
import random
from subprocess import Popen, PIPE
from collections import OrderedDict

from .displaytree import DisplayTree


ESCAPE_CHAR = 27
GIT_CMD = ['git', '--no-pager']

def _run_and_return(command):
    varname = 'tempvar'
    vim.command('let {} = {}'.format(varname, command))
    return vim.eval(varname)

def _find_top_level():
    command = GIT_CMD + ['rev-parse', '--show-toplevel']
    result = Popen(command, stdout=PIPE, stderr=PIPE)
    if result.wait() != 0:
        return None
    top_dir = result.stdout.read()
    return top_dir.strip()

def _run_gitgrep(git_dir, pattern):
    command = GIT_CMD + ['grep', '-e', pattern, '--', git_dir]
    result = Popen(command, stdout=PIPE, stderr=PIPE)
    if result.wait() != 0:
        return None
    string = result.stdout.read()
    return [x.decode('utf-8') for x in string.splitlines()]

def _process_results(result_list):
    results = OrderedDict()

    for item in result_list:
        # Make sure not to split on colons in the actual source line
        filename, lineno, content = item.split(':', maxsplit=2)
        if filename not in results:
            results[filename] = list()
        results[filename].append((lineno, content))
    return results

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

def _highlight_term(pattern):
    vim.command("highlight GitGrepMatch ctermbg=red guibg=red")
    vim.command("match GitGrepMatch /{}/".format(pattern))

def _display_result_file(pattern, filename, line):
    vim.command('e +{} {}'.format(line, filename))
    #_highlight_term(pattern)

def _get_user_input():
    return _run_and_return('nr2char(getchar())')

def _add_line_marker(text):
    space = '  ' if text.startswith('    ') else ''
    return "\u25b6 {}{}".format(space, text.lstrip())

def _display_and_handle(pattern, results):
    # Open new buffer
    vim.command('enew')
    vim.command('setlocal buftype=nofile')
    vim.command('file GitGrep:\ pattern={}'.format(pattern))

    dt = DisplayTree(results)
    dt.display()

    index = 0
    # Populate buffer with results
    current_line = vim.current.buffer[index]
    vim.current.buffer[index] = _add_line_marker(vim.current.buffer[index])

    vim.command('silent! /{}'.format(pattern))
    _set_cursor(1, 1)
    vim.command('normal! zt')
    vim.command('setlocal wrap!')
    vim.command('setlocal cursorline')
    vim.command('redraw!')

    while(True):
        try:
            closing = None
            char = _get_user_input()
            last_index = index
            last_line = current_line
            redraw = False
            # Handle escape
            if char == None or char == '':
                continue
            elif char == 'q' or ord(char) == ESCAPE_CHAR:
                break
            elif char == 'j' and index < dt.max_line:
                index += 1
            elif char == 'k' and index > 0:
                index -= 1
            elif ord(char) == 0x0d:
                result = dt.process(last_index)
                if result:
                    return result

                redraw = True
            # No update if no change
            if not redraw and last_index == index:
                continue

            current_line = vim.current.buffer[index]
            vim.current.buffer[last_index] = last_line
            vim.current.buffer[index] = _add_line_marker(current_line)
            _set_cursor(index+1, 1)
            # Do not clear screen in an effort to improve performance
            vim.command('redraw')
        except KeyboardInterrupt:
            break

    return None

def gitgrep(pattern):

    git_dir = _find_top_level()
    if git_dir is None:
        return

    result_list = _run_gitgrep(git_dir, pattern)
    if not result_list:
        return

    results = _process_results(result_list)

    screen_state = _save_screen_state()
    location = _display_and_handle(pattern, results)
    _restore_screen_state(screen_state)

    if location is None:
        return

    filename, line = location
    _display_result_file(pattern, filename, line)
