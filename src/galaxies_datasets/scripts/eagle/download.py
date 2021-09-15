"""Download images and data from the EAGLE simulation public database."""
import pathlib
import re
from enum import Enum
from importlib import resources
from typing import Optional

import pandas as pd
import requests
import typer
from eagleSqlTools import connect
from eagleSqlTools._eagleSqlTools import _WebDBConnection
from requests.adapters import HTTPAdapter
from tqdm.auto import tqdm

app = typer.Typer()

home_path = pathlib.Path.home()
default_manual_dir = home_path / "tensorflow_datasets/downloads/manual/"


class EagleOrientation(Enum):
    """Available image camera orientations."""

    face = "face"
    edge = "edge"
    box = "box"


def table_query(
    simulation: str, snap_number: int, min_mass_star: float, table: str
) -> str:
    """Composes the sql query from a template."""
    template = resources.read_text("galaxies_datasets.scripts.eagle", "table_query.sql")
    query = template.format(
        simulation=simulation,
        snap_number=snap_number,
        min_mass_star=min_mass_star,
        table=table,
    )

    return query


def download_table(
    connection: _WebDBConnection,
    simulation: str,
    snap_number: int,
    min_mass_star: float,
    table: str,
) -> pd.DataFrame:
    """Download a single table from the database."""
    query = table_query(simulation, snap_number, min_mass_star, table)
    result = connection._execute_query(query)
    df = pd.DataFrame(result)

    return df


def download_tables(
    connection: _WebDBConnection,
    simulation: str,
    snap_number: int,
    min_mass_star: float,
) -> pd.DataFrame:
    """Download tables and merge them."""
    tables = [
        "SubHalo",
        "Sizes",
    ]

    first = True
    df_tot = None
    pbar = tqdm(tables, leave=False)
    for table in pbar:
        pbar.set_description(f"Table {table}")
        df = download_table(connection, simulation, snap_number, min_mass_star, table)
        if first:
            df_tot = df
            first = False
        else:
            df_tot = pd.merge(df_tot, df, on="GalaxyID", how="outer")

    return df_tot


def strip_url(url: Optional[str]) -> Optional[str]:
    """Extract the image url from the image fields in the database."""
    if url:
        return re.search("'(.*)'", url).group(1)
    else:
        return url


def clean_urls(df: pd.DataFrame) -> None:
    """Clean the image urls in the dataframe."""
    for orientation in EagleOrientation:
        column = f"Image_{orientation.value}"
        data = df[column].str.decode("utf8").apply(strip_url)
        df[column] = data


def determine_manual_dir(manual_dir: Optional[pathlib.Path] = None):
    """Determine the manual_dir."""
    if manual_dir is None:
        manual_dir = default_manual_dir

    return manual_dir


def get_download_path(
    simulation: str,
    snap_number: int,
    manual_dir: Optional[pathlib.Path] = None,
):
    """Get the snapshot data download path."""
    manual_dir = determine_manual_dir(manual_dir)

    return manual_dir / f"{simulation}/{snap_number}"


def get_data_filepath(path: pathlib.Path) -> pathlib.Path:
    """Get the data download filepath."""
    return path / "data.csv"


def get_images_path(
    simulation: str,
    snap_number: int,
    manual_dir: Optional[pathlib.Path] = None,
) -> pathlib.Path:
    """Get the image download path."""
    download_path = get_download_path(simulation, snap_number, manual_dir)
    return download_path / "images"


def save_dataframe(df: pd.DataFrame, path: pathlib.Path) -> None:
    """Save the data to a csv file."""
    filepath = get_data_filepath(path)
    df.to_csv(filepath, index=False)


def download_and_save_data(
    connection: _WebDBConnection,
    simulation: str,
    snap_number: int,
    min_mass_star: float,
    manual_dir: Optional[pathlib.Path] = None,
) -> None:
    """Download the data for a single snapshot."""
    df = download_tables(connection, simulation, snap_number, min_mass_star)
    clean_urls(df)
    path = get_download_path(simulation, snap_number, manual_dir)
    path.mkdir(parents=True, exist_ok=True)
    save_dataframe(df, path)


