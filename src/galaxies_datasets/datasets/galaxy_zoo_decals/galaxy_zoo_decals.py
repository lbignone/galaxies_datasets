"""galaxy_zoo_decals dataset."""
import ast
import csv
import dataclasses

import tensorflow as tf
import tensorflow_datasets as tfds

_DESCRIPTION = """
This repository contains the data released in the paper "Galaxy Zoo DECaLS:
Detailed Visual Morphology Measurements from Volunteers and Deep Learning
for 314000 Galaxies"
"""

_HOMEPAGE_URL = "https://doi.org/10.5281/zenodo.4196266"
_DOWNLOAD_URL = "https://zenodo.org/record/4573248/files"

_CITATION = """
@misc{walmsley2021galaxy,
      title={Galaxy Zoo DECaLS: Detailed Visual Morphology Measurements from
      Volunteers and Deep Learning for 314,000 Galaxies},
      author={Mike Walmsley and Chris Lintott and Tobias Geron and Sandor
      Kruk and Coleman Krawczyk and Kyle W. Willett and Steven Bamford and
      William Keel and Lee S. Kelvin and Lucy Fortson and Karen L. Masters
      and Vihang Mehta and Brooke D. Simmons and Rebecca Smethurst and
      Elisabeth M. Baeten and Christine Macmillan},
      year={2021},
      eprint={2102.08414},
      archivePrefix={arXiv},
      primaryClass={astro-ph.GA}
}

@dataset{walmsley_mike_2020_4573248,
  author       = {Walmsley, Mike and
                  Lintott, Chris and
                  Tobias, Geron and
                  Kruk, Sandor J and
                  Krawczyk, Coleman and
                  Willett, Kyle and
                  Bamford, Steven and
                  Kelvin, Lee S and
                  Fortson, Lucy and
                  Gal, Yarin and
                  Keel, William and
                  Masters, Karen and
                  Mehta, Vihang and
                  Simmons, Brooke and
                  Smethurst, Rebecca J and
                  Smith, Lewis and
                  Baeten, Elisabeth M L and
                  Macmillan, Christine},
  title        = {{Galaxy Zoo DECaLS: Detailed Visual Morphology
                   Measurements from Volunteers and Deep Learning for
                   314,000 Galaxies}},
  month        = dec,
  year         = 2020,
  publisher    = {Zenodo},
  version      = {0.0.2},
  doi          = {10.5281/zenodo.4573248},
  url          = {https://doi.org/10.5281/zenodo.4573248}
}
"""

_METADATA = {
    "iauname": tf.string,
    "ra": tf.float64,
    "dec": tf.float64,
    "redshift": tf.float64,
    "elpetro_absmag_r": tf.float64,
    "sersic_nmgy_r": tf.float64,
    "petro_th50": tf.float64,
    "petro_th90": tf.float64,
    "petro_theta": tf.float64,
    "wrong_size_statistic": tf.float64,
    "wrong_size_warning": tf.bool,
}

_QUESTIONS = {
    "smooth-or-featured": [
        "smooth",
        "featured-or-disk",
        "artifact",
    ],
    "how-rounded": [
        "completely",
        "in-between",
        "cigar-shaped",
    ],
    "disk-edge-on": [
        "yes",
        "no",
    ],
    "edge-on-bulge": [
        "rounded",
        "boxy",
        "none",
    ],
    "bar": [
        "yes",
        "no",
    ],
    "has-spiral-arms": [
        "yes",
        "no",
    ],
    "spiral-winding": [
        "tight",
        "medium",
        "loose",
    ],
    "spiral-arm-count": [
        "1",
        "2",
        "3",
        "4",
        "more-than-4",
    ],
    "bulge-size": [
        "none",
        "obvious",
        "dominant",
    ],
    "merging": [
        "merger",
        "tidal-debris",
        "both",
        "neither",
    ],
}

_QUESTIONS_5 = {
    "bar": [
        "strong",
        "weak",
        "no",
    ],
    "bulge-size": [
        "dominant",
        "large",
        "moderate",
        "small",
        "none",
    ],
    "how-rounded": [
        "round",
        "in-between",
        "cigar-shaped",
    ],
    "spiral-arm-count": [
        "1",
        "2",
        "3",
        "4",
        "more-than-4",
        "cant-tell",
    ],
    "merging": [
        "none",
        "minor-disturbance",
        "major-disturbance",
        "merger",
    ],
}

_QUESTIONS_5 = {**_QUESTIONS, **_QUESTIONS_5}  # merge dicts


