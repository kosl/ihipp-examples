# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Introduction to parallel programming'
copyright = '2022, Leon Kos'
author = 'Leon Kos'
release = '1.0.9'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
# https://www.sphinx-doc.org/en/master/usage/markdown.html

extensions = ['myst_parser',]

myst_enable_extensions = [
    "dollarmath",
    "colon_fence",
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
# The paper size ('letterpaper' or 'a4paper').
'papersize': 'a4paper',

# The font size ('10pt', '11pt' or '12pt').
'pointsize': '11pt',

# Additional stuff for the LaTeX preamble.
# See http://tex.stackexchange.com/questions/83020/set-standard-default-scaling-of-includegraphics
# Customized header and footer
'preamble': r'\usepackage{graphicx}\setkeys{Gin}{width=.60\csname Gin@nat@width\endcsname,keepaspectratio}\fancypagestyle{normal}{\fancyhf{}\fancyfoot[LE,RO]{{\thepage}}\fancyfoot[LO]{{\nouppercase{\rightmark}}}\fancyfoot[RE]{{\nouppercase{\leftmark}}}\fancyhead[LE]{Release 1.0.9}\renewcommand{\headrulewidth}{0.4pt}\renewcommand{\footrulewidth}{0.4pt}}',

# Latex figure (float) alignment
'figure_align': 'htbp',

}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
  ('index', 'ipp.tex', u'Documentation',
   u'Leon Kos', 'book'),
]

# Number the Figures, Tables and Listings
numfig = True

math_number_all = True

# Listing font size
from sphinx.highlighting import PygmentsBridge
from pygments.formatters.latex import LatexFormatter

class CustomLatexFormatter(LatexFormatter):
    def __init__(self, **options):
        super(CustomLatexFormatter, self).__init__(**options)
        self.verboptions = r"formatcom=\scriptsize"

PygmentsBridge.latex_formatter = CustomLatexFormatter