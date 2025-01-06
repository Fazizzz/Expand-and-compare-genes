# expand_and_compare_genes.py
# Author: M.Faizan Khalid
# Date: [01-01-2025]
# Description: This script compares gene names in a text file B against text file A using a NCBI gene info file that includes synonyms.
# It expands gene sets to include all known synonyms for the genes to comprehensively check for all overlaps in genes between the two files.
# The output is a CSV file indicating whether each gene from file B (or its synonyms) is present in file A.
# The script will additionally add all synonyms separated by "|" available for a gene next to it if they are present in the NCBI gene_info file for that organism.

import argparse
import csv
import sys

def load_gene_info(gene_info_file):
    """
    Load gene info file and create a dictionary of gene names and their synonyms (case-insensitive).
    :param gene_info_file: Path to the gene info file (tab-delimited).
    :return: Dictionary where keys are gene names and values are sets of synonyms.
    """
    gene_dict = {}
    try:
        with open(gene_info_file, 'r') as f:
            reader = csv.DictReader(f, delimiter='\t')

            # Validate required columns
            required_columns = {'Symbol', 'Synonyms'}
            if not required_columns.issubset(set(reader.fieldnames)):
                raise ValueError(f"Gene info file must contain these columns: {required_columns}")

            for row in reader:
                gene_name = row['Symbol'].strip().lower()  # Normalize to lowercase
                synonyms = [syn.strip().lower() for syn in row['Synonyms'].split('|')] if row['Synonyms'] else []
                gene_dict[gene_name] = set(synonyms)  # Use a set to handle unique synonyms
    except Exception as e:
        print(f"Error reading gene info file: {e}")
        raise
    return gene_dict

def expand_gene_set_with_synonyms(gene_set, gene_dict):
    """
    Expand a set of gene names to include their synonyms.
    :param gene_set: Set of gene names from File A or B.
    :param gene_dict: Dictionary of gene names and their synonyms.
    :return: Expanded set of gene names including synonyms.
    """
    expanded_set = set()
    for gene in gene_set:
        expanded_set.add(gene)
        if gene in gene_dict:
            expanded_set.update(gene_dict[gene])  # Add synonyms to the set
    return expanded_set

def compare_files(gene_dict, file_a_genes, file_b_genes):
    """
    Compare genes in file B with genes and synonyms from file A.
    :param gene_dict: Dictionary of gene names and synonyms.
    :param file_a_genes: Set of gene names in File A.
    :param file_b_genes: Set of gene names in File B.
    :return: List of dictionaries for output, each containing:
             - Gene: The gene from file B.
             - Synonyms: Synonyms for the gene.
             - Present_in_A: Whether the gene or its synonyms are present in file A.
    """
    expanded_file_a = expand_gene_set_with_synonyms(file_a_genes, gene_dict)
    output = []

    for gene_b in file_b_genes:
        synonyms_b = set()  # Initialize synonyms set for gene_b
        present_in_a = False

        # Check if the gene_b matches a key or a synonym in the dictionary
        for gene_name, synonyms in gene_dict.items():
            if gene_b == gene_name or gene_b in synonyms:
                synonyms_b = {gene_name, *synonyms}  # Include the gene name and all its synonyms
                present_in_a = gene_name in expanded_file_a or any(syn in expanded_file_a for syn in synonyms)
                break

        # Exclude gene_b from its own synonyms
        synonyms_b.discard(gene_b)

        output.append({
            "Gene": gene_b,
            "Synonyms": '|'.join(sorted(synonyms_b)),  # Join synonyms with '|'
            "Present_in_A": str(present_in_a)
        })

    return output

def read_gene_file(file_path):
    """
    Read a file with gene names and return a set of genes (case-insensitive).
    :param file_path: Path to the file containing gene names.
    :return: Set of gene names.
    """
    try:
        with open(file_path, 'r') as f:
            return set(line.strip().lower() for line in f if line.strip())
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        raise

def write_output(output, output_file):
    """
    Write the comparison output to a CSV file.
    :param output: List of dictionaries containing the comparison results.
    :param output_file: Path to the output CSV file.
    """
    try:
        with open(output_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["Gene", "Synonyms", "Present_in_A"])
            writer.writeheader()
            writer.writerows(output)
    except Exception as e:
        print(f"Error writing to output file {output_file}: {e}")
        raise

def main():
    """
    Main function to parse arguments and run the script.
    """
    parser = argparse.ArgumentParser(description="Compare gene files with synonyms.")
    parser.add_argument('--gene_info', required=True, help="Path to the gene_info file, can be downloaded from: https://ftp.ncbi.nih.gov/gene/DATA/ (tab-delimited).")
    parser.add_argument('--file_a', required=True, help="Path to file A with gene names.")
    parser.add_argument('--file_b', required=True, help="Path to file B with gene names to compare against file A.")
    parser.add_argument('--output', required=True, help="Path to the output file (CSV format).")
    args = parser.parse_args()

    # Check if gene_info is provided
    if not args.gene_info:
        print("Warning: The gene info file is required for this script to run.")
        print("You can download the file from: https://ftp.ncbi.nih.gov/gene/DATA/")
        sys.exit(1)

    try:
        # Load gene info dictionary
        print("Loading gene info file...")
        gene_dict = load_gene_info(args.gene_info)

        # Read genes from file A and file B
        print("Reading file A and file B...")
        file_a_genes = read_gene_file(args.file_a)
        file_b_genes = read_gene_file(args.file_b)

        # Compare genes and generate output
        print("Comparing genes and generating output...")
        output = compare_files(gene_dict, file_a_genes, file_b_genes)

        # Write output to file
        print(f"Writing output to {args.output}...")
        write_output(output, args.output)
        print("Processing complete! Output written to:", args.output)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

