
## Compiling book

~~~ bash
git clone git@github.com:kosl/ihipp-examples.git
git checkout book
cd docs/
python3 -m venv local
local/bin/pip install --upgrade pip
local/bin/pip install sphinx_rtd_theme
local/bin/pip install --upgrade myst-parser

~~~