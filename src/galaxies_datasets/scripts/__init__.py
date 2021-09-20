"""Available Scripts."""
import typer

from galaxies_datasets.scripts import documentation
from galaxies_datasets.scripts import eagle

app = typer.Typer()
app.add_typer(eagle.app, name="eagle")
app.add_typer(documentation.app, name="documentation")
