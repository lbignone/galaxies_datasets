"""galaxy_zoo_challenge dataset."""
import tensorflow_datasets as tfds

from . import galaxy_zoo_challenge


class GalaxyZooChallengeTest(tfds.testing.DatasetBuilderTestCase):
    """Tests for galaxy_zoo_challenge dataset."""

    DATASET_CLASS = galaxy_zoo_challenge.GalaxyZooChallenge
    SPLITS = {
        "train": 3,  # Number of fake train example
    }


if __name__ == "__main__":
    tfds.testing.test_main()
