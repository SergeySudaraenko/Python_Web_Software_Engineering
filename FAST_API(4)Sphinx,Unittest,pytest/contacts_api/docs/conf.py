import os
import sys
sys.path.insert(0, os.path.abspath('../app'))


project = 'TEST'
copyright = '2024, SERG'
author = 'SERG'
release = '1'

extensions = [
    'sphinx_rtd_theme',
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

html_theme = 'sphinx_rtd_theme'

templates_path = ['_templates']
exclude_patterns = []


html_theme = 'alabaster'
html_static_path = ['_static']
