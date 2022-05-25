Install Server Packages
-----------------------

The default configuration for the anvil app server contains only the server itself.

If you need additional Python packages available on your server you can add them to the 'requirements.txt' file within the 'app' directory of your amoni project.

The next time you run 'amoni start', any packages listed in 'requirements.txt' will be installed and available.
