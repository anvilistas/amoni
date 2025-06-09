Contributing
============
All contributions to this project are welcome via pull request (PR) on the `Github repository <https://github.com/anvilistas/amoni>`_

Issues
------
Please open an `Issue <https://github.com/anvilistas/amoni/issues>`_ and describe the contribution you'd like to make before submitting any code. This prevents duplication of effort and makes reviewing the eventual PR much easier for the maintainers.

Commits
-------
Please try to use commit messages that give a meaningful history for anyone using git's log features. Try to use messages that complete the sentence, "This commit will..." There is some excellent guidance on the subject from `Chris Beams <https://chris.beams.io/posts/git-commit/>`_

Python Code
-----------
Please try, as far as possible, to follow `PEP8 <https://www.python.org/dev/peps/pep-0008/>`_.

Use the `Black formatter <https://github.com/ambv/black>`_ to format all code and the `isort utility <https://github.com/timothycrosley/isort>`_ to sort import statements.

Add the licence text and copyright statement to the top of your code.

Ensure that there is a line with the current version number towards the top of your code.

This can be automated by using `pre-commit <https://pre-commit.com/>`_.
To use ``pre-commit``, first install ``pre-commit`` with pip and then run ``pre-commit install`` inside your local ``anvil-extras`` repository.
All commits thereafter will be adjusted according to the above ``amoni`` python requirements.


Documentation
-------------
Please include documentation for your contribution as part of your PR. Our documents are written in `reStructuredText <https://en.wikipedia.org/wiki/ReStructuredText>`_ and hosted at `Read The Docs <https://amoni.readthedocs.io/en/latest/>`_

Our docs are built using `Sphinx <https://www.sphinx-doc.org/en/master/index.html>`_ which you can install locally and use to view your work before submission. To build a local copy of the docs in a '_build' directory:

   .. code-block::

       make clean
       make html

You can then open 'index.html' from within the build directory using your favourite browser.

Merging
-------
We require both maintainers to have reviewed and accepted a PR before it is merged.

If you would like feedback on your contribution before it's ready to merge, please create a draft PR and request a review.

Copyright
---------
By submitting a PR, you agree that your work may be distributed under the terms of the project's `licence <https://github.com/anvilistas/anvil-extras/blob/master/LICENSE>`_.
