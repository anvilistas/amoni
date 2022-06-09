Use Autocompletion
------------------
Autocompleters generally use the libraries installed in your current python environment
to provide autocompletion as you type. You should install the `anvil-uplink` package to
add Anvil's classes and functions:

.. code-block::

   pip install anvil-uplink

In addition, many autocompleters can use `Python stub files <https://mypy.readthedocs.io/en/stable/stubs.html>`_
to understand the options available to you as you type code.

Amoni makes use of this facility to provide autocompletion for the anvil app_tables
module where the tables are defined within an app's `anvil.yaml` file. To enable this
feature, install the `anvil-stubs` package into your environment:

.. code-block::

   pip install anvil-stubs

Note - This package is provided by the anvilistas team and is not an official Anvil tool.

Amoni will then maintain additional stub files in your project's `anvil-stubs` directory.
Those are regenerated whenever you add an app or dependency to your project but you can
refresh those at any time manually by running:

.. code-block::

   amoni stubs <name of your app>
