<!--
Overview page for documentation

The text for this page is included from the README. This file is also
where we tell Sphinx about other pages in this documentation site.
-->
:::{include} ../README.md
:::

:::{toctree}
---
hidden: true
---

Overview <self>
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
