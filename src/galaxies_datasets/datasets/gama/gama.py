"""gama dataset."""
import tensorflow_datasets as tfds

_DESCRIPTION = """
Dataset containing SDSS images corresponding to galaxies in the GAMA survey. Sources
selection is based on Porter-Temple et al. (2022).
"""

_CITATION = """
@ARTICLE{2011MNRAS.413..971D,
        author = {{Driver}, S.~P. and
                 {Hill}, D.~T. and
                 {Kelvin}, L.~S. and
                 {Robotham}, A.~S.~G. and
                 {Liske}, J. and
                 {Norberg}, P. and
                 {Baldry}, I.~K. and
                 {Bamford}, S.~P. and
                 {Hopkins}, A.~M. and
                 {Loveday}, J. and
                 {Peacock}, J.~A. and
                 {Andrae}, E. and
                 {Bland-Hawthorn}, J. and
                 {Brough}, S. and
                 {Brown}, M.~J.~I. and
                 {Cameron}, E. and
                 {Ching}, J.~H.~Y. and
                 {Colless}, M. and
                 {Conselice}, C.~J. and
                 {Croom}, S.~M. and
                 {Cross}, N.~J.~G. and
                 {de Propris}, R. and
                 {Dye}, S. and
                 {Drinkwater}, M.~J. and
                 {Ellis}, S. and
                 {Graham}, Alister W. and
                 {Grootes}, M.~W. and
                 {Gunawardhana}, M. and
                 {Jones}, D.~H. and
                 {van Kampen}, E. and
                 {Maraston}, C. and
                 {Nichol}, R.~C. and
                 {Parkinson}, H.~R. and
                 {Phillipps}, S. and
                 {Pimbblet}, K. and
                 {Popescu}, C.~C. and
                 {Prescott}, M. and
                 {Roseboom}, I.~G. and
                 {Sadler}, E.~M. and
                 {Sansom}, A.~E. and
                 {Sharp}, R.~G. and
                 {Smith}, D.~J.~B. and
                 {Taylor}, E. and
                 {Thomas}, D. and
                 {Tuffs}, R.~J. and
                 {Wijesinghe}, D. and
                 {Dunne}, L. and
                 {Frenk}, C.~S. and
                 {Jarvis}, M.~J. and
                 {Madore}, B.~F. and
                 {Meyer}, M.~J. and
                 {Seibert}, M. and
                 {Staveley-Smith}, L. and
                 {Sutherland}, W.~J. and
                 {Warren}, S.~J.},
        title = "{Galaxy and Mass Assembly (GAMA): survey diagnostics and core data
        release}",
        journal = {MNRAS},
        keywords = {surveys, galaxies: distances and redshifts, galaxies: fundamental
        parameters, galaxies: general, galaxies: statistics, Astrophysics - Cosmology
        and Nongalactic Astrophysics},
        year = 2011,
        month = may,
        volume = {413},
        number = {2},
        pages = {971-995},
        doi = {10.1111/j.1365-2966.2010.18188.x}
"""

_IMAGE_WIDTH = 525


class Gama(tfds.core.GeneratorBasedBuilder):
    """DatasetBuilder for GAMA dataset."""

    VERSION = tfds.core.Version("1.0.0")
    RELEASE_NOTES = {
        "1.0.0": "Initial release.",
    }

    MANUAL_DOWNLOAD_INSTRUCTIONS = """
      Manually extract the data to the `tensorflow_datasets/downloads/manual/GAMA`
      directory
      """

    def _info(self) -> tfds.core.DatasetInfo:
        """Returns the dataset metadata."""
        return tfds.core.DatasetInfo(
            builder=self,
            description=_DESCRIPTION,
            features=tfds.features.FeaturesDict(
                {
                    # These are the features of your dataset like images, labels ...
                    "cataid": tfds.features.Text(),
                    "image": tfds.features.Image(shape=(_IMAGE_WIDTH, _IMAGE_WIDTH, 3)),
                }
            ),
            # If there's a common (input, target) tuple from the
            # features, specify them here. They'll be used if
            # `as_supervised=True` in `builder.as_dataset`.
            # supervised_keys=('image', 'label'),  # Set to `None` to disable
            supervised_keys=None,
            homepage="""
        http://www.gama-survey.org/
        """,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager: tfds.download.DownloadManager):
        """Returns SplitGenerators."""
        path = dl_manager.manual_dir / "GAMA" / "SDSS images"

        return {
            "train": self._generate_examples(path),
        }

    def _generate_examples(self, path):
        """Yields examples."""
        for f in path.glob("*.jpg"):
            cataid = f.name.split(".")[0]  # use as key

            yield cataid, {
                "cataid": cataid,
                "image": f,
            }
