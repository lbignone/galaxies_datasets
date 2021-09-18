Usage
=====


Galaxies_datasets is a collection of ready-to-use extragalactic astronomy datasets
for use with TensorFlow, Jax, and other Machine Learning frameworks.

It follows the `tensorflow_datasets`_ framework, making it very easy to switch
between different datasets. All datasets are exposed as `tf.data.Datasets`_, enabling
easy-to-use and high-performance input pipelines.

Loading a dataset can be as easy as::

    from galaxies_datasets import datasets
    import tensorflow_datasets as tfds

    # Construct a tf.data.Dataset
    ds = tfds.load("galaxy_zoo_challenge", split="train")

In the example above ::

    from galaxies_datasets import datasets

registers the collection of galactic datasets with the `tensorflow_datasets`_ package
making them available through its API. And that is it! ...Almost.

For more details on tensorflow_datasets check out the `documentation`_.

Some datasets require that you first manually download data. Check :ref:`each
dataset<Dataset catalog>` for instructions.


Dataset catalog
---------------


Currently available datasets focus on galaxy morphology.

They include observational data from the `galazy zoo project`_:

- galaxy_zoo_challenge
- galaxy_zoo_2
- galaxy_zoo_decals

As well as mock galaxy images from the `EAGLE simulation`_:

- eagle


Scripts
-------


Galaxies_datasets provides some scripts to download and prepare data. The scripts
are available through a command-line interface powered by `Typer`_.

For example, to download images and data from the EAGLE simulation you can simply do::

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


.. _tensorflow_datasets: https://www.tensorflow.org/datasets/
.. _tf.data.Datasets: https://www.tensorflow.org/api_docs/python/tf/data/Dataset
.. _documentation: https://www.tensorflow.org/datasets/overview
.. _galazy zoo project: https://www.zooniverse.org/projects/zookeeper/galaxy-zoo/
.. _EAGLE simulation: http://icc.dur.ac.uk/Eagle/
.. _Typer: https://typer.tiangolo.com/
.. _Command-line Interface: cli.html
