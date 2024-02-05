# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys
import django
sys.path.insert(0, os.path.abspath('../..'))  # Adjust the relative path based on your project structure
os.environ['DJANGO_SETTINGS_MODULE'] = 'tpGL.settings'  # Replace with your actual settings module

django.setup()

project = 'CRTL F Engine'
copyright = '2023, CTRL F Team '
author = ' CTRL F Team'
release = '2023/2024'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
        'sphinx.ext.autodoc',
    # Add other extensions as needed
]

templates_path = ['_templates']
exclude_patterns = []


language = 'english'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'renku'
html_static_path = ['_static']