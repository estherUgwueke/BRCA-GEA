#!/bin/bash

# Pipeline to run differential sequencing analyis for breast cancer types, 
# add data into a database and also visualize results.

echo "Pipeline execution started"

# Get the data required for the analysis and direct outputs
echo "---Getting data---" > output.log
bash get_data.sh >> output.log 2>&1

# Perform differential gene expression analysis using python
echo "---Performing differential analysis---" >> output.log
python run_deseq_analysis.py >> output.log 2>&1

# Generate insert statements from data for the database
echo "---Generating INSERT statements---" >> output.log
python generate_insert_statements.py >> output.log 2>&1

# Setup and populate the database
echo "---Setting up the database---" >> output.log
python setup_database.py >> output.log 2>&1

# Visualize the results of differential seq analysis with plots
echo "---Generating visualization plots---" >> output.log
python visualize_results.py >> output.log 2>&1

echo "Pipeline execution finished"
