"""galaxy_zoo_2 dataset."""
import tensorflow_datasets as tfds

from . import galaxy_zoo_2


class GalaxyZoo2Test(tfds.testing.DatasetBuilderTestCase):
    """Tests for galaxy_zoo_2 dataset."""

    DATASET_CLASS = galaxy_zoo_2.GalaxyZoo2
    SPLITS = {
        "train": 3,  # Number of fake train example
    }


if __name__ == "__main__":
    tfds.testing.test_main()
