"""Command-line interface."""
import typer

from galaxies_datasets.scripts import app

typer_click_object = typer.main.get_command(app)

if __name__ == "__main__":
    app()
