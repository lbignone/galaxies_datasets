"""Build catalog script."""
import inspect
import pathlib
import textwrap
from importlib import resources
from typing import List
from typing import Optional

import tensorflow_datasets as tfds
import typer

from galaxies_datasets import datasets

app = typer.Typer()


def list_datasets():
    """Return all datasets in a list of (name, value) pairs sorted by name."""
    return inspect.getmembers(datasets, inspect.isclass)


def empty_string_for_none(string: Optional[str]):
    """If None return empty string."""
    if string is None:
        string = ""

    return string


def get_documentation_info(builder: tfds.core.DatasetBuilder) -> dict:
    """Return a dictionary containing the data to pass to the documentation template."""
    d = {
        "description": textwrap.dedent(builder.info.description),
        "homepage": empty_string_for_none(builder.info.homepage),
        "MANUAL_DOWNLOAD_INSTRUCTIONS": textwrap.dedent(
            empty_string_for_none(builder.MANUAL_DOWNLOAD_INSTRUCTIONS)
        ),
    }

    return d


def load_all_configs(
    builder: tfds.core.DatasetBuilder,
) -> List[tfds.core.DatasetBuilder]:
    """Load all builders from available configs."""
    return [
        tfds.builder(f"{builder.name}/{config_name}")
        for config_name in builder.builder_configs
    ]


def load_dataset_template():
    """Load the dataset documentation template."""
    return resources.read_text(
        "galaxies_datasets.scripts.documentation", "dataset_template.md"
    )


def get_dataset_documentation(builder: tfds.core.DatasetBuilder) -> str:
    """Get the documentation for a single dataset."""
    template = load_dataset_template()

    info = get_documentation_info(builder)
    info["name"] = builder.name
    result = template.format(**info)
    result += "\n"

    return result


def get_catalog_documentation(builders: List[tfds.core.DatasetBuilder]) -> str:
    """Get the dataset catalog."""
    documentation = "# Datasets\n"
    for builder in builders:
        documentation += get_dataset_documentation(builder)

    return documentation


@app.command()
def build_catalog(
    dataset: List[str] = typer.Option(  # noqa:B008
        None, "--dataset", "-d", help="Dataset to document"
    ),
    build_dir: Optional[pathlib.Path] = typer.Option(  # noqa:B008
        None, help="Path where to export catalog"
    ),
) -> None:
    """Build the dataset catalog documentation."""
    if not dataset:
        builders = [tfds.builder(value.name) for _, value in list_datasets()]
    else:
        builders = [tfds.builder(name) for name in dataset]

    if build_dir is None:
        build_dir = pathlib.Path(".")

    documentation = get_catalog_documentation(builders)

    with open(build_dir / "datasets.md", "w") as f:
        f.write(documentation)


if __name__ == "__main__":
    app()
