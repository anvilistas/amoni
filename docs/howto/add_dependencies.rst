Add Dependencies
----------------

The `app` directory in your project must contain a folder for the app you wish to run
plus a folder for each of its dependencies. The dependencies must also be defined in
`app/config.yaml` in order for the app server to find them correctly.

To add a dependency to your project:

.. code-block::

   amoni app add --as-dependency <URL to the app> <Name of the dependency> <ID of the dependency>

If the URL you provide is at `anvil.works` (perhaps from within the Anvil IDE), you
will need to :ref:`configure-ssh` in order for it to work. Amoni does not support
username/password authentication.

Amoni will clone the repository from the URL you provide and add it as a git submodule
to your amoni project. The submodule will be placed in the app folder.

Amoni will also change the settings in `app/config.yaml` so that the app server will
know where to find the dependency you've just added.

Finally, amoni will commit the changes you've just made to your project.
