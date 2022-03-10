Contributor Guide
=================

Thank you for your interest in improving this project.
This project is open-source under the `MIT license`_ and
welcomes contributions in the form of bug reports, feature requests, and pull requests.

Here is a list of important resources for contributors:

- `Source Code`_
- `Documentation`_
- `Issue Tracker`_
- `Code of Conduct`_

.. _MIT license: https://opensource.org/licenses/MIT
.. _Source Code: https://github.com/lbignone/galaxies_datasets
.. _Documentation: https://galaxies_datasets.readthedocs.io/
.. _Issue Tracker: https://github.com/lbignone/galaxies_datasets/issues

How to report a bug
-------------------

Report bugs on the `Issue Tracker`_.

When filing an issue, make sure to answer these questions:

- Which operating system and Python version are you using?
- Which version of this project are you using?
- What did you do?
- What did you expect to see?
- What did you see instead?

The best way to get your bug fixed is to provide a test case,
and/or steps to reproduce the issue.


How to request a feature
------------------------

Request features on the `Issue Tracker`_.


How to set up your development environment
------------------------------------------

You need Python 3.7.1+ and the following tools:

- Poetry_
- Nox_
- nox-poetry_

Install the package with development requirements:

.. code:: console

   $ poetry install

You can now run an interactive Python session,
or the command-line interface:

.. code:: console

   $ poetry run python
   $ poetry run galaxies_datasets

.. _Poetry: https://python-poetry.org/
.. _Nox: https://nox.thea.codes/
.. _nox-poetry: https://nox-poetry.readthedocs.io/

How to set up your development environment (detailed instructions)
------------------------------------------------------------------

`Fork and clone`_ this repository.

Install Poetry_ to manage dependencies and packaging.

Install Nox_ to manage automated testing and other operations.

Install nox-poetry_ to use Poetry_ inside Nox_ sessions.

Install pyenv_ to manage the multiple Python versions supported.

Once pyenv is installed you can install Python versions 3.7, 3.8 and 3.9

.. code:: console

   $ pyenv install 3.7.12
   $ pyenv install 3.8.12
   $ pyenv install 3.9.10

It is recommended that you create a :code:`.python-version` file in the root directory of
the project. This will help pyenv determine which Python version to use. The content
of the file should be:

.. code::

   3.9.10
   3.8.12
   3.7.12

Make sure that poetry is using the correct Python version

.. code:: console

   $ poetry env use 3.9

Install the package with development requirements:

.. code:: console

   $ poetry install

Activate the development virtual environment

.. code:: console

   $ poetry shell

.. _Fork and clone: https://docs.github.com/get-started/quickstart/fork-a-repo#forking-a-repository
.. _pyenv: https://github.com/pyenv/pyenv

How to test the project
-----------------------

Run the full test suite:

.. code:: console

   $ nox

List the available Nox sessions:

.. code:: console

   $ nox --list-sessions

You can also run a specific Nox session.
For example, invoke the unit test suite like this:

.. code:: console

   $ nox --session=tests

Unit tests are located in the ``tests`` directory,
and are written using the pytest_ testing framework.

.. _pytest: https://pytest.readthedocs.io/


How to submit changes
---------------------

Open a `pull request`_ to submit changes to this project.

Your pull request needs to meet the following guidelines for acceptance:

- The Nox test suite must pass without errors and warnings.
- Include unit tests. This project maintains 100% code coverage.
- If your changes add functionality, update the documentation accordingly.

Feel free to submit early, though—we can always iterate on this.

To run linting and code formatting checks before commiting your change, you can install pre-commit as a Git hook by running the following command:

.. code:: console

   $ nox --session=pre-commit -- install

It is recommended to open an issue before starting work on anything.
This will allow a chance to talk it over with the owners and validate your approach.

.. _pull request: https://github.com/lbignone/galaxies_datasets/pulls
.. github-only
.. _Code of Conduct: CODE_OF_CONDUCT.rst
