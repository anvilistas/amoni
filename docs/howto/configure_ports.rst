Configure Ports and Origin URL
=============================

Amoni uses a two-port system:

Internal Ports (Docker):

* Port 3030 for the Anvil app server (fixed in config.yaml)
* Port 5432 for PostgreSQL (standard PostgreSQL port)

External Ports (Host Machine):

* Default port 3030 for accessing the Anvil app (configurable)
* Default port 5432 for accessing PostgreSQL (configurable)

You can customize these ports using environment variables in a ``.env`` file. If no ``.env`` file is found, amoni will fall back to these default values:

.. code-block:: bash

    AMONI_APP_PORT=3030  # Port for accessing the Anvil app
    AMONI_DB_PORT=5432   # Port for accessing the PostgreSQL database
    ORIGIN_URL=http://localhost:3030  # Default localhost URL

A warning message will be displayed when using default values. To set custom values:

.. code-block:: bash

    # .env file
    AMONI_APP_PORT=8080   # Custom port for the Anvil app
    AMONI_DB_PORT=5433    # Custom port for the database

Creating a .env File
-------------------

1. Copy the environment template file:

   .. code-block:: bash

       cp env.template .env

   Note: The ``env.template`` file is provided by default when you create a new project with ``amoni init``.

2. Edit the ``.env`` file to set your desired ports:

   .. code-block:: bash

       # Custom port configuration
       AMONI_APP_PORT=8080
       AMONI_DB_PORT=5433

   Note: If you don't set these variables, the default ports will be used.

Port and Origin Configuration Details
----------------------------------

AMONI_APP_PORT
^^^^^^^^^^^^^^
* Controls the external port where your Anvil app will be accessible on your host machine
* Maps to the internal port 3030 (fixed in config.yaml)
* Default external port: 3030
* Example: Setting AMONI_APP_PORT=8080 makes the app available at ``http://localhost:8080``

AMONI_DB_PORT
^^^^^^^^^^^^^
* Controls the external port where PostgreSQL will be accessible on your host machine
* Maps to the internal port 5432 (standard PostgreSQL port)
* Default external port: 5432
* Useful when you need to:

  * Connect to the database using external tools
  * Run multiple Amoni projects simultaneously
  * Avoid conflicts with existing PostgreSQL installations

Origin URL Configuration
^^^^^^^^^^^^^^^^^^^^^
* Controls the public URL where your app will be accessible
* Default: ``http://localhost:${AMONI_APP_PORT}``
* Examples:

  * Local development: ``http://localhost:8080`` (when AMONI_APP_PORT=8080)
  * Public domain: ``https://myapp.example.com``

* Use cases:

  * Running behind a reverse proxy
  * Deploying with a custom domain
  * Testing with different ports

Using with Cloudflare Tunnels
^^^^^^^^^^^^^^^^^^^^^^^^^^
When using Cloudflare Tunnels to expose your app to the internet:

1. Set ``disable-tls: true`` in your ``config.yaml``:

   .. code-block:: yaml

       disable-tls: true  # Required for Cloudflare Tunnel

2. Set your ORIGIN_URL to your Cloudflare domain:

   .. code-block:: bash

       ORIGIN_URL=https://myapp.example.com

This configuration works because:

* Cloudflare Tunnel handles the TLS termination
* Traffic between Cloudflare and your app is already secure
* The app server doesn't need to handle HTTPS directly

Best Practices
-------------

1. Never commit your ``.env`` file to version control
2. Always use ``env.template`` as a template
3. Document any custom port requirements in your project's README
4. Consider port availability when choosing custom ports
5. Use HTTPS for production origin URLs
6. Enable ``disable-tls`` when using Cloudflare Tunnels
