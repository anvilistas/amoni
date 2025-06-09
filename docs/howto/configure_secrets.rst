Configure Secrets and Encryption Keys
=====================================

This guide explains how to configure and manage app secrets and sensitive values
in your project.

Understanding Secrets and Encryption Keys
-----------------------------------------
Your Anvil app may use two types of sensitive values:

1. **Secrets**: Regular sensitive values like API keys or passwords
2. **Encryption Keys**: Special keys used for encrypting/decrypting data

These values are defined in your app's ``anvil.yaml`` file and stored in your project's
``config.yaml`` file.

Automatic Configuration
-----------------------
When you run ``amoni init`` with the ``--interactive`` flag or set up a new app, amoni
automatically:

1. Reads your app's ``anvil.yaml`` to identify required secrets and encryption keys
2. For regular secrets:

   * Sets placeholder values that you can update later
   * Preserves existing values if already configured

3. For encryption keys:

   * Generates secure, random encryption keys
   * Uses base64 encoding for proper storage
   * Preserves existing keys if already configured

Manual Configuration
--------------------
You can manually configure secrets and encryption keys using the ``amoni config`` command:

For regular secrets:

.. code-block:: shell

   amoni config api-key "your-api-key-here" --parent secret
   amoni config webhook-secret "your-webhook-secret" --parent secret

For encryption keys:

.. code-block:: shell

   amoni config user-data-key "your-base64-encoded-key" --parent encryption-key

.. note::
   For encryption keys, ensure your values are properly base64 encoded. Amoni's
   automatic key generation handles this for you, but for manual configuration,
   you need to provide correctly formatted keys.

Best Practices
--------------

   * Never commit real secrets or encryption keys to version control
   * Let amoni generate encryption keys when possible
   * Use the interactive setup for initial configuration
   * Document required secrets in your project README
