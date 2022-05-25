Add Dependencies
----------------

The 'app' directory in your project must contain a folder for the app you wish to run plus a folder for each of its dependencies.

To add a dependency, first clone the relevant app to your local machine and place the resulting directory within the 'app' folder of your amoni project.

Within the the 'app' directory, you should also see a file named 'config.yaml'. This file contains the settings used to start the anvil server. Open this file with your favourite text editor.

At the bottom of the file, ensure there is a 'dep_id' section with an entry for each of the dependencies you need. Each entry needs to map the id of the dependency to the folder where it can be found.

e.g. if your app were called 'my_app' and depended upon two other apps named 'my_dependency_1' with id 'ABCDEF' and 'my_dependency_2' with id 'UVWXYZ', your file would look something like:

.. code-block:: yaml

   app: /app/hello_world
   data-dir: /anvil_data
   database: jdbc:postgresql://db/anvil?username=anvil&password=anvil
   uplink-key: uplink-key
   client-uplink-key: client-uplink-key
   auto-migrate: true
   dep_id:
       ABCDEF: my_dependency_1
       UVWXYZ: my_dependency_2
