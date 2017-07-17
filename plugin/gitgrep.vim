if !has('python3')
    echo "No Python for you..."
    finish
endif

python3 import sys
python3 import vim
python3 sys.path.append(vim.eval('expand("<sfile>:h")'))


function! GitGrep()
python3 << endOfPython

import gitgrep
gitgrep.gitgrep()

endOfPython
endfunction

" --------------------------------
"  Expose our commands to the user
" --------------------------------
command! GitGrep call GitGrep()
