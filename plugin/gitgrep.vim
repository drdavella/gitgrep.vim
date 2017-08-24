if !has('python3')
    echo "No Python for you..."
    finish
endif

python3 import sys
python3 import vim
python3 sys.path.append(vim.eval('expand("<sfile>:h")'))


function! GitGrep(pattern)
python3 << endOfPython

import gitgrep
gitgrep.gitgrep(vim.eval('a:pattern'))

endOfPython
endfunction

" --------------------------------
"  Expose our commands to the user
" --------------------------------
command! -nargs=1 GitGrep call GitGrep(<f-args>)
