Change the Main App
-------------------

The `app` directory in your project must contain a folder for the anvil app you want to
run locally and `app/config.yaml` must point to that folder so that the app server
starts the correct app.

Amoni includes a 'hello_world' app which is the default app when you first
create a project.

To change the default to your own anvil app:

.. code-block::

   amoni app add <URL to your app> <Name of your app>

If the URL you provide is at `anvil.works` (perhaps from within the Anvil IDE), you
will need to :ref:`configure-ssh` in order for it to work.

Amoni will clone the repository from the URL you provide and add it as a git submodule
to your amoni project. The submodule will be placed in the app folder.

Amoni will also change the settings in `app/config.yaml` so that the app server will
now start the app you just installed and it will parse the app's `anvil.yaml` file
and add stub entries to `anvil-stubs/tables/app_tables.pyi` (so that your autcompleter
will know what tables exist in your app).

Finally, amoni will commit the changes you've just made to your project.

You can now delete the 'hello_world' directory if you wish.

The next time you run 'amoni start', you should see your new app available in your browser.
