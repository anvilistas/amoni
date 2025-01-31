Add Dependencies
----------------

The `app` directory in your project must contain a folder for the app you wish to run
plus a folder for each of its dependencies. The dependencies must also be defined in
`app/config.yaml` in order for the app server to find them correctly.

To add a dependency to your project:

.. code-block::

   amoni app add --as-dependency <URL to the app> <Name of the dependency> <ID of the dependency> [--set-version]

The optional ``--set-version`` flag will automatically set the dependency's version based on the version information in your main app's anvil.yaml file. If not specified, the dependency will use its default branch.

If the URL you provide is at `anvil.works` (perhaps from within the Anvil IDE), you
will need to :ref:`configure-ssh` in order for it to work. Amoni does not support
username/password authentication.

Amoni will clone the repository from the URL you provide and add it as a git submodule
to your amoni project. The submodule will be placed in the app folder.

Amoni will also change the settings in `app/config.yaml` so that the app server will
know where to find the dependency you've just added.

Finally, amoni will:

1. Commit the changes you've just made to your project
2. If ``--set-version`` was used, fetch and checkout the version specified in your main app's anvil.yaml
3. Ensure the dependency is properly configured in your project
