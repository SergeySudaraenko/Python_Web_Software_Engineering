import os
import sys
sys.path.insert(0, os.path.abspath('../contacts_api/app'))




project = 'TEST'
copyright = '2024, SERG'
author = 'SERG'
release = '1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [ 'sphinx.ext.autodoc',
    'sphinx_autodoc_typehints',]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
