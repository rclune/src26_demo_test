# Compiling the OMSF Demonstration Documentation

The docs for this project are built with [Sphinx](http://www.sphinx-doc.org/en/master/).
To compile the docs, run Sphinx via uv from the root directory of the repo:

```shell
uv run sphinx-build -j auto -b html docs docs/_build/html
```

Let's break this down:
- [uv](https://docs.astral.sh/uv/) is a Python package and project manager. 
- `uv run` runs the command(s) after this in an environment managed by uv. See the [uv documentation](https://docs.astral.sh/uv/guides/scripts/) to learn more. 
- `sphinx-build` activates [Sphinx](https://www.sphinx-doc.org/en/master/index.html), a tool for generating static documentation pages, and tells it to generate the pages based on what is in the source directory (`docs`) and place them in the output directory. 
- `-j auto` controlls the parallelism of the command, in this case because `auto` is specified, Sphinx will pick the optimial parallel processes itself. 
- `-b html` tells Sphinx to specifically generate static HTML pages - this is the most common type to generate.
- `docs` is the source directory. 
- `docs/_build/html` is the output directory where the generated HTML files will be stored

**The compiled docs will be in the `docs/_build/html/` directory and can be viewed by opening `index.html`.** You can also view the built docs by looking at the GitHub Pages site for this repository: [http://omsf.io/OMSF_docs_template/](http://omsf.io/OMSF_docs_template/)

## What's included:
Before building: 
- `_static`: a directory to contain any custom static files, see the [README](./_static/README.md) in this directory for more information.
-  `_templates`: a directory with [JINJA2 templates](https://jinja.palletsprojects.com/en/stable/templates/) that tell Sphinx what the generated API documentation should look like
- `conf.py`: This is the configuration file for the documentation. It contains any extensions that are being used to generate the documentation, any documentation themes that are being used, versioning and project information, and so much more. 
- `index.md`: This file is where you tell Sphinx what to document. It has an autosummary directive, but any hand-written documentation will need to be noted here as well. (For example, the `myst-md-demo.md` document.)
- `doc_templates`: This contains several templates to help guide your documentation writing process. See the [Documentation Templates](#documentation-templates) section below to learn more.
- `myst-md-demo.md`: Demonstrating how to use different Markdown capabilities to format and organize individual documentation pages.
- `desert-flower.jpg`: Image used in the `myst-md-demo.md` example.

After building: 
- `api/generated`: a directory containing the files Sphinx generated based on its autosummary directive. (More information on this below.)
- `_build`: a directory containing all other files Sphinx generated while building the documentation. Most notably, `_build/html` will have all of the static HTML files that were created.

## Documentation Templates

The `docs/doc_templates` folder contains several templates to help you think about and organize your external documentation. With some exceptions, using these is as simple as 
1. Copying them into the `docs` directory
1. Renaming the file (you probably want to remove the 'template' part of the file name)
1. Filling out what you would like to put there 
1. Listing them in `docs/index.md` so that they appear in the table of contents in your external documentation 

There are a few exceptions:
1. The README_template.md should be copied to your root directory (or anywhere else a README would be useful). Notice that `docs/index.md` already includes the README in the root directory.
1. If you have automatically generated API documentation you likely do not need to use the reference_table.md template. This is just an example of how to make a nicely formatted table in Markdown and is useful for if your tool usage does not rely on the API. 
1. There are two different templates in `docs/doc_templates/tutorial_templates` depending on how you would like to showcase your tutorial:
    - As a markdown file
    - As a python notebook, this [tutorial](https://docs.readthedocs.com/platform/latest/guides/jupyter.html) is a great resource for learning how to embed notebooks into your documentation. 

## Hosting the documentation...
The pages generated using the command above are static HTML pages, for others to view them they need to be *hosted* somewhere. Here are a few options for hosting your docs: 

### Using Read the Docs
A configuration file for [Read The Docs](https://readthedocs.org/) (readthedocs.yaml) is included in the top level of the repository. To use Read the Docs to host your documentation, go to https://readthedocs.org/ and connect this repository. *You may need to change your default branch to `main` under Advanced Settings for the project.*

### Using GitHub Pages
You will need to create a workflow (you can find an example [here](https://github.com/omsf/OMSF_docs_template/blob/main/.github/workflows/documentation.yml)) to deploy your documentation to a GitHub pages site and then adjust the settings in your repository to have them automatically update when changes are made to the main branch. This [tutorial](https://coderefinery.github.io/documentation/gh_workflow/) outlines the steps, though the workflow can be made much more sophsticated based on your project's needs. Learn more about GitHub workflows [here](https://docs.github.com/en/actions/how-tos/write-workflows). 

## Automatic API Documentation
A configuration for automatically documenting [OpenFF](https://openforcefield.org/) software (as an example) with AutoSummary is included. The project is processed and documented as follows:

A module (or package) is documented if and only if it satisfies **all** the following criteria:
1. Its parent module is documented, or it is the root module.
2. It is public (ie, its name does not begin with an underscore).
3. It is not listed in the `autosummary_context["exclude_modules"]` list in `conf.py`. (There is an example of this in `conf.py`!)

The members of a module (package) are then only documented if:
1. If a documented module has a `__all__` attribute that is a list of strings, its members will be documented if and only if their names appear in `__all__`. (See `src/my_project/__init__.py` for an example of this!)
1. If a documented module does not have `__all__`, all its members that satisfy all the following criteria will be documented:
    1. The member is public (ie, its name does not begin with an underscore)
    2. The member is defined in the module rather than imported
1. Any member of a documented class that satisfies all the following criteria will be documented:
    1. The member is public (ie, its name does not begin with an underscore)
    2. The member is defined in the class being documented (ie, it is not inherited)

The term member here refers to functions, classes, submodules, module attributes/constants, etc. of the module.

This means it is usually not necessary to define `__all__`, except in cases when you want an imported object to be accessible in the API at a different point to where it is defined, or you want to document a private object. It is considered best practice to use the `__all__` attribute to define all public members according to [PEP8](https://peps.python.org/pep-0008/#public-and-internal-interfaces). It is typical to find this attribute at the top of the file, PEP8 specifies that it should be after the module docstring but before any import statements except `from __future__`.

**However** using the `__all__` attribute means that your new public member won't appear in the documentation if you forget to add it to the `__all__` attirbute in the correct module! This is why in practice you might see many projects not using this feature as typically it is obvious what should and should not be in the public API. 

### How Sphinx's autodoc works
This is just an overview of how autodoc works, for more information see the [Sphinx documentation](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html). 
1. An autosummary directive must be written - see `docs/index.md` for an example.
1. When building the docs autosummary imports whatever items are listed in the directive. In the case of the example provided in this repository, you'll see `my_project` listed in the autosummary directive in `docs/index.md` but there is a `:recursive` option meaning that the subpackage will be imported as well.
1. For each item, a stub .rst page is generated based on the templates provided in `docs/_templates`. Thes pages may have autosummary directives within them that then recurse, generating more .rst page, you can find all of these in `docs/api/generated` once you have built the documentation locally.

### Documenting an inherited method without changing its behavior:
To document an inherited method without changing its behavior, define it in the child class without a docstring:

```python
class foo(bar):
    # Write the full signature to make sure it gets documented
    def method_on_bar(self):
        # Docstring will be inherited from bar.method_on_bar
        super().method_on_bar()
```

To explore more examples of automatic documentation, open  `docs/_build/html/index.rst` and look through the `my_project` tab. You can find the matching code in the `src` directory. 
