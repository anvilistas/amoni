.. _configure-ssh:

Configure SSH
-------------
This guide assumes that you have already created an ssh key pair and added your public
key to Anvil.

If that's not the case, you can find useful information on how to do those steps at,
for example:

* `Creating an SSH key pair <https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent>`_
* `Adding your key to Anvil <https://anvil.works/docs/version-control/git>`_

In order for Amoni to know how to use your ssh keys to connect to a remote server (e.g.
anvil.works), add the following to your SSH config file (possibly `~/.ssh/config`):

.. code-block::

   Host anvil.works
       IdentityFile <path to your ssh key>

Depending on the version of openssh you are using, you may also need the following:

.. code-block::

   Host anvil.works
       IdentityFile <path to your ssh key>
       HostkeyAlgorithms +ssh-rsa
       PubkeyAcceptedAlgorithms +ssh-rsa

See `this forum post <https://anvil.works/forum/t/ssh-key-not-working/10227>`_ for more information.