def get_urls(
    simulation: str,
    snap_number: int,
    orientation: EagleOrientation,
    manual_dir: Optional[pathlib.Path] = None,
):
    """Retrieve the image urls for a specific orientation."""
    path = get_download_path(simulation, snap_number, manual_dir)
    filepath = get_data_filepath(path)
    df = pd.read_csv(filepath)
    sel = df[~df[f"Image_{orientation.value}"].isna()]

    result = sel[f"Image_{orientation.value}"]

    return result


def get_filename_from_url(url: str) -> str:
    """Get the image filename fro a url."""
    return url.split("/")[-1]


def download_images(
    simulation: str,
    snap_number: int,
    orientation: EagleOrientation,
    manual_dir: Optional[pathlib.Path] = None,
):
    """Download the images for a specific snapshot."""
    session = requests.Session()
    session.mount("http://", HTTPAdapter(max_retries=5))

    urls = get_urls(simulation, snap_number, orientation, manual_dir)

    images_path = get_images_path(simulation, snap_number, manual_dir)
    images_path.mkdir(parents=True, exist_ok=True)

    pbar = tqdm(urls, leave=False)
    for url in pbar:
        filename = get_filename_from_url(url)
        pbar.set_description(filename)
        path = images_path / filename

        response = session.get(url, timeout=10, stream=True)
        with open(path, "wb") as f:
            for chunk in response:
                f.write(chunk)


def print_info_message(
    user: str,
    simulation: str,
    start_snap_number: int,
    stop_snap_number: int,
    min_mass_star: float,
    manual_dir: Optional[pathlib.Path] = None,
) -> None:
    """Print an info message."""
    fg = typer.colors.MAGENTA

    typer.secho("You are requesting to download:", fg=fg)
    typer.secho(f"Simulation: {simulation}")
    typer.secho(f"start_snap_number: {start_snap_number}")
    typer.secho(f"stop_snap_number: {stop_snap_number}")
    typer.secho(f"min_mass_star: {min_mass_star:.1e}")

    path = determine_manual_dir(manual_dir)
    typer.secho("Download location", fg=fg)
    typer.secho(f"{path}")

    database_url = "http://icc.dur.ac.uk/Eagle/database.php"
    typer.secho(f"Login to the EAGLE Public Database ({database_url})", fg=fg)

    typer.secho(f"User: {user}")


user_arg = typer.Argument(..., help="Username for the EAGLE public database")
simulation_arg = typer.Argument(..., help="Name of the EAGLE simulation")
start_snap_number_arg = typer.Option(12, help="Starting snapshot to download")
stop_snap_number_arg = typer.Option(
    28, help="Stopping (exclusive) snapshot " "to download"
)
min_mass_star_arg = typer.Option(
    1e8, help="Minimum stellar mass of galaxies to download"
)
manual_dir_arg = typer.Option(None, "--manual_dir", help="Where to download data.")


@app.command()
def download(
    user: str = user_arg,
    simulation: str = simulation_arg,
    start_snap_number: int = start_snap_number_arg,
    stop_snap_number: int = stop_snap_number_arg,
    min_mass_star: float = min_mass_star_arg,
    manual_dir: pathlib.Path = manual_dir_arg,
) -> None:
    """Download images and data from the EAGLE simulation public database."""
    print_info_message(
        user, simulation, start_snap_number, stop_snap_number, min_mass_star, manual_dir
    )
    connection = connect(user)

    pbar = tqdm(range(start_snap_number, stop_snap_number))
    for snap_number in pbar:
        pbar.set_description(f"Snapshot #{snap_number}")
        download_and_save_data(
            connection, simulation, snap_number, min_mass_star, manual_dir
        )
        orientation_pbar = tqdm(EagleOrientation)
        for orientation in orientation_pbar:
            orientation_pbar.set_description(f"Orientation {orientation.value}")
            download_images(simulation, snap_number, orientation, manual_dir)


if __name__ == "__main__":
    app()
