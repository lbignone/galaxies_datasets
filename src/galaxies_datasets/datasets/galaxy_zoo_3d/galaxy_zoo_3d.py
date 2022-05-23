"""galaxy_zoo_3d dataset."""
import numpy as np
import tensorflow as tf
import tensorflow_datasets as tfds
from astropy.io import fits

# TODO(galaxy_zoo_3d): Markdown description  that will appear on the catalog page.
_DESCRIPTION = """
Description is **formatted** as markdown.

It should also contain any processing which has been applied (if any),
(e.g. corrupted example skipped, images cropped,...):
"""

# TODO(galaxy_zoo_3d): BibTeX citation
_CITATION = """
"""


class GalaxyZoo3d(tfds.core.GeneratorBasedBuilder):
    """DatasetBuilder for galaxy_zoo_3d dataset."""

    VERSION = tfds.core.Version("1.0.0")
    RELEASE_NOTES = {
        "1.0.0": "Initial release.",
    }

    MANUAL_DOWNLOAD_INSTRUCTIONS = """
      GalaxyZoo3d has a dedicated script to download data.

      Usage:

          galaxies_datasets galaxyzoo3d download
      """

    def _info(self) -> tfds.core.DatasetInfo:
        """Returns the dataset metadata."""
        return tfds.core.DatasetInfo(
            builder=self,
            description=_DESCRIPTION,
            features=tfds.features.FeaturesDict(
                {
                    # These are the features of your dataset like images, labels ...
                    "mangaid": tfds.features.Text(),
                    "image": tfds.features.Image(shape=(None, None, 3)),
                    "center_mask": tfds.features.Image(
                        shape=(None, None, 1), dtype=tf.float32
                    ),
                    "stars_mask": tfds.features.Image(
                        shape=(None, None, 1), dtype=tf.float32
                    ),
                    "spiral_mask": tfds.features.Image(
                        shape=(None, None, 1), dtype=tf.float32
                    ),
                    "bar_mask": tfds.features.Image(
                        shape=(None, None, 1), dtype=tf.float32
                    ),
                }
            ),
            # If there's a common (input, target) tuple from the
            # features, specify them here. They'll be used if
            # `as_supervised=True` in `builder.as_dataset`.
            # supervised_keys=('image', 'label'),  # Set to `None` to disable
            supervised_keys=None,
            homepage="""
        https://www.sdss.org/dr17/data_access/value-added-catalogs/?vac_id=galaxy-zoo-3d
        """,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager: tfds.download.DownloadManager):
        """Returns SplitGenerators."""
        path = dl_manager.manual_dir / "galaxyzoo3d"

        return {
            "train": self._generate_examples(path),
        }

    def _generate_examples(self, path):
        """Yields examples."""
        for f in path.glob("*.gz"):
            mangaid = f.name.split("_")[1]  # use as key
            hdul = fits.open(f)

            image = hdul[0].data

            center_mask = hdul[1].data.astype("float32")
            center_mask = np.expand_dims(center_mask, axis=-1)

            stars_mask = hdul[2].data.astype("float32")
            stars_mask = np.expand_dims(stars_mask, axis=-1)

            spiral_mask = hdul[3].data.astype("float32")
            spiral_mask = np.expand_dims(spiral_mask, axis=-1)

            bar_mask = hdul[4].data.astype("float32")
            bar_mask = np.expand_dims(bar_mask, axis=-1)

            hdul.close()

            yield mangaid, {
                "mangaid": mangaid,
                "image": image,
                "center_mask": center_mask,
                "stars_mask": stars_mask,
                "spiral_mask": spiral_mask,
                "bar_mask": bar_mask,
            }
