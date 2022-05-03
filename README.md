# query_qtl_atlas
Python scripts for finding any QTL near SNPs in the Sorghum QTL Atlas.

The primary query_qtl_atlas.py script requires a local SQLite database be generated using exported Sorghum QTL Atlas data (in Excel format). A helper script is provided to simplify database generation (see instructions below).

```bash
python query_qtl_atlas.py -h

usage: query_qtl_atlas.py [-h] --input INPUT --output OUTPUT
                          [--database DATABASE] [--distance DISTANCE]
                          [--qtl_length QTL_LENGTH] [--column COLUMN]
                          [--substring SUBSTRING]

This script was designed to find any QTLs near SNPs in the Sorghum QTL Atlas
(https://aussorgm.org.au/sorghum-qtl-atlas/search/)

optional arguments:
  -h, --help            show this help message and exit
  --database DATABASE   The SorghumQtlAtlas database to use.
  --distance DISTANCE   The maximum distance (in kb) from a SNP to search for
                        QTL (default: 10).
  --qtl_length QTL_LENGTH
                        The maximum length (in kb) of a QTL to include
                        (default: 5000).
  --column COLUMN       To search for specific substrings within columns, use
                        the following index numbers: { 0: index, 1: QTL Id, 2:
                        Publication, 3: Population, 4: Trait Description, 5:
                        LG:Start-End (v3.0), 6: Genes Under QTL (v3.0), 7:
                        Synteny, 8: Chr, 9: Start, 10: Stop}. Ex. --column 2
                        (this will use the Publication column to look for
                        substrings). Multiple columns may also be designated:
                        --column 2,8
  --substring SUBSTRING
                        Substring to search for within column (designated in
                        --column). Ex. --column 4 --substring wax. Multiple
                        substrings may be designated: --column 3,8 --substring
                        bap,2

required arguments:
  --input INPUT         The name of the input file (CSV). File structure:
                        markerName,chromosome,position Or:
                        markerName,chromosome,start,stop -- both with a header
  --output OUTPUT       The output file to be created (CSV).
```

Generate SQLite database from each SQA trait Excel table (see [Sorghum QTL Atlas](https://aussorgm.org.au/sorghum-qtl-atlas/search/?group=trait)):

```bash
python generate_atlas_database.py -h

usage: generate_atlas_database.py [-h] --input INPUT [--database DATABASE]

This script was designed to build a local instance of the Sorghum QTL Atlas
(https://aussorgm.org.au/sorghum-qtl-atlas/search/)

optional arguments:
  -h, --help           show this help message and exit
  --database DATABASE  The SorghumQtlAtlas database output name. (Default:
                       SorghumQtlAtlas.db)

required arguments:
  --input INPUT        The name of the input files (Excel) as a comma-
                       separated list. Ex. Atlas_leaf.xlsx,Atlas_maturity.xlsx
```
