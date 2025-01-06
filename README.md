# Expand gene names to include synonyms and compare between sets 

This python script is a simple utility designed to allow for accurate comparisons of gene sets found in file B against another set in file A. Often times genes have multiple names or synonyms which can make identifying them between experiments, assemblies or sharing data frustrating. NCBI offers a comprehensive list of organisms and their associated genes with their known synonyms in a special [gene_info](https://ftp.ncbi.nih.gov/gene/DATA/) file. Comparing genes against this list and manually comparing lists is a difficult process and can be automated. The following script generates a csv file as an output with every gene in file B as (column 1), it's known synonyms from the NCBI gene_info not already provided (column 2), and whether or not TRUE/FALSE it is present in set A (column 3). Gene synonyms are separated by the "|" character in column 2 of the output. This script allows the accurate comparison of gene sets taking into consideration potential synonyms of genes present to prevent over or miscounting of genes.    

_______________________________________________________
## Table of Contents
- [Installation](#installation)
- [Requirements](#requirements)
- [Usage](#usage)
- [Input File Formats](#input-file-formats)
- [Output Format](#output-format)
- [Example](#example)
- [License](#license)
- [Acknowledgments](#acknowledgments)

_______________________________________________________
## Installation
Clone this repository to your local machine:

```bash
git clone https://github.com/Fazizzz/Expand-and-compare-genes.git
cd Expand-and-compare-genes
```
________________________________________________________
## Requirements

* `Python 3.8+`
* `Text files contatining gene names (Include special characters found in gene names i.e "-")`
* `A gene_info file downloaded from: https://ftp.ncbi.nih.gov/gene/DATA/ (this file can be subset by organism to speed up matching)`

_______________________________________________________ 
## Usage

This script was written to be used with the provided human genes as part of the Hg38-human-only-2025-01-05-gene_info.txt file derived from the 01-05-2025 release of the NCBI gene_info file. The script should work with all organisms as long as they have genes and gene synonyms provided in the the gene_info file, but was not tested with other organisms.

Download gene_info file linux

```

wget https://ftp.ncbi.nih.gov/gene/DATA/gene_info.gz

gunzip gene_info.gz

```

Download gene_info file Mac

```

curl -O https://ftp.ncbi.nih.gov/gene/DATA/gene_info.gz

gunzip gene_info.gz

```
Optional: You can subset the gene_info file for your desired organism. This speeds up the process by making the file smaller and easier to parse. Here is how the provided file for the human genome was generated.

```
awk 'NR == 1 || $1 == "9606" {print $0}' gene_info > Hg38-human-only-gene_info.txt

``` 
Note: The python script needs the headers to be retained in the gene_info file to function correctly. I have included an abbreviated version of the NCBI gene_info file with just 3 key columns within this repo for use (#tax_id, Symbol and Synonyms). The larger file could not fit on Github. These are the 3 minimum columns required in the gene_info file to run the utility correctly.

```
# Generate 3 column file from previous step
cut -f 1,3,5 Hg38-human-only-2025-01-05-gene_info.txt > 3Key-columns-Hg38-human-only-2025-01-05-gene_info.txt
```

Run the script with:

```
python expand_and_compare_genes.py --file_a {file_a.txt} --file_b {file_b.txt} --output {output.txt} --gene_info {gene_info}.txt

```

The script takes four main arguments:

*	`-h or --help:` Show this help message and exit
*	`--file_a:` Path to file A with gene names.
*	`--file_b:` Path to file B with gene names to compare against file A..
*	`--output:` Path to the output file (CSV format). 
*	`--gene_info:` Path to the gene_info file (can be downloaded from: https://ftp.ncbi.nih.gov/gene/DATA/)
	Note: The gene names are all converted to lower case for comparisons to prevent the script from being case sensitive

________________________________________________________

## Input File Formats

# 1. Gene input files for comparison 

Example file a:
```
A1BG
A2M
A2MP1
NAT1
NAT2
NATP
SERPINA3
AADAC
AAMP

```
Example file b:
```
A1B
A2MD
A2MP
AAC1
AAC2
AACP
AACT
CES5A1
AAMP
ABO
ABR
ABCA4

```

# 2. Gene_info file format

Here are the first two lines of the gene_info file for reference

Example:
```
#tax_id	GeneID	Symbol	LocusTag	Synonyms	dbXrefs	chromosome	map_location	description	type_of_gene	Symbol_from_nomenclature_authority	Full_name_from_nomenclature_authority	Nomenclature_status	Other_designations	Modification_date	Feature_type
9606	1	A1BG	-	A1B|ABG|GAB|HYST2477	MIM:138670|HGNC:HGNC:5|Ensembl:ENSG00000121410|AllianceGenome:HGNC:5	19	19q13.43	alpha-1-B glycoprotein	protein-coding	A1BG	alpha-1-B glycoprotein	O	alpha-1B-glycoprotein|HEL-S-163pA|epididymis secretory sperm binding protein Li 163pA	20250104	-
9606	2	A2M	-	A2MD|CPAMD5|FWP007|S863-7	MIM:103950|HGNC:HGNC:7|Ensembl:ENSG00000175899|AllianceGenome:HGNC:7	12	12p13.31	alpha-2-macroglobulin	protein-coding	A2M	alpha-2-macroglobulin	O	alpha-2-macroglobulin|C3 and PZP-like alpha-2-macroglobulin domain-containing protein 5|alpha-2-M	20250104	-
...
```

_________________________________________________________

## Output Format

The script generates a CSV file with the following columns:

Gene: All of the gene names provided in file_b (not sorted in the same order and in lowercase)
Synonyms: All other synonyms found for the gene name provided in file_b found in the NCBI gene_info file
Present_in_A: True/False whether or not the gene or its synonym was found to be file_a 

Example Output:
```
Gene,Synonyms,Present_in_A
aamp,-,True
aac2,nat-2|nat2|pnat,True
aacp,natp|natp1,True
abo,a3galnt|a3galt1|gtb|nagat,False
abr,mdb,False
a2mp,a2mp1,True
a1b,a1bg|abg|gab|hyst2477,True
abca4,abc10|abcr|armd2|cord3|ffm|rmp|rp19|stgd|stgd1,False
aac1,mnat|nat-1|nat1|nati,True
aact,act|gig24|gig25|serpina3,True
a2md,a2m|cpamd5|fwp007|s863-7,True
ces5a1,aadac|dac,True
```
___________________________________________________________
## Example

Here's an example command for running the script:

```
python expand_and_compare_genes.py --file_a Test_file_a.txt --file_b Test_file_b.txt --output Test_output.txt --gene_info Hg38-human-only-2025-01-05-gene_info.txt

```
___________________________________________________________

## License

This project is licensed under the GPL-3.0 License - see the [LICENSE](https://www.gnu.org/licenses/gpl-3.0.en.html#license-text) file for details.


___________________________________________________________

## Acknowledgments

* **M.Faizan Khalid** - *Author and current maintainer of the code*

This script was developed by Muhammad Faizan Khalid for use with human genes. The script is intended to be a utility for use in bioinformatics analysis and analysis pipelines. Usage and implementation of this script is currently free, and this is not a commercial product. The author is not responsible for damages, upkeep and any issues with the script. It is provided as is. Please report any bugs or issues for future improvements which may be added into the repository. 
  
For citing this tool, please use Khalid M.Faizan or Khalid MF. You can follow my research using my [Google Scholar profile](https://scholar.google.com/citations?hl=en&user=qFZQ5wYAAAAJ&sortby=title&view_op=list_works&gmla=AL3_zigRWGX9g8Jc22idbBUMFuy7cVN_pEIyL6_DXSA-qWkJbcaONzhRNSmAwmQXKEm-3-WYGouZZC2pCE6zD9tZLxizbM7jQzzZMOgtkgsuL825u4lvSs9kwsccajhJbBg2Mrc37at_HCQ).

This project is made possible thanks to the open-source bioinformatics community for their resources and support.

