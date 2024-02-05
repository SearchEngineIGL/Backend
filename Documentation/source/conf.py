# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys

sys.path.insert(0, os.path.abspath('../..'))  # Adjust the relative path based on your project structure

project = 'CRTL F Documentation'
copyright = '2023, Nesrine Abla  Hind Lyna '
author = 'Nesrine  Abla  Hind Lyna '
release = '2023/2024'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
        'sphinx.ext.autodoc',
    # Add other extensions as needed
]

templates_path = ['_templates']
exclude_patterns = ['**/migrations/*', '**/tests/*']


language = 'english'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']


