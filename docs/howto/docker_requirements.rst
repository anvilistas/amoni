Docker Requirements Management
==============================

This guide explains how amoni manages Python requirements for your Docker containers.

Automatic Requirements Copying
------------------------------
When you run ``amoni start``, the system automatically:

1. Checks for a ``requirements.txt`` file in your app's ``server_code`` directory
2. If found, copies it to the ``app`` directory
3. Uses this file to install dependencies in the Docker container

This ensures that your Docker environment has all the Python packages needed by your Anvil app's server code.
