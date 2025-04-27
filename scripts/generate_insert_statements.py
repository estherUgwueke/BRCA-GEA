#!/usr/bin/python3

# Import libraries
import os
import pandas as pd

# Define functions to convert TSV/CSV to MySQL INSERT statements


def add_backticks(row, delimiter='\t'):
    """Wrap column names in backticks for MySQL."""
    values = row.split(delimiter)
    output = ["`{}`".format(value) for value in values]
    return ",".join(output)


def add_quotes(row, delimiter='\t'):
    """Wrap values in single quotes."""
    values = row.split(delimiter)
    output = ["'{}'".format(value) for value in values]
    return ",".join(output)


def csv_to_mysql(table, csv_file_path, delimiter='\t'):
    """This function converts a CSV/TSV file to MySQL INSERT statements."""
    with open(csv_file_path, 'r') as file:
        csv_array = file.readlines()
    header_str = add_backticks(csv_array[0].strip(), delimiter)
    sql_statement = ""
    # Generate INSERT statements for each row in the table
    for row in csv_array[1:]:
        row_str = add_quotes(row.strip(), delimiter)
        sql_statement += "INSERT INTO {}({}) VALUES({}); \n".format(table, header_str, row_str)
    return sql_statement


# Read the TSV file into a dataframe
file_path = "../data/E-GEOD-52194-experiment-design.tsv"
df = pd.read_csv(file_path, sep='\t')

# Remove rows for samples not analyzed
filtered_df = df[df['Analysed'] != 'No']

# Select and rename specific columns to be short and clear
selected_columns = {
    'Run': 'Sample_ID',
    'Sample Characteristic[clinical information]': 'Condition',
    'Sample Characteristic[disease]': 'Disease'
}
filtered_df = filtered_df[list(selected_columns.keys())].rename(columns=selected_columns)

# Save the filtered DataFrame to a new TSV file
output_file_path = "../data/E-GEOD-52194-experiment-design-filtered.tsv"
filtered_df.to_csv(output_file_path, sep='\t', index=False)
print(f"Filtered data is saved")

# Specify the paths to the data files
raw_counts_path = "../data/E-GEOD-52194-raw-counts.tsv"
metadata_path = "../data/E-GEOD-52194-experiment-design-filtered.tsv"

# Generate SQL statements for the raw data files (TSV)
raw_counts_sql = csv_to_mysql('raw_counts', raw_counts_path, delimiter='\t')
metadata_sql = csv_to_mysql('experiment_metadata', metadata_path, delimiter='\t')

# Create a directory to save results
output_dir = "../results/sql_outputs"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Directory created!")
else:
    print(f"Directory already exists.")

# Save the insert statements to SQL files
with open(f"{output_dir}/raw_counts.sql", "w") as raw_counts_file:
    raw_counts_file.write(raw_counts_sql)

with open(f"{output_dir}/metadata.sql", "w") as metadata_file:
    metadata_file.write(metadata_sql)

# Set the filename of CSV files from differential analysis results 
analysed_csv_files = {
    "tnbc_vs_normal_results": "tnbc_vs_normal_results.csv",
    "nontnbc_vs_normal_results": "nontnbc_vs_normal_results.csv",
    "her2_vs_normal_results": "her2_vs_normal_results.csv",
    "tnbc_vs_nontnbc_results": "tnbc_vs_nontnbc_results.csv",
    "tnbc_vs_her2_results": "tnbc_vs_her2_results.csv",
    "nontnbc_vs_her2_results": "nontnbc_vs_her2_results.csv",
    "normalized_counts": "normalized_counts.csv"
}

# Process each CSV file, generate INSERT statements and save to sql file
for table_name, file_name in analysed_csv_files.items():
    file_path = f"../results/deseq_analysis/{file_name}"
    sql_statements = csv_to_mysql(table_name, file_path, delimiter=',')
    output_file_path = f"{output_dir}/{table_name}.sql"
    with open(output_file_path, "w") as sql_file:
        sql_file.write(sql_statements)
        print(f"SQL statements for '{table_name}' saved to {output_dir}")

# Print statement to show process is finished
print("All SQL statements for TSV and CSV files is saved")
