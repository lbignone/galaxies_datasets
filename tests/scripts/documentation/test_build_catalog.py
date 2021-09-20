"""Test build_catalog."""
import tensorflow_datasets as tfds

from galaxies_datasets.scripts.documentation.build_catalog import empty_string_for_none
from galaxies_datasets.scripts.documentation.build_catalog import (
    get_catalog_documentation,
)
from galaxies_datasets.scripts.documentation.build_catalog import (
    get_dataset_documentation,
)
from galaxies_datasets.scripts.documentation.build_catalog import get_documentation_info
from galaxies_datasets.scripts.documentation.build_catalog import list_datasets
from galaxies_datasets.scripts.documentation.build_catalog import load_all_configs
from galaxies_datasets.scripts.documentation.build_catalog import load_dataset_template


def test_empty_string_for_none():
    """When None replace by empty strings."""
    test_string = "not empty"
    assert empty_string_for_none(test_string) == test_string
    assert empty_string_for_none(None) == ""


def test_list_datasets():
    """Test list_dataset."""
    datasets_inspection = list_datasets()
    assert len(datasets_inspection) > 0
    for _, value in datasets_inspection:
        assert issubclass(value, tfds.core.GeneratorBasedBuilder)


def test_get_documentation_basic_info():
    """Test basic documentation data retrieval."""
    builder = tfds.builder("eagle")
    info = get_documentation_info(builder)
    assert isinstance(info, dict)
    assert isinstance(info["description"], str)
    assert isinstance(info["homepage"], str)
    assert isinstance(info["MANUAL_DOWNLOAD_INSTRUCTIONS"], str)


def test_load_all_configs():
    """Test that all configs are retrieved."""
    base_builder = tfds.builder("eagle")
    builders = load_all_configs(base_builder)
    assert isinstance(builders, list)
    for builder in builders:
        assert isinstance(builder, tfds.core.DatasetBuilder)

    base_builder = tfds.builder("mnist")
    builders = load_all_configs(base_builder)
    assert len(builders) == 0


def test_load_dataset_template():
    """Test loaded template is string."""
    template = load_dataset_template()
    assert isinstance(template, str)


def test_get_dataset_documentation():
    """Test dataset documentation is string."""
    builder = tfds.builder("eagle")
    documentation = get_dataset_documentation(builder)
    assert isinstance(documentation, str)


def test_get_catalog_documentation():
    """Test documenting multiple datasets."""
    builders = [tfds.builder("eagle"), tfds.builder("mnist")]
    documentation = get_catalog_documentation(builders)
    assert isinstance(documentation, str)
    assert "eagle" in documentation
    assert "mnist" in documentation
