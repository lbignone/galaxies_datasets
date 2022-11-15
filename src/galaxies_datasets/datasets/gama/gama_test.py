"""galaxy_zoo_3d dataset."""
import tensorflow_datasets as tfds

from . import gama


class GamaTest(tfds.testing.DatasetBuilderTestCase):
    """Tests for galaxy_zoo_3d dataset."""

    DATASET_CLASS = gama.Gama
    SPLITS = {
        "train": 3,  # Number of fake train example
    }

    # If you are calling `download/download_and_extract` with a dict, like:
    #   dl_manager.download({'some_key': 'http://a.org/out.txt', ...})
    # then the tests needs to provide the fake output paths relative to the
    # fake data directory
    # DL_EXTRACT_RESULT = {'some_key': 'output_file1.txt', ...}


if __name__ == "__main__":
    tfds.testing.test_main()
