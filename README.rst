Galaxies Datasets
=================

|header|

.. |header| image:: header.png
   :alt: Galaxies Datasets

|PyPI| |Status| |Python Version| |License|

|Read the Docs| |Tests| |Codecov|

|pre-commit| |Black|

.. |PyPI| image:: https://img.shields.io/pypi/v/galaxies_datasets.svg
   :target: https://pypi.org/project/galaxies_datasets/
   :alt: PyPI
.. |Status| image:: https://img.shields.io/pypi/status/galaxies_datasets.svg
   :target: https://pypi.org/project/galaxies_datasets/
   :alt: Status
.. |Python Version| image:: https://img.shields.io/pypi/pyversions/galaxies_datasets
   :target: https://pypi.org/project/galaxies_datasets
   :alt: Python Version
.. |License| image:: https://img.shields.io/pypi/l/galaxies_datasets
   :target: https://opensource.org/licenses/MIT
   :alt: License
.. |Read the Docs| image:: https://img.shields.io/readthedocs/galaxies_datasets/latest.svg?label=Read%20the%20Docs
   :target: https://galaxies_datasets.readthedocs.io/
   :alt: Read the documentation at https://galaxies_datasets.readthedocs.io/
.. |Tests| image:: https://github.com/lbignone/galaxies_datasets/workflows/Tests/badge.svg
   :target: https://github.com/lbignone/galaxies_datasets/actions?workflow=Tests
   :alt: Tests
.. |Codecov| image:: https://codecov.io/gh/lbignone/galaxies_datasets/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/lbignone/galaxies_datasets
   :alt: Codecov
.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit
.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Black


*Galaxies Datasets* is a collection of ready-to-use extragalactic astronomy datasets
for use with TensorFlow, Jax, and other Machine Learning frameworks.

It follows the `tensorflow_datasets`_ framework, making it very easy to switch
between different datasets. All datasets are exposed as `tf.data.Datasets`_, enabling
easy-to-use and high-performance input pipelines.


Usage
-----

Loading a dataset can be as easy as:

.. code-block:: python

    from galaxies_datasets import datasets
    import tensorflow_datasets as tfds

    # Construct a tf.data.Dataset
    ds = tfds.load("galaxy_zoo_challenge", split="train")

    # Build your input pipeline
    ds = ds.shuffle(1000).batch(128).prefetch(10).take(5)

In the example above:

.. code-block:: python

    from galaxies_datasets import datasets

registers the collection of galactic datasets with the `tensorflow_datasets`_ package
making them available through its API. And that is it! ...Almost.

For more details on tensorflow_datasets check out the `documentation`_.

Some datasets require that you first manually download data. Check each dataset for
instructions.


Datasets
--------

Currently `available datasets`_ focus on galaxy morphology.

They include observational data from the `Galaxy zoo project`_:

- galaxy_zoo_challenge
- galaxy_zoo2
- galaxy_zoo_decals

As well as mock galaxy images from the `EAGLE simulation`_:

- eagle


Installation
------------

You can install *Galaxies Datasets* via pip_ from PyPI_:

.. code:: console

   $ pip install galaxies_datasets


Scripts
-------

*Galaxies Datasets* provides some scripts to download and prepare data. The scripts
are available through a command-line interface powered by `Typer`_.

For example, to download images and data from the EAGLE simulation you could simply do::

    galaxies_datasets eagle download USER SIMULATION

where USER is your username for the EAGLE public database and SIMULATION is the name
of one of the EAGLE simulations.

For all available commands check the `Command-line Interface`_ reference, or run::

    galaxies_datasets --help

The command-line interface also supports automatic completion in all operating
systems, in all the shells (Bash, Zsh, Fish, PowerShell), so that you can just hit
TAB and get the available options or subcommands.

To install automatic completion in bash run::

    galaxies_datasets --install-completion bash


Contributing
------------

Contributions are very welcome.
To learn more, see the `Contributor Guide`_.


License
-------

Distributed under the terms of the `MIT license`_,
*Galaxies Datasets* is free and open source software.


Issues
------

If you encounter any problems,
please `file an issue`_ along with a detailed description.


Disclaimer
----------

This is a utility library that downloads and prepares datasets. We do not host
or distribute these datasets, vouch for their quality or fairness, or claim that you
have license to use the dataset. It is your responsibility to determine whether you
have permission to use the dataset under the dataset's license.

If you're a dataset owner and wish to update any part of it (description, citation,
etc.), or do not want your dataset to be included in this library, please get in
touch through a GitHub issue. Thanks for your contribution to the ML community!


Credits
-------

This project was generated from `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_
template.

Icons made by `Freepik <https://www.freepik.com>`_ from `www.flaticon.com
<https://www.flaticon.com/>`_


.. _@cjolowicz: https://github.com/cjolowicz
.. _MIT license: https://opensource.org/licenses/MIT
.. _PyPI: https://pypi.org/
.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python
.. _file an issue: https://github.com/lbignone/galaxies_datasets/issues
.. _pip: https://pip.pypa.io/
.. _tensorflow_datasets: https://www.tensorflow.org/datasets/
.. _tf.data.Datasets: https://www.tensorflow.org/api_docs/python/tf/data/Dataset
.. _documentation: https://www.tensorflow.org/datasets/overview
.. _Galaxy zoo project: https://www.zooniverse.org/projects/zookeeper/galaxy-zoo/
.. _EAGLE simulation: http://icc.dur.ac.uk/Eagle/
.. _Typer: https://typer.tiangolo.com/
.. github-only
.. _available datasets: docs/datasets.md
.. _Contributor Guide: CONTRIBUTING.rst
.. _Command-line Interface: cli.rst
.. _Usage: https://galaxies_datasets.readthedocs.io/en/latest/usage.html
