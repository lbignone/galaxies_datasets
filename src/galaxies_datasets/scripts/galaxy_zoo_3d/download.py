"""Download segmentation maps from Galaxy Zoo 3D."""
import time
from pathlib import Path

import requests
import typer
from requests.adapters import HTTPAdapter
from requests.adapters import Retry
from requests.packages import urllib3
from tqdm.auto import tqdm

# Use requests instead of urllib.request

app = typer.Typer()


@app.command()
def download():
    """Download Galaxy Zoo 3D segmentation maps."""
    # define a timeout so the programs exits in case of server failure
    timeout = 10
    # flag to skip ssl certificate verification
    verify = False
    # disable ssl verification warnings
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # using a single shared session should result in better performance
    session = requests.Session()

    # setup retries
    retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
    session.mount("https://", HTTPAdapter(max_retries=retries))

    # default download location
    home_path = Path.home()
    default_manual_dir = home_path / "tensorflow_datasets/downloads/manual/"
    basepath = default_manual_dir / "galaxyzoo3d"
    basepath.mkdir(exist_ok=True, parents=True)

    # Bajo el archivo .sha1sum en el que están los nombres de todos los archivos .gz
    # que queremos bajar y sus respectivos sha1sum.
    url = "https://data.sdss.org/sas/dr17/manga/morphology/galaxyzoo3d/v4_0_0/"
    sha1sum = "manga_morphology_galaxyzoo3d_v4_0_0.sha1sum"
    response = session.get(url + sha1sum, timeout=timeout, verify=verify)
    with open(basepath / sha1sum, "wb") as f:
        f.write(response.content)

    archivos = open(basepath / sha1sum, "r").read().split("\n")[:-1]
    gzs = [a.split(" ")[2] for a in archivos]
    # sha1sums = [a.split(" ")[0] for a in archivos]

    # Descargo todos los archivos comprimidos en .gz en la carpeta "Mapas".
    t_i = time.time()
    for filename in tqdm(gzs):
        path = basepath / filename
        # skip download if file already exists
        if not path.is_file():
            response = session.get(url + filename, timeout=timeout, verify=verify)
            with open(path, "wb") as f:
                f.write(response.content)

    t_f = time.time() - t_i
    print(
        "Tardó "
        + str(int(t_f / 3600))
        + " horas y "
        + str(round((t_f / 3600 % 1) * 60))
        + " minutos en descargar todos los archivos"
    )


if __name__ == "__main__":
    app()
