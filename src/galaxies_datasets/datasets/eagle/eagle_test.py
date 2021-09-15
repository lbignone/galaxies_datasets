"""eagle dataset."""
import tensorflow_datasets as tfds

from . import eagle


class EagleTest(tfds.testing.DatasetBuilderTestCase):
    """Tests for eagle dataset."""

    DATASET_CLASS = eagle.Eagle
    SPLITS = {
        "train": 3,  # Number of fake train example
    }


if __name__ == "__main__":
    tfds.testing.test_main()
