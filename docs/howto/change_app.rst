Change the Main App
-------------------

The 'app' directory in your project must contain a folder for the anvil app you want to
run locally. Amoni includes a 'hello_world' app which is the default app to be served.

To change that to some other app, first clone your app to your local machine and place
the resulting directory within the 'app' directory of your amoni project.

Within the 'app' directory, you should also see a file named 'config.yaml'. This file
contains all the setting used to start the anvil server. Open this file with your
favourite text editor and change the entry on the first line from '/app/hello_world' to
the app folder you would like to run.

Save the file and exit your editor.

You can also delete the 'hello_world' directory if you wish.

The next time you run 'amoni start', you should see your new app available in your browser.
