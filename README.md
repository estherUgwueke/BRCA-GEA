# BRCA-GEA: Identification of Differentially Expressed Genes in Breast Cancer Using RNA-Seq Analysis

## 🧬 Overview
BRCA-DESeq
A pipeline for RNA sequencing data analysis from breast cancer patients to determine which genes are differently expressed between tumor subtypes and normal breast tissue. It is designed as an easy-to-use computational analysis tool to help researchers identify patterns in breast cancer genetics more quickly, such as overexpressed or underexpressed genes, promote the discovery of possible therapeutic targets, and improve current understanding of breast cancer development.

##### Dependencies/Package versions: 
- Python v3.8
- Pydeseq2 v0.4.4
- PyMySql v1.1.1
- Bioinfokit v2.1.4

## 📦 Project Components
The components achieved in the project are as follows;
Components | Description | Scripts
------------- | ------------- | ---------------
`Database` | A SQL database implementation containing raw data and differential expression analysis results | generate_insert_statements.py; setup_database.py 
`Bash Script` | A pipeline for differential gene expression analysis | brca_deseq_pipeline.sh --> dependency scripts (get_data.sh; run_deseq_analysis.py) 
`Python Scripts` | Analyzes output from PyDESeq2 and generates visualizations like volcano plots and heatmaps | visualize_results.py

##### 🗂️ File Description
[PEP-8](https://peps.python.org/pep-0008/) style guide used.

Parameters | Description
------------ | -------------
`get_data.sh` | A bash script used to retrieve raw data for analysis from [EBI](https://www.ebi.ac.uk/gxa/experiments/E-GEOD-52194/Downloads). The RNA-Seq raw counts data contains 19 samples (3 tumor subtypes and normal) with 40,527 known genes after filtering out the unknowns.
`run_deseq_analysis.py` | A Python script for differential gene expression analysis. 
`generate_insert_statements.py` | Script for generating INSERT statements from raw and analysed results data. 	
`setup_database.py` | Script to create tables and insert data from the .sql files.
`visualize_results.py` | Python script to visualize the differential expression results using different plots.
`brca_deseq_pipeline.sh` | A bash script to run the pipeline from data acquisition, database population, and visualization of results. 	
    

## 🏁 Quick Start
⚡ Recommendation to run the pipeline:

Access to a database?: Run brca-deseq_pipeline.sh 

No database access? Run differential expression and visualization Python scripts only.

##### 📝 Usage:

1. Clone the repo
```python
# Clone the repository
git clone https://github.com/estherUgwueke/BRCA-GEA.git

# Change directory
cd BRCA-GEA/scripts
```   
2. Activate Python environment (Conda preferably)
```python
conda activate “env_name”
```

3. Run the pipeline using bash
```bash
bash brca-deseq_pipeline.sh 
```

## 👥 Users 
1. Graduate Students – Both for bioinformatics and non-bioinformatics graduate students to perform differential gene expression analysis.
2. Cancer Researchers – To analyze differential gene expression with BRCA data with a quick, reproducible framework.
3. Instructors/Faculty Members – To demonstrate to students/learners a reproducible pipeline for differential gene expression analysis using RNA-seq data. 


## 📄 License
This project is licensed under the [MIT License](https://raw.githubusercontent.com/estherUgwueke/BRCA-GEA/refs/heads/main/LICENSE?token=GHSAT0AAAAAAC6XSAVYLMOSPMXAO3PGPERI2ANS5SA).


## 🎓 Credit
Thanks to [Sanbomics](https://www.youtube.com/watch?v=wIvxFEMQVwg). Some parts of this code were adapted from the video tutorial on differential expression using pydeseq2. 
Other scripts for setting up the database and visualization plots were adapted from the examples on Bioinfokit ![PyPI version](https://badge.fury.io/py/bioinfokit.svg) and 
PyMySQL ![PyPI_version](https://badge.fury.io/py/PyMySQL.svg) webpages.


## 🔒 Privacy
The database used for the project is private and not accessible. Please kindly follow the script, then change the details as shown below for your database. 
```python
import pymysql

# To establish a connection to the database
connection = pymysql.connect(
    host="your_host",
    user="your_username",
    password="your_password",
    database="your_database",
    cursorclass=pymysql.cursors.DictCursor
)
```
