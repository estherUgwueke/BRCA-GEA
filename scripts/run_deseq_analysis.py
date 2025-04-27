#!/usr/bin/python3

# Import libraries
import os
import pydeseq2
from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats
from pydeseq2.default_inference import DefaultInference
import pandas as pd

# Define input and output paths
input_dir = "../data"
output_dir = "../results/deseq_analysis"

# Create output directory
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Directory created!")
else:
    print(f"Directory already exists.")

# Read the raw counts data
raw_counts_path = os.path.join(input_dir, "E-GEOD-52194-raw-counts.tsv")
raw_counts = pd.read_csv(raw_counts_path, sep="\t")

# Find the number of NaN values in each column
nan_count_by_column = raw_counts.isna().sum()
print(nan_count_by_column)

# Set gene id column as index
raw_counts = raw_counts.set_index("Gene ID")

# Filter out rows with zero values
raw_counts_filter = raw_counts[raw_counts.sum(axis=1) > 0]

# Remove all rows where 'Gene Name' is NaN
raw_counts_final = raw_counts_filter[raw_counts_filter["Gene Name"].notna()]

# Save gene names to a variable and drop it
gene_names = raw_counts_final["Gene Name"]
counts_numeric = raw_counts_final.drop("Gene Name", axis=1)

# Transpose the raw count data rows for analysis
transposed_counts = counts_numeric.T

# Load the metadata file and filter out unanalysed samples
metadata_path = os.path.join(input_dir, "E-GEOD-52194-experiment-design.tsv")
metadata = pd.read_csv(metadata_path, sep="\t")
metadata_filter = metadata[metadata["Analysed"] != "No"]

# Select sample IDs and condition columns only for analysis
metadata_final = metadata_filter[["Run", "Factor Value[clinical information]"]]

# Rename the columns for analysis
metadata_final = metadata_final.rename(columns={
    "Run": "Sample_ID",
    "Factor Value[clinical information]": "Condition"
})

# Set the sample_id as the index to match the transposed count data
metadata_final = metadata_final.set_index("Sample_ID")

# Sort both datasets by the sample IDs
metadata_sorted = metadata_final.sort_index()
counts_sorted = transposed_counts.sort_index()

############### Differential Analysis #######################################

# Run the differential expression analysis
inference = DefaultInference(n_cpus=8)
dds = DeseqDataSet(
        counts=counts_sorted,
        metadata=metadata_sorted,
        design_factors="Condition",
        refit_cooks=True,
        inference=inference
    )

dds.deseq2()
print(dds)
print(dds.varm["dispersions"])
print(dds.varm["LFC"])

# Compare different conditions
# Compare triple-negative breast cancer vs normal
tnbc_vs_normal = DeseqStats(
        dds,
        inference=inference,
        contrast=[
            "Condition",
            "triple-negative breast cancer",
            "normal"
        ]
)
tnbc_vs_normal.summary()

# Compare non-triple-negative breast cancer vs normal
nontnbc_vs_normal = DeseqStats(
        dds,
        inference=inference,
        contrast=[
            "Condition",
            "non-triple-negative breast cancer",
            "normal"
        ]
)
nontnbc_vs_normal.summary()

# Compare HER2 Positive vs normal
her2_vs_normal = DeseqStats(
        dds,
        inference=inference,
        contrast=[
            "Condition",
            "HER2 Positive Breast Carcinoma",
            "normal"
        ]
)
her2_vs_normal.summary()

# Compare triple-negative vs non-triple-negative
tnbc_vs_nontnbc = DeseqStats(
        dds,
        inference=inference,
        contrast=[
            "Condition",
            "triple-negative breast cancer",
            "non-triple-negative breast cancer"
        ]
)
tnbc_vs_nontnbc.summary()

# Compare triple-negative vs HER2 Positive
tnbc_vs_her2 = DeseqStats(
        dds,
        inference=inference,
        contrast=[
            "Condition",
            "triple-negative breast cancer",
            "HER2 Positive Breast Carcinoma"
        ]
)
tnbc_vs_her2.summary()

# Compare non-triple-negative vs HER2 Positive
nontnbc_vs_her2 = DeseqStats(
        dds,
        inference=inference,
        contrast=[
            "Condition",
            "non-triple-negative breast cancer",
            "HER2 Positive Breast Carcinoma"
        ]
)
nontnbc_vs_her2.summary()

# Extract results dataframes from each comparison
tnbc_vs_normal_df = tnbc_vs_normal.results_df
nontnbc_vs_normal_df = nontnbc_vs_normal.results_df
her2_vs_normal_df = her2_vs_normal.results_df
tnbc_vs_nontnbc_df = tnbc_vs_nontnbc.results_df
tnbc_vs_her2_df = tnbc_vs_her2.results_df
nontnbc_vs_her2_df = nontnbc_vs_her2.results_df


# Create a mapping dictionary from Gene ID to Gene Name
gene_name_dict = gene_names.to_dict()

# Create a function to add gene names to results


def add_gene_names(results_df, map_gene_name):
    results_copy = results_df.copy()
    results_copy['Gene_Name'] = results_copy.index.map(map_gene_name)
    return results_copy


# Add gene names to all the results dataframes
tnbc_vs_normal = add_gene_names(tnbc_vs_normal_df, gene_name_dict)
nontnbc_vs_normal = add_gene_names(nontnbc_vs_normal_df, gene_name_dict)
her2_vs_normal = add_gene_names(her2_vs_normal_df, gene_name_dict)
tnbc_vs_nontnbc = add_gene_names(tnbc_vs_nontnbc_df, gene_name_dict)
tnbc_vs_her2 = add_gene_names(tnbc_vs_her2_df, gene_name_dict)
nontnbc_vs_her2 = add_gene_names(nontnbc_vs_her2_df, gene_name_dict)

# Save the results to a csv file
tnbc_vs_normal.to_csv(os.path.join(output_dir, "tnbc_vs_normal_results.csv"))
nontnbc_vs_normal.to_csv(os.path.join(output_dir, "nontnbc_vs_normal_results.csv"))
her2_vs_normal.to_csv(os.path.join(output_dir, "her2_vs_normal_results.csv"))
tnbc_vs_nontnbc.to_csv(os.path.join(output_dir, "tnbc_vs_nontnbc_results.csv"))
tnbc_vs_her2.to_csv(os.path.join(output_dir, "tnbc_vs_her2_results.csv"))
nontnbc_vs_her2.to_csv(os.path.join(output_dir, "nontnbc_vs_her2_results.csv"))

# Access the normalized counts from the analysis layers
normalized_counts = dds.layers["normed_counts"]

# Create a dataFrame with the normalized counts
normalized_counts_df = pd.DataFrame(
        normalized_counts,
        index=dds.obs.index,
        columns=dds.var.index
)

# Transpose the data to get the gene as rows
normalized_counts_t = normalized_counts_df.T

# Add gene names to the dataframe and save to a file
normalized_counts_t['Gene_Name'] = gene_names
normalized_counts_t.to_csv(os.path.join(output_dir, "normalized_counts.csv"))

print("All processed successfully")
