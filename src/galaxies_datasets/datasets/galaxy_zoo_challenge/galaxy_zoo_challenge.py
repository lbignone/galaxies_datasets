"""galaxy_zoo_challenge dataset."""
import csv
import dataclasses

import tensorflow as tf
import tensorflow_datasets as tfds

_URL = "https://www.kaggle.com/c/galaxy-zoo-the-galaxy-challenge"

_DESCRIPTION_TRAINING = f"""
This dataset contains the training data for the 2014 [Kaggle Galaxy Zoo
competion]({_URL}). This includes images and labels.
"""

_DESCRIPTION_TEST = f"""
This dataset contains the test data used to evaluate the 2014 [Kaggle Galaxy
Zoo competion]({_URL}). This includes only images.
"""

_CITATION = r"""
@ARTICLE{2015MNRAS.450.1441D,
       author = {{Dieleman}, Sander and {Willett}, Kyle W. and {Dambre}, Joni},
        title = "{Rotation-invariant convolutional neural networks for galaxy
         morphology prediction}",
      journal = {\mnras},
     keywords = {methods: data analysis, techniques: image processing,
     catalogues, galaxies: general, Astrophysics - Instrumentation and
     Methods for Astrophysics, Astrophysics - Astrophysics of Galaxies,
     Computer Science - Computer Vision and Pattern Recognition,
     Computer Science - Machine Learning,
     Computer Science - Neural and Evolutionary Computing,
     Statistics - Machine Learning},
         year = 2015,
        month = jun,
       volume = {450},
       number = {2},
        pages = {1441-1459},
          doi = {10.1093/mnras/stv632},
archivePrefix = {arXiv},
       eprint = {1503.07077},
 primaryClass = {astro-ph.IM},
       adsurl = {https://ui.adsabs.harvard.edu/abs/2015MNRAS.450.1441D},
      adsnote = {Provided by the SAO/NASA Astrophysics Data System}
}
"""

_CLASSES = [
    "Class1.1",
    "Class1.2",
    "Class1.3",
    "Class2.1",
    "Class2.2",
    "Class3.1",
    "Class3.2",
    "Class4.1",
    "Class4.2",
    "Class5.1",
    "Class5.2",
    "Class5.3",
    "Class5.4",
    "Class6.1",
    "Class6.2",
    "Class7.1",
    "Class7.2",
    "Class7.3",
    "Class8.1",
    "Class8.2",
    "Class8.3",
    "Class8.4",
    "Class8.5",
    "Class8.6",
    "Class8.7",
    "Class9.1",
    "Class9.2",
    "Class9.3",
    "Class10.1",
    "Class10.2",
    "Class10.3",
    "Class11.1",
    "Class11.2",
    "Class11.3",
    "Class11.4",
    "Class11.5",
    "Class11.6",
]


@dataclasses.dataclass
class GalaxyZooChallengeConfig(tfds.core.BuilderConfig):
    """Training dataset config."""

    train: bool = True


class GalaxyZooChallenge(tfds.core.GeneratorBasedBuilder):
    """DatasetBuilder for galaxy_zoo_challenge dataset."""

    VERSION = tfds.core.Version("1.0.0")
    RELEASE_NOTES = {
        "1.0.0": "Initial release.",
    }

    MANUAL_DOWNLOAD_INSTRUCTIONS = f"""
    Download the following files from the [Kaggle competition site]({_URL}):

    - images_training_rev1.zip
    - images_test_rev1.zip
    - training_solutions_rev1.zip

    Extract them in `manual_dir/galaxy_zoo_challenge`
    """

    BUILDER_CONFIGS = [
        # `name` (and optionally `description`) are required for each config
        GalaxyZooChallengeConfig(name="train"),
        GalaxyZooChallengeConfig(name="test", train=False),
    ]

    def _info(self) -> tfds.core.DatasetInfo:
        """Returns the dataset metadata."""
        features = {
            "image": tfds.features.Image(shape=(424, 424, 3)),
            "GalaxyID": tf.int64,
        }
        supervised_keys = None
        if self.builder_config.train:
            features["label"] = {class_name: tf.float64 for class_name in _CLASSES}
            supervised_keys = ("image", "label")

        return tfds.core.DatasetInfo(
            builder=self,
            description=_DESCRIPTION_TRAINING,
            features=tfds.features.FeaturesDict(features),
            supervised_keys=supervised_keys,  # Set to `None` to disable
            homepage=_URL,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager: tfds.download.DownloadManager):
        """Returns SplitGenerators."""
        data_path = dl_manager.manual_dir / "galaxy_zoo_challenge"
        if self.builder_config.train:
            img_path = data_path / "images_training_rev1"
            csv_path = data_path / "training_solutions_rev1.csv"
            return {
                "train": self._generate_examples(img_path, csv_path),
            }
        else:
            img_path = data_path / "images_test_rev1"
            return {
                "train": self._generate_examples_test(img_path),
            }

    def _generate_examples(self, img_path, csv_path):
        """Yields examples."""
        if self.builder_config.train:
            with csv_path.open() as f:
                for row in csv.DictReader(f):
                    galaxy_id = row["GalaxyID"]
                    yield galaxy_id, {
                        "GalaxyID": galaxy_id,
                        "image": img_path / f"{galaxy_id}.jpg",
                        "label": {
                            class_name: row[class_name] for class_name in _CLASSES
                        },
                    }

    def _generate_examples_test(self, img_path):
        """Yields examples."""
        for path in img_path.glob("*.jpg"):
            galaxy_id = path.name.split(".")[0]
            yield galaxy_id, {
                "image": path,
                "GalaxyID": galaxy_id,
            }