def morphology_features(questions, auto=False):
    """Compose features dictionary."""
    d = {}
    for question in questions:
        if not auto:
            d[f"{question}_total-votes"] = tf.int64
        for answer in questions[question]:
            if not auto:
                d[f"{question}_{answer}"] = tf.int64
                d[f"{question}_{answer}_debiased"] = tf.float64
            else:
                d[f"{question}_{answer}_concentration"] = tfds.features.Sequence(
                    tf.float64, length=25
                )
            d[f"{question}_{answer}_fraction"] = tf.float64

    return d


def find_image_path(iauname, image_paths):
    """Find image path."""
    filename = f"{iauname}.png"
    header = filename[:4]
    for image_path in image_paths:
        path = image_path / header
        if tf.io.gfile.exists(path):
            path = path / filename
            if tf.io.gfile.exists(path):
                return path

    return None


@dataclasses.dataclass
class GalaxyZooDecalsConfig(tfds.core.BuilderConfig):
    """Config for decals DR 1 and 2."""

    data: str = "1_and_2"
    csv_name: str = "gz_decals_volunteers_1_and_2.csv"
    auto: bool = False


class GalaxyZooDecals(tfds.core.GeneratorBasedBuilder):
    """DatasetBuilder for galaxy_zoo_decals dataset."""

    VERSION = tfds.core.Version("1.0.0")
    RELEASE_NOTES = {
        "1.0.0": "Initial release.",
    }

    MANUAL_DOWNLOAD_INSTRUCTIONS = """
    Download from this [Zenodo
    repository](https://zenodo.org/record/4573248#.YSEdzPfQ_mg) the
    following three csv files and place them in `manual_dir/galaxy_zoo_decals`

    - gz_decals_volunteers_1_and_2.csv
    - gz_decals_volunteers_5.csv
    - gz_decals_auto_posteriors.csv

    Also download all four gz_decals_dr5_png_part*.zip files and extract
    them in `manual_dir/galaxy_zoo_decals`. You should end up with with
    four folders structured like this:

        gz_decals_dr5_png_part*.zip/J*/J*.png
    """

    BUILDER_CONFIGS = [
        # `name` (and optionally `description`) are required for each config
        GalaxyZooDecalsConfig(name="volunteers_1_and_2"),
        GalaxyZooDecalsConfig(
            name="volunteers_5", data="5", csv_name="gz_decals_volunteers_5.csv"
        ),
        GalaxyZooDecalsConfig(
            name="auto",
            data="5",
            csv_name="gz_decals_auto_posteriors.csv",
            auto=True,
        ),
    ]

    @property
    def morphology_features(self):
        """Return features dictionary."""
        if self.builder_config.data == "5":
            questions = _QUESTIONS_5
        else:
            questions = _QUESTIONS

        return morphology_features(questions=questions, auto=self.builder_config.auto)

    def _info(self) -> tfds.core.DatasetInfo:
        """Returns the dataset metadata."""
        return tfds.core.DatasetInfo(
            builder=self,
            description=_DESCRIPTION,
            features=tfds.features.FeaturesDict(
                {
                    "image": tfds.features.Image(shape=(424, 424, 3)),
                    "morphology": self.morphology_features,
                    "metadata": _METADATA,
                }
            ),
            # If there's a common (input, target) tuple from the
            # features, specify them here. They'll be used if
            # `as_supervised=True` in `builder.as_dataset`.
            supervised_keys=None,  # Set to `None` to disable
            homepage=_HOMEPAGE_URL,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager: tfds.download.DownloadManager):
        """Returns SplitGenerators."""
        data_path = dl_manager.manual_dir / "galaxy_zoo_decals"
        csv_path = data_path / self.builder_config.csv_name
        image_paths = [data_path / f"gz_decals_dr5_png_part{i}" for i in range(1, 5)]
        return {
            "train": self._generate_examples(image_paths, csv_path),
        }

    def _generate_examples(self, image_paths, csv_path):
        """Yields examples."""
        with csv_path.open() as f:
            for row in csv.DictReader(f):
                iauname = row["iauname"]

                if self.builder_config.auto:
                    for field in row:
                        if "_concentration" in field:
                            row[field] = ast.literal_eval(row[field])

                image_path = find_image_path(iauname, image_paths)

                if image_path:
                    yield iauname, {
                        "image": image_path,
                        "morphology": {
                            k: "nan" if row[k] == "" else row[k]
                            for k in self.morphology_features
                        },
                        "metadata": {
                            k: "nan" if row[k] == "" else row[k] for k in _METADATA
                        },
                    }
