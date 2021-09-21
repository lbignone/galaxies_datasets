"""eagle dataset."""
import csv

import tensorflow as tf
import tensorflow_datasets as tfds

_DESCRIPTION = """
This dataset contains mock galaxy images generated from the [EAGLE collection of
hydrodynamic cosmological simulations](http://icc.dur.ac.uk/Eagle/).

Images are 256x256x3 pngs in three orientation: edge-on, face-on and box, ie.
aligned with the xy projection of the simulation box.

Entries in the dataset are identified by their GalaxyID, matching the ones in the
EAGLE public database. The snapshot number is also included.

Datasets for each simulation can be access using the name `eagle/simulation` (e.g.
`eagle/RefL0100N1504`)

Available simulations are:

- RefL0100N1504
- RefL0025N0752
- RefL0025N0376
- RecalL0025N0752
"""

_CITATION = """
@ARTICLE{2017MNRAS.470..771T,
       author = {{Trayford}, James W. and {Camps}, Peter and {Theuns}, Tom and
         {Baes}, Maarten and {Bower}, Richard G. and {Crain}, Robert A. and
         {Gunawardhana}, Madusha L.~P. and {Schaller}, Matthieu and
         {Schaye}, Joop and {Frenk}, Carlos S.},
        title = "{Optical colours and spectral indices of z = 0.1 eagle
        galaxies with the 3D dust radiative transfer code skirt}",
      journal = {MNRAS},
         year = 2017,
        month = sep,
       volume = {470},
       number = {1},
        pages = {771-799},
          doi = {10.1093/mnras/stx1051},
       adsurl = {https://ui.adsabs.harvard.edu/abs/2017MNRAS.470..771T},
}
@ARTICLE{2016A&C....15...72M,
       author = {{McAlpine}, S. and {Helly}, J.~C. and {Schaller}, M. and
         {Trayford}, J.~W. and {Qu}, Y. and {Furlong}, M. and {Bower}, R.~G.
         and {Crain}, R.~A. and {Schaye}, J. and {Theuns}, T. and
         {Dalla Vecchia}, C. and {Frenk}, C.~S. and {McCarthy}, I.~G. and
         {Jenkins}, A. and {Rosas-Guevara}, Y. and {White}, S.~D.~M. and
         {Baes}, M. and {Camps}, P. and {Lemson}, G.},
        title = "{The EAGLE simulations of galaxy formation: Public release of
        halo and galaxy catalogues}",
      journal = {Astronomy and Computing},
         year = 2016,
        month = apr,
       volume = {15},
        pages = {72-89},
          doi = {10.1016/j.ascom.2016.02.004},
       adsurl = {https://ui.adsabs.harvard.edu/abs/2016A&C....15...72M},
}
@ARTICLE{2015MNRAS.446..521S,
       author = {{Schaye}, Joop and {Crain}, Robert A. and {Bower}, Richard G.
       and {Furlong}, Michelle and {Schaller}, Matthieu and {Theuns}, Tom and
         {Dalla Vecchia}, Claudio and {Frenk}, Carlos S. and {McCarthy}, I.~G.
          and {Helly}, John C. and {Jenkins}, Adrian
          and {Rosas-Guevara}, Y.~M. and {White}, Simon D.~M. and {Baes},
          Maarten and {Booth}, C.~M. and {Camps}, Peter and {Navarro},
          Julio F. and {Qu}, Yan and {Rahmati}, Alireza and {Sawala}, Till
          and {Thomas}, Peter A. and {Trayford}, James},
        title = "{The EAGLE project: simulating the evolution and assembly of
         galaxies and their environments}",
      journal = {MNRAS},
         year = 2015,
        month = jan,
       volume = {446},
       number = {1},
        pages = {521-554},
          doi = {10.1093/mnras/stu2058},
       adsurl = {https://ui.adsabs.harvard.edu/abs/2015MNRAS.446..521S},
}
"""


class Eagle(tfds.core.GeneratorBasedBuilder):
    """DatasetBuilder for eagle dataset."""

    VERSION = tfds.core.Version("1.0.0")
    RELEASE_NOTES = {
        "1.0.0": "Initial release.",
    }

    MANUAL_DOWNLOAD_INSTRUCTIONS = """
    Galaxies_datasets has a dedicated script to download EAGLE data.

    Usage:

        galaxies_datasets eagle download [OPTIONS] USER SIMULATION

    For more information and additional options run:

        galaxies_datasets eagle download --help
    """

    BUILDER_CONFIGS = [
        # `name` (and optionally `description`) are required for each config
        tfds.core.BuilderConfig(name="RefL0100N1504"),
        tfds.core.BuilderConfig(name="RefL0025N0752"),
        tfds.core.BuilderConfig(name="RefL0025N0376"),
        tfds.core.BuilderConfig(name="RecalL0025N0752"),
    ]

    def _info(self) -> tfds.core.DatasetInfo:
        """Returns the dataset metadata."""
        return tfds.core.DatasetInfo(
            builder=self,
            description=_DESCRIPTION,
            features=tfds.features.FeaturesDict(
                {
                    # These are the features of your dataset like images, labels ...
                    "GalaxyID": tf.int64,
                    "Image_box": tfds.features.Image(
                        shape=(256, 256, 3), encoding_format="png"
                    ),
                    "Image_edge": tfds.features.Image(
                        shape=(256, 256, 3), encoding_format="png"
                    ),
                    "Image_face": tfds.features.Image(
                        shape=(256, 256, 3), encoding_format="png"
                    ),
                    "Snapshot": tfds.features.ClassLabel(num_classes=28),
                    "Sizes": {
                        "R_halfmass30": tf.float32,
                        "R_halfmass100": tf.float32,
                        "R_halfmass30_projected": tf.float32,
                        "R_halfmass100_projected": tf.float32,
                    },
                }
            ),
            # If there's a common (input, target) tuple from the
            # features, specify them here. They'll be used if
            # `as_supervised=True` in `builder.as_dataset`.
            supervised_keys=None,  # Set to `None` to disable
            homepage="https://icc.dur.ac.uk/Eagle/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager: tfds.download.DownloadManager):
        """Returns SplitGenerators."""
        path = dl_manager.manual_dir / self.builder_config.name

        return {
            "train": self._generate_examples(path),
        }

    def _generate_examples(self, path):
        """Yields examples."""
        for snap_path in path.iterdir():
            csv_path = snap_path / "data.csv"
            images_path = snap_path / "images"
            with tf.io.gfile.GFile(csv_path, "r") as f:
                for row in csv.DictReader(f):
                    if int(row["Image_ID"]) != -1:
                        galaxy_id = row["GalaxyID"]
                        image_box_path = images_path / f"galrand_{galaxy_id}.png"
                        image_edge_path = images_path / f"galedge_{galaxy_id}.png"
                        image_face_path = images_path / f"galface_{galaxy_id}.png"
                        example = {
                            "GalaxyID": galaxy_id,
                            "Image_box": image_box_path,
                            "Image_edge": image_edge_path,
                            "Image_face": image_face_path,
                            "Snapshot": row["SnapNum"],
                            "Sizes": {
                                "R_halfmass30": row["R_halfmass30"],
                                "R_halfmass100": row["R_halfmass100"],
                                "R_halfmass30_projected": row["R_halfmass30_projected"],
                                "R_halfmass100_projected": row[
                                    "R_halfmass100_projected"
                                ],
                            },
                        }
                        yield galaxy_id, example
