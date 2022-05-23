"""Available Scripts."""
import typer

from galaxies_datasets.scripts import documentation
from galaxies_datasets.scripts import eagle
from galaxies_datasets.scripts import galaxyzoo3d

app = typer.Typer()
app.add_typer(eagle.app, name="eagle")
app.add_typer(galaxyzoo3d.app, name="galaxyzoo3d")
app.add_typer(documentation.app, name="documentation")
