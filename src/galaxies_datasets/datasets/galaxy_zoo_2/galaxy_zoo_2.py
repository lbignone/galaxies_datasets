"""galaxy_zoo_2 dataset."""
import pandas as pd
import tensorflow as tf
import tensorflow_datasets as tfds

_URL = "https://zenodo.org/record/3565489#.YSOxXffQ9hF"
_URL_GZ = "https://data.galaxyzoo.org/"

_DESCRIPTION = f"""
Dataset containing images from the "original" sample of subject images in
Galaxy Zoo 2 and morphological classification from Hart et al. (2016).
Images are obtained from [this repository]({_URL}) and
the morhological classification from "GZ2 - Table 1 - Normal-depth sample
with new debiasing method – CSV" (from Hart et al. 2016), which is available at
[data.galaxyzoo.org]({_URL_GZ})
"""

_CITATION = r"""
@ARTICLE{2013MNRAS.435.2835W,
       author = {{Willett}, Kyle W. and
                 {Lintott}, Chris J. and
                 {Bamford}, Steven P. and
                 {Masters}, Karen L. and
                 {Simmons}, Brooke D. and
                 {Casteels}, Kevin R.~V. and
                 {Edmondson}, Edward M. and
                 {Fortson}, Lucy F. and
                 {Kaviraj}, Sugata and
                 {Keel}, William C. and
                 {Melvin}, Thomas and
                 {Nichol}, Robert C. and
                 {Raddick}, M. Jordan and
                 {Schawinski}, Kevin and
                 {Simpson}, Robert J. and
                 {Skibba}, Ramin A. and
                 {Smith}, Arfon M. and
                 {Thomas}, Daniel},
        title = "{Galaxy Zoo 2: detailed morphological classifications for
        304 122 galaxies from the Sloan Digital Sky Survey}",
      journal = {\mnras},
     keywords = {methods: data analysis, catalogues, galaxies: elliptical and
      lenticular, galaxies: general, galaxies: spiral,
      Astrophysics - Cosmology and Nongalactic Astrophysics},
         year = 2013,
        month = nov,
       volume = {435},
       number = {4},
        pages = {2835-2860},
          doi = {10.1093/mnras/stt1458},
archivePrefix = {arXiv},
       eprint = {1308.3496},
 primaryClass = {astro-ph.CO},
       adsurl = {https://ui.adsabs.harvard.edu/abs/2013MNRAS.435.2835W},
      adsnote = {Provided by the SAO/NASA Astrophysics Data System}
}

@ARTICLE{2016MNRAS.461.3663H,
       author = {{Hart}, Ross E. and
                 {Bamford}, Steven P. and
                 {Willett}, Kyle W. and {Masters}, Karen L. and
                 {Cardamone}, Carolin and
                 {Lintott}, Chris J. and
                 {Mackay}, Robert J. and
                 {Nichol}, Robert C. and
                 {Rosslowe}, Christopher K. and
                 {Simmons}, Brooke D. and
                 {Smethurst}, Rebecca J.},
        title = "{Galaxy Zoo: comparing the demographics of spiral arm number
        and a new method for correcting redshift bias}",
      journal = {\mnras},
     keywords = {methods: data analysis, galaxies: formation,
     galaxies: general, galaxies: spiral,
     galaxies: structure, Astrophysics - Astrophysics of Galaxies},
         year = 2016,
        month = oct,
       volume = {461},
       number = {4},
        pages = {3663-3682},
          doi = {10.1093/mnras/stw1588},
archivePrefix = {arXiv},
       eprint = {1607.01019},
 primaryClass = {astro-ph.GA},
       adsurl = {https://ui.adsabs.harvard.edu/abs/2016MNRAS.461.3663H},
      adsnote = {Provided by the SAO/NASA Astrophysics Data System}
}

@dataset{willett_kyle_w_2013_3565489,
  author       = {Willett, Kyle W. and
                  Lintott, Chris J. and
                  Bamford, Steven P. and
                  Masters, Karen L. and
                  Simmons, Brooke D. and
                  Casteels, Kevin R. V. and
                  Edmonson, Edward M. and
                  Fortson, Lucy F. and
                  Kaviraj, Sugata and
                  Keel, William C. and
                  Melvin, Thomas and
                  Nichol, Robert C. and
                  Raddick, M. Jordan and
                  Schawinski, Kevin and
                  Simpson, Robert J. and
                  Skibba, Ramin A. and
                  Smith, Arfon M. and
                  Thomas, Daniel},
  title        = {Galaxy Zoo 2: Images from Original Sample},
  month        = nov,
  year         = 2013,
  publisher    = {Zenodo},
  version      = {Original},
  doi          = {10.5281/zenodo.3565489},
  url          = {https://doi.org/10.5281/zenodo.3565489}
}


"""

