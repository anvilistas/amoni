Welcome to Amoni
================

Amoni is a command line tool to manage local development tasks for an `Anvil <https://anvil.works>`_ application.

Amoni gives you:

* A preconfigured postgresql server running in a docker container
* A preconfigured Anvil application server running in a docker container
* Simple commands to start and stop those servers
* A preconfigured docker container to run your test suite
* Convenient access to the anvil error log
* Your app available in your browser at port 3030 on your local machine
* Your database server available on port 5432 on your local machine
* Commands to fetch an app from a remote repository and add it to your project either as the main app or as a dependency
* Stub files so that your autocompleter can see the tables available in your app

So your workflow becomes:

.. code-block:: shell

   amoni init
   cd <my_new_amoni_project_directory>
   amoni start

   >>> Wait a while the first time while the server images download
   >>> Point my browser at http://localhost:3030
   >>> Marvel at how simple that was

   amoni test

   >>> Sigh with relief at those lovely passing tests

   amoni stop

   >>> Sup coffee (or beverage of choice)


.. toctree::
   :maxdepth: 2

   installation.rst
   getting_started.rst
   howto/index.rst
   reference/index.rst

Why the Name?
-------------
It's `Greek for anvil <https://translate.google.com/?sl=auto&tl=el&text=anvil&op=translate>`_ and the idea for this library was conceived on a sunny veranda on the island of Κέρκυρα (Corfu).

* :ref:`genindex`
* :ref:`search`
