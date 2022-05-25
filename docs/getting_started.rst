Getting Started
===============

Create a New Amoni Project
--------------------------
In your terminal, navigate to a directory where you would like to create a new amoni
project and run:

.. code-block:: shell

   amoni init

This will prompt you for two pieces of information:

* Project

  A new directory will be created using the name you provide here.
* App Folder Name

  This should be the name of the folder containing the anvil app you wish to run locally.
  There is a minimal demo app included with amoni called 'hello_world' and this is the
  default that will be used if you simply hit enter at this prompt.

Amoni will now create a new directory using the name you provided and set up the necessary
files and directories within it.

Start Your Servers
------------------
Change into your new directory and run:

.. code-block::

   amoni start

The first time you run this command, it will take several minutes to complete. It:

* Downloads a docker image containing a postgresql database server if no local image exists (or is out of date)
* Downloads a docker image containing a fully configured anvil app server if no local image exists (or is out of date)
* Creates new docker containers from those two images
* Starts the two containers

Any subsequent times you run the command, the downloads will be unnecessary and the containers will start immediately.

You should see output similar to:

.. code-block:: shell

   Checking for newer images
   Starting anvil app and database servers
   Your app is now available at http://localhost:3030

In your browser, navigate to that url and you should see your app running.

If there were any errors, you can open the anvil error log which you will find in the 'logs' directory of your project.

Run Your Tests
--------------
You can now run the test suite for your app using:

.. code-block::

   amoni test

The test files are in the 'tests' directory of your project and are run using `pytest <https://docs.pytest.org/en/7.1.x/>`_.

Stop Your Servers
-----------------
When you are finished, you can stop your anvil and database servers using:

.. code-block:: shell

   amoni stop
