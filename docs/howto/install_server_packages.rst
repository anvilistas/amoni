Install Server Packages
-----------------------

The default configuration for the anvil app server contains only the server itself.

If you need additional Python packages available on your server, you can add them to the 'requirements.txt' file within your app's 'server_code' folder.

Each time you run 'amoni start', amoni will:

1. Copy the requirements.txt file from your app's server_code folder to the app folder
2. Install any packages listed in the requirements.txt file

This ensures that your server always has access to the latest package requirements defined in your app.
