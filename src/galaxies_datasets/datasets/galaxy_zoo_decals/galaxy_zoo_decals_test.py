"""galaxy_zoo_decals dataset."""
import tensorflow_datasets as tfds

from . import galaxy_zoo_decals


class GalaxyZooDecalsTest(tfds.testing.DatasetBuilderTestCase):
    """Tests for galaxy_zoo_decals dataset."""

    DATASET_CLASS = galaxy_zoo_decals.GalaxyZooDecals
    SPLITS = {
        "train": 6,  # Number of fake train example
    }


if __name__ == "__main__":
    tfds.testing.test_main()
