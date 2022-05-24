# Datasets

## eagle

**Description**:

This dataset contains mock galaxy images generated from the [EAGLE collection of
hydrodynamic cosmological simulations](http://icc.dur.ac.uk/Eagle/).

Images are 256x256x3 pngs in three orientation: edge-on, face-on and box, ie.
aligned with the xy projection of the simulation box.

Entries in the dataset are identified by their GalaxyID, matching the ones in the
EAGLE public database. The snapshot number is also included.

Datasets for each simulation can be access using the name `eagle/simulation` (e.g.
`eagle/RefL0100N1504`)

Available simulations are:

- RefL0100N1504
- RefL0025N0752
- RefL0025N0376
- RecalL0025N0752

**Homepage**: [https://icc.dur.ac.uk/Eagle/](https://icc.dur.ac.uk/Eagle/)

**Manual download instructions**:
Galaxies_datasets has a dedicated script to download EAGLE data.

Usage:

    galaxies_datasets eagle download [OPTIONS] USER SIMULATION

For more information and additional options run:

    galaxies_datasets eagle download --help

## galaxy_zoo2

**Description**:

Dataset containing images from the "original" sample of subject images in
Galaxy Zoo 2 and morphological classification from Hart et al. (2016).
Images are obtained from [this repository](https://zenodo.org/record/3565489#.YSOxXffQ9hF) and
the morhological classification from "GZ2 - Table 1 - Normal-depth sample
with new debiasing method – CSV" (from Hart et al. 2016), which is available at
[data.galaxyzoo.org](https://data.galaxyzoo.org/)

**Homepage**: [https://zenodo.org/record/3565489#.YSOxXffQ9hF](https://zenodo.org/record/3565489#.YSOxXffQ9hF)

**Manual download instructions**:
Download from [this Zenodo repository](https://zenodo.org/record/3565489#.YSOxXffQ9hF) files:

- gz2_filename_mapping.csv
- images_gz2.zip

Download from the [galaxy zoo data site](https://data.galaxyzoo.org/) file:

- gz2_hart16.csv

Extract them in `manual_dir/galaxy_zoo_2`.

## galaxy_zoo3d

**Description**:

Dataset containing crowd sourced spatial pixel (spaxel) maps identifying galaxy
centres, foreground stars, galactic bars and spiral arms in all galaxies in the
target file for the MaNGA survey. Data comes from the "Galaxy Zoo: 3D" project (
Masters et al. 2021).

**Homepage**: [
https://www.sdss.org/dr17/data_access/value-added-catalogs/?vac_id=galaxy-zoo-3d
](https://www.sdss.org/dr17/data_access/value-added-catalogs/?vac_id=galaxy-zoo-3d)

**Manual download instructions**:
GalaxyZoo3d has a dedicated script to download data.

Usage:

    galaxies_datasets galaxy_zoo3d download

## galaxy_zoo_challenge

**Description**:

This dataset contains the training data for the 2014 [Kaggle Galaxy Zoo
competion](https://www.kaggle.com/c/galaxy-zoo-the-galaxy-challenge). This includes images and labels.

**Homepage**: [https://www.kaggle.com/c/galaxy-zoo-the-galaxy-challenge](https://www.kaggle.com/c/galaxy-zoo-the-galaxy-challenge)

**Manual download instructions**:
Download the following files from the [Kaggle competition site](https://www.kaggle.com/c/galaxy-zoo-the-galaxy-challenge):

- images_training_rev1.zip
- images_test_rev1.zip
- training_solutions_rev1.zip

Extract them in `manual_dir/galaxy_zoo_challenge`

## galaxy_zoo_decals

**Description**:

This repository contains the data released in the paper "Galaxy Zoo DECaLS:
Detailed Visual Morphology Measurements from Volunteers and Deep Learning
for 314000 Galaxies"

**Homepage**: [https://doi.org/10.5281/zenodo.4196266](https://doi.org/10.5281/zenodo.4196266)

**Manual download instructions**:
Download from this [Zenodo
repository](https://zenodo.org/record/4573248#.YSEdzPfQ_mg) the
following three csv files and place them in `manual_dir/galaxy_zoo_decals`

- gz_decals_volunteers_1_and_2.csv
- gz_decals_volunteers_5.csv
- gz_decals_auto_posteriors.csv

Also download all four gz_decals_dr5_png_part\*.zip files and extract
them in `manual_dir/galaxy_zoo_decals`. You should end up with with
four folders structured like this:

    gz_decals_dr5_png_part*.zip/J*/J*.png
