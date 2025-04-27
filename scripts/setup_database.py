#!/usr/bin/python3

import pymysql

# Establish a connection to the database
connection = pymysql.connect(
    host="localhost",
    user="eugwueke",
    database="eugwueke",
    cursorclass=pymysql.cursors.DictCursor,
    unix_socket="/run/mysqld/mysqld.sock"
)

# Set path to the input sql files
input_dir = "../results/sql_outputs"

# Define the paths to the .sql files
raw_counts_sql_path = f"{input_dir}/raw_counts.sql"
metadata_sql_path = f"{input_dir}/metadata.sql"
normalized_counts_sql_path = f"{input_dir}/normalized_counts.sql"
tnbc_vs_normal_sql_path = f"{input_dir}/tnbc_vs_normal_results.sql"
nontnbc_vs_normal_sql_path = f"{input_dir}/nontnbc_vs_normal_results.sql"
her2_vs_normal_sql_path = f"{input_dir}/her2_vs_normal_results.sql"
tnbc_vs_nontnbc_sql_path = f"{input_dir}/tnbc_vs_nontnbc_results.sql"
tnbc_vs_her2_sql_path = f"{input_dir}/tnbc_vs_her2_results.sql"
nontnbc_vs_her2_sql_path = f"{input_dir}/nontnbc_vs_her2_results.sql"

# Drop any existing tables and create new tables
with connection:
    with connection.cursor() as cursor:
        # Dropping any existing tables with the same name
        cursor.execute("DROP TABLE IF EXISTS raw_counts;")
        cursor.execute("DROP TABLE IF EXISTS experiment_metadata;")
        cursor.execute("DROP TABLE IF EXISTS normalized_counts;")
        cursor.execute("DROP TABLE IF EXISTS tnbc_vs_normal_results;")
        cursor.execute("DROP TABLE IF EXISTS nontnbc_vs_normal_results;")
        cursor.execute("DROP TABLE IF EXISTS her2_vs_normal_results;")
        cursor.execute("DROP TABLE IF EXISTS tnbc_vs_nontnbc_results;")
        cursor.execute("DROP TABLE IF EXISTS tnbc_vs_her2_results;")
        cursor.execute("DROP TABLE IF EXISTS nontnbc_vs_her2_results;")
        print("Existing tables dropped successfully.")

        # Create the raw_counts table
        create_table_query_raw_counts = """
        CREATE TABLE raw_counts (
            `Gene ID` VARCHAR(30),
            `Gene Name` VARCHAR(30),
            `SRR1027182` INTEGER,
            `SRR1027186` INTEGER,
            `SRR1027185` INTEGER,
            `SRR1027177` INTEGER,
            `SRR1027181` INTEGER,
            `SRR1027175` INTEGER,
            `SRR1027180` INTEGER,
            `SRR1027184` INTEGER,
            `SRR1027190` INTEGER,
            `SRR1027188` INTEGER,
            `SRR1027176` INTEGER,
            `SRR1027189` INTEGER,
            `SRR1027174` INTEGER,
            `SRR1027179` INTEGER,
            `SRR1027178` INTEGER,
            `SRR1027187` INTEGER,
            `SRR1027171` INTEGER,
            `SRR1027173` INTEGER,
            `SRR1027183` INTEGER
        );
        """
        cursor.execute(create_table_query_raw_counts)

        # Create the experiment_metadata table
        create_table_query_experiment_metadata = """
        CREATE TABLE experiment_metadata (
            `Sample_ID` VARCHAR(10),
            `Condition` VARCHAR(50),
            `Disease` VARCHAR(50)
        );
        """
        cursor.execute(create_table_query_experiment_metadata)

        # Create the normalized_counts table
        create_table_query_normalized_counts = """
        CREATE TABLE normalized_counts (
            `Gene ID` VARCHAR(30),
            `SRR1027171` INTEGER,
            `SRR1027173` INTEGER,
            `SRR1027174` INTEGER,
            `SRR1027175` INTEGER,
            `SRR1027176` INTEGER,
            `SRR1027177` INTEGER,
            `SRR1027178` INTEGER,
            `SRR1027179` INTEGER,
            `SRR1027180` INTEGER,
            `SRR1027181` INTEGER,
            `SRR1027182` INTEGER,
            `SRR1027183` INTEGER,
            `SRR1027184` INTEGER,
            `SRR1027185` INTEGER,
            `SRR1027186` INTEGER,
            `SRR1027187` INTEGER,
            `SRR1027188` INTEGER,
            `SRR1027189` INTEGER,
            `SRR1027190` INTEGER,
            `Gene_Name` VARCHAR(50)
        );
        """
        cursor.execute(create_table_query_normalized_counts)

        # Create tables for comparison results
        create_table_query_comparison = """
        CREATE TABLE {} (
            `Gene ID` VARCHAR(30),
            `baseMean` FLOAT NULL,
            `log2FoldChange` FLOAT NULL,
            `lfcSE` FLOAT NULL,
            `stat` FLOAT NULL,
            `pvalue` FLOAT NULL,
            `padj` FLOAT NULL,
            `Gene_Name` VARCHAR(50)
        );
        """
        comparison_tables = [
            "tnbc_vs_normal_results",
            "nontnbc_vs_normal_results",
            "her2_vs_normal_results",
            "tnbc_vs_nontnbc_results",
            "tnbc_vs_her2_results",
            "nontnbc_vs_her2_results"
        ]
        for table_name in comparison_tables:
            cursor.execute(create_table_query_comparison.format(table_name))

        print("Tables created successfully.")

        # Insert data from the sql files to the database
        sql_files = {
            "raw_counts": raw_counts_sql_path,
            "experiment_metadata": metadata_sql_path,
            "normalized_counts": normalized_counts_sql_path,
            "tnbc_vs_normal_results": tnbc_vs_normal_sql_path,
            "nontnbc_vs_normal_results": nontnbc_vs_normal_sql_path,
            "her2_vs_normal_results": her2_vs_normal_sql_path,
            "tnbc_vs_nontnbc_results": tnbc_vs_nontnbc_sql_path,
            "tnbc_vs_her2_results": tnbc_vs_her2_sql_path,
            "nontnbc_vs_her2_results": nontnbc_vs_her2_sql_path
        }

        for table_name, sql_file_path in sql_files.items():
            with open(sql_file_path, 'r') as sql_file:
                sql_statements = sql_file.read()
                sql_statements = sql_statements.replace("''", "NULL")
                for statement in sql_statements.split(";"):
                    if statement.strip():
                        cursor.execute(statement)
            print(f"Data inserted into table '{table_name}' successfully.")

    # Commit the changes and close connection
    connection.commit()
    print("All changes committed successfully.")
