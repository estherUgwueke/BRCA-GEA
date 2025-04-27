#!/usr/bin/python3

# Import libraries
import os
import pandas as pd
from bioinfokit import analys, visuz

# Create an output directory to save results
output_dir = "../results/plots"
os.makedirs(output_dir, exist_ok=True)

# Set the variable for different comparisons
comparisons = [
    "tnbc_vs_normal",
    "nontnbc_vs_normal",
    "her2_vs_normal",
    "tnbc_vs_nontnbc",
    "tnbc_vs_her2",
    "nontnbc_vs_her2"
]

# Loop through each file and drop NAN values
for comp in comparisons:
    file_path = f"../results/deseq_analysis/{comp}_results.csv"
    df = pd.read_csv(file_path)
    print(f"Processing {file_path}...")
    df = df.dropna(subset=["log2FoldChange", "pvalue"])
    # Set volcano plotting for all comparisons
    visuz.GeneExpression.volcano(
        df=df,
        lfc='log2FoldChange',
        pv='pvalue',
        geneid='Gene_Name',
        genenames=tuple(df.sort_values("pvalue").head(10)['Gene_Name']),
        gstyle=2,
        lfc_thr=(0.5, -0.5),
        pv_thr=(0.05, 0.05),
        markerdot='*',
        dotsize=20,
        valpha=0.5,
        ar=45,
        color=('green', 'grey', 'red'),
        plotlegend=True,
        legendpos='upper right',
        legendanchor=(1.46, 1),
        axtickfontname='DejaVu Sans',
        axlabelfontname='DejaVu Sans',
        axlabelfontsize=10,
        axtickfontsize=10,
        r=300,
        sign_line=True,
        figname=os.path.join(output_dir, f"volcano_{comp}")
    )
print("Volcano plots created")

# Read the data and select significant genes by pvalue and log2FoldChange
significant_genes = {}
for comp in comparisons:
    file_path = f"../results/deseq_analysis/{comp}_results.csv"
    df = pd.read_csv(file_path)
    sig_df = df[(df['pvalue'] < 0.05) & (abs(df['log2FoldChange']) > 0.5)]
    significant_genes[comp] = set(sig_df['Gene_Name'].tolist())
    print(f"{comp}: {len(significant_genes[comp])} significant genes")

# Find genes significant in at least two comparisons
min_comparisons = 2
genes_to_keep = set()
for gene_set in significant_genes.values():
    for gene in gene_set:
        count = sum(1 for genes in significant_genes.values() if gene in genes)
        if count >= min_comparisons:
            genes_to_keep.add(gene)

print(
    f"Found {len(genes_to_keep)} genes significant in at least "
    f"{min_comparisons} comparisons"
)

# Load the data for normalized counts
norm_counts = pd.read_csv("../results/deseq_analysis/normalized_counts.csv")

# Set Gene_Name as index and select genes in two comparisons
normalized_counts = norm_counts.set_index("Gene_Name")
normalized_counts = normalized_counts.drop("Gene ID", axis=1)
sig_counts = normalized_counts[normalized_counts.index.isin(genes_to_keep)]

# Select top 50 genes to plot based on their variance
if len(sig_counts) > 50:
    gene_variance = sig_counts.var(axis=1)
    top_genes = gene_variance.sort_values(ascending=False).head(50).index
    sig_counts = sig_counts.loc[top_genes]

print(f"Creating heatmap with {len(sig_counts)} genes")

# Create general heatmap for significant genes for all comparisons
visuz.gene_exp.hmap(
        df=sig_counts,
        cmap="RdYlGn",
        zscore=0,
        dim=(6, 6),
        tickfont=(6, 4),
        figname=os.path.join(output_dir, "significant_genes_heatmap")
    )

# Create a separate heatmap for each comparison
for comp in comparisons:
    comp_genes = list(significant_genes[comp])
    if len(comp_genes) > 50:
        comp_df = pd.read_csv(f"../results/deseq_analysis/{comp}_results.csv")
        comp_df = comp_df[comp_df['Gene_Name'].isin(comp_genes)]
        comp_df = comp_df.sort_values('pvalue').head(50)
        comp_genes = comp_df['Gene_Name'].tolist()
    comp_counts = normalized_counts[normalized_counts.index.isin(comp_genes)]
    if len(comp_counts) > 0:
        visuz.gene_exp.hmap(
            df=comp_counts,
            cmap="RdYlGn",
            zscore=0,
            dim=(6, 6),
            tickfont=(6, 4),
            figname=os.path.join(output_dir, f"heatmap_{comp}")
        )
    else:
        print(f"No genes to plot for {comp}")

print("Heatmaps created for each comparison")
