"""Test cases for the download_eagle script."""
import pathlib

import pandas as pd
from eagleSqlTools._eagleSqlTools import _WebDBConnection

from galaxies_datasets.scripts.eagle.download import clean_urls
from galaxies_datasets.scripts.eagle.download import default_manual_dir
from galaxies_datasets.scripts.eagle.download import download_and_save_data
from galaxies_datasets.scripts.eagle.download import download_table
from galaxies_datasets.scripts.eagle.download import download_tables
from galaxies_datasets.scripts.eagle.download import EagleOrientation
from galaxies_datasets.scripts.eagle.download import get_download_path
from galaxies_datasets.scripts.eagle.download import get_filename_from_url
from galaxies_datasets.scripts.eagle.download import get_images_path
from galaxies_datasets.scripts.eagle.download import get_urls
from galaxies_datasets.scripts.eagle.download import save_dataframe
from galaxies_datasets.scripts.eagle.download import strip_url
from galaxies_datasets.scripts.eagle.download import table_query


THIS_DIR = pathlib.Path(__file__).parent


class DummyConnection(_WebDBConnection):
    """Dummy implementation of the EAGLE database connection."""

    def __init__(self):
        """Override init."""
        self.counter = 0

    def _execute_query(self, query):
        galaxy_ids = [89, 45]
        queries = [query] * 2
        url = (
            "<img src='http://virgodb.cosma.dur.ac.uk/eagle-webstorage"
            "/RefL0025N0752_Subhalo/galface_1848107.png'>"
        )
        # apparently the incoming data comes encoded
        url = url.encode("utf8")

        image_urls = [url, None]
        d = {
            "GalaxyID": galaxy_ids,
            f"query_{self.counter}": queries,
        }
        if self.counter == 0:
            d_urls = {
                f"Image_{orientation.value}": image_urls
                for orientation in EagleOrientation
            }
            d = {**d, **d_urls}
        self.counter += 1
        return d


def test_table_query():
    """Test the table query template."""
    path = THIS_DIR / "table_query_test.sql"
    with open(path, encoding="utf-8", errors="strict") as f:
        expected_sql = f.read()

    obtained_sql = table_query("RecalL0025N0752", 27, 1e8, "Magnitudes")

    assert expected_sql == obtained_sql


def test_download_table():
    """Test that data is retrieved after a query."""
    path = THIS_DIR / "table_query_test.sql"
    with open(path, encoding="utf-8", errors="strict") as f:
        expected_sql = f.read()

    connection = DummyConnection()
    data = download_table(connection, "RecalL0025N0752", 27, 1e8, "Magnitudes")
    assert isinstance(data, pd.DataFrame)
    assert data["query_0"].iloc[0] == expected_sql


def test_download_tables():
    """Test that both tables are downloaded and merged."""
    connection = DummyConnection()
    data = download_tables(connection, "test_simulation", 27, 1e8)
    assert isinstance(data, pd.DataFrame)
    assert "SubHalo" in data["query_0"].iloc[0]
    assert "Sizes" in data["query_1"].iloc[0]


def test_strip_url():
    """Test that the url is correctly extracted."""
    url = (
        "<img src='http://virgodb.cosma.dur.ac.uk/eagle-webstorage"
        "/RefL0025N0752_Subhalo/galface_1848107.png'>"
    )
    expected = (
        "http://virgodb.cosma.dur.ac.uk/eagle-webstorage"
        "/RefL0025N0752_Subhalo/galface_1848107.png"
    )
    obtained = strip_url(url)
    assert obtained == expected


def test_strip_url_none():
    """Test that missing urls are ignored."""
    url = None
    expected = None
    obtained = strip_url(url)
    assert obtained == expected


def test_clean_urls():
    """Test that image url fields are correctly clean."""
    connection = DummyConnection()
    expected = (
        "http://virgodb.cosma.dur.ac.uk/eagle-webstorage"
        "/RefL0025N0752_Subhalo/galface_1848107.png"
    )
    data = download_tables(connection, "test_simulation", 27, 1e8)
    clean_urls(data)
    for orientation in EagleOrientation:
        assert data[f"Image_{orientation.value}"].iloc[0] == expected
        assert data[f"Image_{orientation.value}"].iloc[1] is None


def test_save_dataframe(tmp_path):
    """Test that the data is saved."""
    connection = DummyConnection()
    data = download_tables(connection, "test_simulation", 27, 1e8)
    clean_urls(data)
    save_dataframe(data, tmp_path)
    filepath = tmp_path / "data.csv"
    saved_df = pd.read_csv(filepath)
    pd.testing.assert_frame_equal(data, saved_df)


def test_default_download_path():
    """Test that the default download path is correctly set."""
    simulation = "RefL0025N0752"
    snap_number = 27
    expected_path = default_manual_dir / f"{simulation}/{snap_number}"
    actual = get_download_path(simulation, snap_number)
    assert actual == expected_path


def test_custom_download_path(tmp_path):
    """Test that a custom download path is correctly set."""
    simulation = "RefL0025N0752"
    snap_number = 27
    expected_path = tmp_path / f"{simulation}/{snap_number}"
    actual = get_download_path(simulation, snap_number, tmp_path)
    assert actual == expected_path


def test_download_and_save_data(tmp_path):
    """Test that data is downloaded and saved."""
    connection = DummyConnection()
    simulation = "test_sim"
    snap_number = 27
    min_mass_star = 1e8
    path = tmp_path / f"{simulation}/{snap_number}"
    download_and_save_data(connection, simulation, snap_number, min_mass_star, tmp_path)
    df = pd.read_csv(path / "data.csv")
    assert isinstance(df, pd.DataFrame)


def test_get_urls(tmp_path):
    """Test that image url retrieval."""
    connection = DummyConnection()
    simulation = "test_sim"
    snap_number = 27
    min_mass_star = 1e8
    orientation = EagleOrientation.face
    download_and_save_data(connection, simulation, snap_number, min_mass_star, tmp_path)
    urls = get_urls(simulation, snap_number, orientation, tmp_path)

    expected_url = (
        "http://virgodb.cosma.dur.ac.uk/eagle-webstorage"
        "/RefL0025N0752_Subhalo/galface_1848107.png"
    )

    assert urls.iloc[0] == expected_url
    assert urls.isna().sum() == 0


def test_get_images_path(tmp_path):
    """Test the image download path."""
    simulation = "test_sim"
    snap_number = 27
    expected_path = tmp_path / f"{simulation}/{snap_number}/images"
    images_path = get_images_path(simulation, snap_number, tmp_path)
    assert images_path == expected_path


def test_get_filename_from_url():
    """Test that the image filename is extracted from the url."""
    url = (
        "http://virgodb.cosma.dur.ac.uk/eagle-webstorage"
        "/RefL0025N0752_Subhalo/galface_1848107.png"
    )
    expected_filename = "galface_1848107.png"
    filename = get_filename_from_url(url)
    assert filename == expected_filename
