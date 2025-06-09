Getting Started
===============

Create a New Amoni Project
--------------------------
In your terminal, navigate to a directory where you would like to create a new amoni
project and run:

.. code-block:: shell

   amoni init demo [--interactive]

Amoni will now create a new directory named demo and set up the necessary
files and directories within it.

Interactive Setup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If you use the ``--interactive`` (or ``-i``) flag, amoni will guide you through the setup process:

1. Configure your main app:

   * Enter the repository URL for your main app
   * Specify a name for the app

2. Configure dependencies:

   * For each dependency in your main app's anvil.yaml
   * Enter the repository URL for the dependency
   * The version will be automatically set based on your main app's configuration

3. Configure server settings:

   * Set the app server port (default: 3030)
   * Set the database port (default: 5432)
   * Set the origin URL (default: http://localhost:<app_port>)

4. Configure app secrets and encryption keys:

   * Automatically detects secrets from your app's anvil.yaml
   * For existing secrets, option to update or keep current values
   * For encryption keys, automatically generates secure keys or allows custom values
   * All secrets and keys are stored in config.yaml

5. Configure SMTP settings (optional):

   * SMTP host (e.g., smtp.gmail.com)
   * SMTP username and password
   * SMTP port (default: 587)
   * SMTP encryption method (default: starttls)

All these settings will be saved in your project's configuration files. The environment
variables are stored in a ``.env`` file, while app configuration is stored in
``app/config.yaml``.

Start Your Servers
------------------
Change into your new directory and run:

.. code-block::

   amoni start

The first time you run this command, it will take several minutes to complete as it
downloads the images for the servers. During startup, amoni will:

* Copy any requirements.txt from your app's server_code folder to the app folder
* Configure environment variables from your .env file
* Start the database and app servers

Any subsequent times you run the command, the downloads will be unnecessary and the containers will start immediately.

You should see output ending with:

.. code-block:: shell

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

Configuration Management
------------------------
After initial setup, you can manage your configuration using these commands:

Set environment variables:

.. code-block:: shell

   amoni env AMONI_APP_PORT 8080
   amoni env AMONI_DB_PORT 5433

Update configuration values:

.. code-block:: shell

   # Set a regular config value
   amoni config disable-tls true

   # Set a secret value
   amoni config my-secret-key "secret123" --parent secret

   # Set an encryption key
   amoni config my-encryption-key "base64-encoded-key" --parent encryption-key

These commands will automatically update your .env file and config.yaml as appropriate.
