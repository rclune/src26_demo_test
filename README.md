# OMSF Documentation Template
A documentation system that developers can easily transfer to their own projects. 

## What's included?
In the root of the repository you will find: 
- `docs` directory: This is where you will be adding any documentation that isn't automatically generated and changing how your external documentation is structured. It also includes a folder of templates for different types of documentation to help you get started. This directory has its own [README](./docs/README.md#compiling-the-omsf-demonstration-documentation) with information about building the docs, automatically creating API documentation, and hosting your documentation. 
- `src/my_project` directory: This contains some examples to show off the API documentation capabilities of Sphinx. 
- `pyproject.toml`: Example TMOL configuration file for a python package, see [this resource](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#writing-pyproject-toml) for more information on Python Packaging. 
- `readthedocs.yaml`: This is a configuration file for Read the Docs, this is one option for hosting your documentation. There is more information about how to do this in the README in the `docs` folder. 

## Intended usage
```{eval-rst}
.. note:: There are some files included in this repository as examples and they do not need to be copied or kept in your project repository for the documentation to build. These files include: 

    - Anything in the ``src/my_project`` directory (though the docs do assume an ``src/project_name`` structure.)
    - ``docs/desert-flower.jpg``
    - ``docs/myst-md-demo.md``
```
<details>
<summary><strong> Starting a Completely New Project </strong></summary>

Thank you for thinking about documentation from the beginning of your development process!! 

You can duplicate this repository and directly start developing in it via GitHub's mirroring capabilities. 
See GitHub's documentation on [Duplicating a repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/duplicating-a-repository) for the most efficient way to do this. 
</details>

<details>
    <summary><strong>Incorporating Documentation Into an Existing Project </strong></summary>
    You can directly copy the contents of this project into your project repository, though you should make sure the copy won't overwrite anything you'd like to keep. Make sure to update the `pyproject.toml`, `conf.py`, and `index.md` with information for your specific project.
    
</details>

Once you have your docs set up in your project repository you can start adding documentation for your project. 

For automatically generated API documentation, you will need to write docstrings for all members of your module, there are more instructions for how to do this in the README in the `docs` folder. 

For all other documentation you will need to create a new `.md` file directly in the `docs` directory, write up whatever you would like to document using Markdown (see the [next section](#markdown-and-restructuredtext)) and then add it to the TOC section of `docs/index.md`. There's a comment in `docs/index.md` to show you where to point to your new files. 

## Markdown and reStructuredText
Sphinx natively uses reStructuredText (RST or reST) as its markup language, however, Markdown is more ubiquitous and many find it easier to use and learn. Due to this, all of the documentation files included here are Markdown (.md) files and a package, [myst-parser](https://myst-parser.readthedocs.io/en/latest/intro.html) is used so that Sphinx can still generate the static documentation pages. 

For those of you new to Markdown, [markdownguide.org](https://www.markdownguide.org/) is a wonderful resource for learning this markup language. They also have a great [Cheat Sheet](https://www.markdownguide.org/cheat-sheet/) for quickly reviewing the basic syntax!

There may be some situations in which knowing some of the capabilities of RST is useful. Here are a few resources if you find yourself in those situations: 
- Sphinx's [reStructuredText Primer](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html)
- An [RST Cheat Sheet](https://sphinx-tutorial.readthedocs.io/cheatsheet/)

If you're willing to learn some HTML/CSS you can do even fancier stuff with your documentation, but that is outside the scope of this project. 

## Docstring formats
The automatically generated API documentation relies on docstrings to know what to write. There are examples of docstrings provided in the `src/my_project` directory. There are many different types of docstring formats ([Sphinx](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html), [Google](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html), [Numpy](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_numpy.html#example-numpy), etc.), but the examples included in this repo use the Sphinx format as using other formats requires [Sphinx's napoleon extension](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html). 

The choice of docstring format is entirely up to you, what's most important is maintaining consistency across functions, classes and files!