_METADATA = {
    "dr7objid": tf.int64,
    "ra": tf.float64,
    "dec": tf.float64,
    "rastring": tf.string,
    "decstring": tf.string,
}


_QUESTIONS = {
    "t01_smooth_or_features": [
        "a01_smooth",
        "a02_features_or_disk",
        "a03_star_or_artifact",
    ],
    "t02_edgeon": [
        "a04_yes",
        "a05_no",
    ],
    "t03_bar": [
        "a06_bar",
        "a07_no_bar",
    ],
    "t04_spiral": [
        "a08_spiral",
        "a09_no_spiral",
    ],
    "t05_bulge_prominence": [
        "a10_no_bulge",
        "a11_just_noticeable",
        "a12_obvious",
        "a13_dominant",
    ],
    "t06_odd": [
        "a14_yes",
        "a15_no",
    ],
    "t07_rounded": [
        "a16_completely_round",
        "a17_in_between",
        "a18_cigar_shaped",
    ],
    "t08_odd_feature": [
        "a19_ring",
        "a20_lens_or_arc",
        "a21_disturbed",
        "a22_irregular",
        "a23_other",
        "a24_merger",
        "a38_dust_lane",
    ],
    "t09_bulge_shape": [
        "a25_rounded",
        "a26_boxy",
        "a27_no_bulge",
    ],
    "t10_arms_winding": [
        "a28_tight",
        "a29_medium",
        "a30_loose",
    ],
    "t11_arms_number": [
        "a31_1",
        "a32_2",
        "a33_3",
        "a34_4",
        "a36_more_than_4",
        "a37_cant_tell",
    ],
}


def morphology_features(questions):
    """Compose features dictionary."""
    d = {}
    d["gz2_class"] = tf.string
    d["total_classifications"] = tf.int64
    d["total_votes"] = tf.int64
    for question in questions:
        for answer in questions[question]:
            d[f"{question}_{answer}_count"] = tf.int64
            d[f"{question}_{answer}_weight"] = tf.float64
            d[f"{question}_{answer}_fraction"] = tf.float64
            d[f"{question}_{answer}_weighted_fraction"] = tf.float64
            d[f"{question}_{answer}_debiased"] = tf.float64
            d[f"{question}_{answer}_flag"] = tf.int64

    return d


def merge_cvs(table1_csv, mapping_csv):
    """Merge table1 and mapping tables."""
    df_table1 = pd.read_csv(table1_csv)
    df_mapping = pd.read_csv(mapping_csv)
    df = df_table1.merge(df_mapping, left_on="dr7objid", right_on="objid")
    return df


class GalaxyZoo2(tfds.core.GeneratorBasedBuilder):
    """DatasetBuilder for galaxy_zoo_2 dataset."""

    VERSION = tfds.core.Version("1.0.0")
    RELEASE_NOTES = {
        "1.0.0": "Initial release.",
    }

    MANUAL_DOWNLOAD_INSTRUCTIONS = f"""
    Download from [this Zenodo repository]({_URL}) files:

    - gz2_filename_mapping.csv
    - images_gz2.zip

    Download from the [galaxy zoo data site]({_URL_GZ}) file:

    - gz2_hart16.csv

    Extract them in `manual_dir/galaxy_zoo_2`.
    """

    def _info(self) -> tfds.core.DatasetInfo:
        """Returns the dataset metadata."""
        return tfds.core.DatasetInfo(
            builder=self,
            description=_DESCRIPTION,
            features=tfds.features.FeaturesDict(
                {
                    # These are the features of your dataset like images, labels ...
                    "image": tfds.features.Image(shape=(424, 424, 3)),
                    "table1": morphology_features(_QUESTIONS),
                    "metadata": _METADATA,
                }
            ),
            # If there's a common (input, target) tuple from the
            # features, specify them here. They'll be used if
            # `as_supervised=True` in `builder.as_dataset`.
            supervised_keys=None,  # Set to `None` to disable
            homepage=_URL,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager: tfds.download.DownloadManager):
        """Returns SplitGenerators."""
        data_path = dl_manager.manual_dir / "galaxy_zoo_2"
        paths = {
            "images_path": data_path / "images",
            "mapping_csv": data_path / "gz2_filename_mapping.csv",
            "table1_csv": data_path / "gz2_hart16.csv",
        }

        return {
            "train": self._generate_examples(paths),
        }

    def _generate_examples(self, path):
        """Yields examples."""
        df = merge_cvs(path["table1_csv"], path["mapping_csv"])
        df = df.set_index("asset_id")

        for image_path in path["images_path"].glob("*.jpg"):
            asset_id = int(image_path.name.split(".")[0])
            if asset_id in df.index:
                row = df.loc[asset_id]
                yield asset_id, {
                    "image": image_path,
                    "table1": {k: row[k] for k in morphology_features(_QUESTIONS)},
                    "metadata": {k: row[k] for k in _METADATA},
                }
