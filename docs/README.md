
## Compiling book

### gpu02 login node

~~~ bash
git clone git@github.com:kosl/ihipp-examples.git
git checkout book
cd docs/
python3 -m venv local
local/bin/pip install --upgrade pip
local/bin/pip install sphinx_rtd_theme
local/bin/pip install --upgrade myst-parser
source local/bin/activate

make html
make latexpdf
~~~

### bison server

~~~ bash
module load python-3.7.4-gcc-8.3.0-voruwiu
module load texlive-20200406-gcc-8.3.0-oranjyk

git clone git@github.com:kosl/ihipp-examples.git
git checkout book
cd docs/
python3 -m venv local
local/bin/pip install --upgrade pip
local/bin/pip install sphinx_rtd_theme
local/bin/pip install --upgrade myst-parser
source local/bin/activate

make html
make latexpdf
~~~