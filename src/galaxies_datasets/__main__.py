"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Galaxies Datasets."""


if __name__ == "__main__":
    main(prog_name="galaxies_datasets")  # pragma: no cover
