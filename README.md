# query_qtl_atlas
A python script for finding any QTLs near SNPs in the Sorghum QTL Atlas.

This script requires a local SQL database be generated using the Sorghum QTL Atlas data.

```bash
python query_qtl_atlas.py -h

usage: query_qtl_atlas.py [-h] --input INPUT --trait TRAIT --output OUTPUT [--database DATABASE]
                          [--distance DISTANCE] [--column COLUMN] [--substring SUBSTRING]

This script was designed to find any QTLs near SNPs in the Sorghum QTL Atlas
(https://aussorgm.org.au/sorghum-qtl-atlas/search/)

optional arguments:
  -h, --help            show this help message and exit
  --database DATABASE   The SorghumQtlAtlas database to use.
  --distance DISTANCE   The distance in kb from a SNP to search for QTL (default: 10).
  --column COLUMN       To search for specific substrings within columns, use the following index
                        numbers: { 0: index, 1: QTL Id, 2: Publication, 3: Population, 4: Trait
                        Description, 5: LG:Start-End (v3.0), 6: Genes Under QTL (v3.0), 7: Synteny, 8:
                        Chr, 9: Start, 10: Stop}. Ex. --column 2 (this will use the Publication column
                        to look for substrings). Multiple columns may also be designated: --column 2,8
  --substring SUBSTRING
                        Substring to search for within column (designated in --column). Ex. --column 4
                        --substring wax. Multiple substrings may be designated: --column 3,8
                        --substring bap,2

required arguments:
  --input INPUT         The name of the input file (CSV). File structure:
                        markerName,chromosome,position Or: markerName,chromosome,start,stop -- both
                        without a header
  --trait TRAIT         The trait table from which QTL are pulled. Trait categories include: leaf,
                        maturity, panicle, resistance_abiotic, resistance_biotic, stem_composition,
                        and stem_morphology
  --output OUTPUT       The output file to be created (CSV).
```

