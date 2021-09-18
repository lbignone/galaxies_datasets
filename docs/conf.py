"""Sphinx configuration."""
from datetime import datetime


project = "Galaxies Datasets"
author = "Lucas Bignone"
copyright = f"{datetime.now().year}, {author}"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "sphinx_rtd_theme",
    "sphinx.ext.autosectionlabel",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "sphinx_rtd_theme"
