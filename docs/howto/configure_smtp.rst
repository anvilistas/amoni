Configure SMTP Settings
=======================

This guide explains how to configure SMTP settings for your Anvil app's email functionality.

Interactive Setup
-----------------
The easiest way to configure SMTP is during project initialization:

.. code-block:: shell

   amoni init myproject --interactive

During the interactive setup, you'll be prompted for:

* SMTP host (e.g., smtp.gmail.com)
* SMTP username
* SMTP password
* SMTP port (default: 587)
* SMTP encryption method (default: starttls)

Manual Configuration
--------------------
You can manually configure SMTP settings using the ``amoni config`` command:

.. code-block:: shell

   amoni config smtp-host "smtp.gmail.com"
   amoni config smtp-username "your-email@gmail.com"
   amoni config smtp-password "your-app-specific-password"
   amoni config smtp-port "587"
   amoni config smtp-encryption "starttls"
