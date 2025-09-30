<!--
Overview page for documentation

The text for this page is included from the README and the overview.md file.
If you have an overview, remove the inclusion of the README.md, below. If you do not
have a separate overview, remove the inclusion of overview.md and readme_link.md, below.

This file is also where we tell Sphinx about other pages in this documentation site.
-->
:::{include} overview.md
:::

:::{include} ../README.md
:::

:::{toctree}
---
hidden: true
---

Overview <self>
readme_link.md
myst-md-demo.md

:::
<!--
Add any new (not automatically generated) documentation files above the :::
in the order you would like to have them appear in the TOC.
-->

<!--
The autosummary directive renders to rST,
so we must use eval-rst here
-->
```{eval-rst}
.. raw:: html

    <div style="display: None">

.. autosummary::
   :recursive:
   :caption: API Reference
   :toctree: api/generated
   :nosignatures:

   my_project

.. raw:: html

    </div>
```
