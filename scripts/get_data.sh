#!/bin/bash

# Script to download RNA-Seq raw counts data

# Create a directory to save the raw data
data_path=../data
mkdir -p $data_path

# Download data from the website to the data folder
wget -O $data_path/E-GEOD-52194-experiment-design.tsv \
    https://www.ebi.ac.uk/gxa/experiments-content/E-GEOD-52194/resources/\
ExperimentDesignFile.RnaSeq/experiment-design

wget -O $data_path/E-GEOD-52194-raw-counts.tsv \
    https://www.ebi.ac.uk/gxa/experiments-content/E-GEOD-52194/resources/\
DifferentialSecondaryDataFiles.RnaSeq/raw-counts
