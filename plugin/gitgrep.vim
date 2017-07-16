if !has('python3')
    echo "No Python for you..."
    finish
endif

python3 import sys
python3 import vim
python3 sys.path.append(vim.eval('expand("<sfile>:h")'))
python3 import gitgrep
