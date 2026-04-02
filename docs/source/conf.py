import os
import sys

from sphinx.application import Sphinx
from sphinx.transforms import SphinxContentsFilter

sys.path.insert(0, os.path.abspath("../.."))  # important for autodoc

# Configuration file for the Sphinx documentation builder.
# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
project = "PAGOZA"
copyright = "2026, Jelle Bonthuis; Tim Dick"
author = "Jelle Bonthuis; Tim Dick"
release = "1.0.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"

language = "en"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autosummary",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    # add nbsphinx here
    "nbsphinx",
]

napoleon_custom_sections = [
    ("Requires", "params_style"),
    ("Modifies", "params_style"),
]
napoleon_use_param = False
napoleon_use_rtype = False
# set autodoc to always show private _methods
autodoc_default_options = {
    "private-members": True,
    "autodoc_class_signature": "separated",
}
autosummary_generate = True
autosummary_generate_overwrite = True
autodoc_member_order = "bysource"
autodoc_preserve_defaults = True

# html_theme = "furo"
html_permalinks = False
html_last_updated_fmt = "%b %d, %Y"

html_static_path = ["_static"]
html_css_files = ["custom.css"]
templates_path = ["_templates"]

# # -- Custom Documenter to skip function headers -----------------------------
import re  # noqa: E402

from docutils import nodes  # noqa: E402
from sphinx import addnodes  # noqa: E402
from sphinx.environment.collectors.title import TitleCollector  # noqa: E402
from sphinx.ext.autodoc import (  # noqa: E402
    ClassDocumenter,
    DataDocumenter,
    FunctionDocumenter,
)


def process_doc(self, app: Sphinx, doctree: nodes.document) -> None:
    """Add a title node to the document (just copy the first section title),
    and store that title in the environment.
    """
    titlenode = nodes.title()
    longtitlenode = titlenode
    # explicit title set with title directive; use this only for
    # the <title> tag in HTML output
    if "title" in doctree:
        longtitlenode = nodes.title()
        longtitlenode += nodes.Text(doctree["title"])
    # look for first section title and use that as the title
    for node in doctree.findall(nodes.section):
        visitor = SphinxContentsFilter(doctree)
        node[0].walkabout(visitor)
        titlenode += visitor.get_entry_text()  # type: ignore[no-untyped-call]
        break
    else:
        # document has no title
        # Added by Jelle Bonthuis 2025-06-17 to handle caes where no section title is found
        # but we want to not use <no title>
        desc_signatures = list(doctree.traverse(addnodes.desc_signature))
        if desc_signatures:
            for sig in desc_signatures:
                match = re.search(r'_toc_name="([^"]*)"', str(sig))
                if match:
                    value = match.group(1)
                    titlenode += nodes.Text(value)
                    break
        else:
            titlenode += nodes.Text(doctree.get("title", "<no title>"))
    app.env.titles[app.env.docname] = titlenode
    app.env.longtitles[app.env.docname] = longtitlenode


TitleCollector.process_doc = process_doc


def setup(app):
    # app.add_autodocumenter(TitleClassDocumenter, override=True)
    # app.add_autodocumenter(NoHeaderFunctionDocumenter, override=True)
    # app.add_autodocumenter(NoHeaderDataDocumenter, override=True)
    pass
