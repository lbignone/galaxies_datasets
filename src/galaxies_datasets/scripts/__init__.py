"""Available Scripts."""
import typer

from galaxies_datasets.scripts import documentation
from galaxies_datasets.scripts import eagle
from galaxies_datasets.scripts import galaxy_zoo_3d

app = typer.Typer()
app.add_typer(eagle.app, name="eagle")
app.add_typer(galaxy_zoo_3d.app, name="galaxy_zoo3d")
app.add_typer(documentation.app, name="documentation")
