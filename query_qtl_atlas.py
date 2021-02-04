#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
By J. Lucas Boatwright 

Find any QTLs near SNPs found to be significant in the Sorghum QTL Atlas
"""

import sys
import argparse
from sqlalchemy import create_engine

def parse_arguments():
    """Parse arguments passed to script"""
    parser = argparse.ArgumentParser(description="This script was " + 
            "designed to find any QTLs near SNPs in the Sorghum " + 
            "QTL Atlas (https://aussorgm.org.au/sorghum-qtl-atlas/search/)\n\n")

    requiredNamed = parser.add_argument_group('required arguments')

    requiredNamed.add_argument(
            "--input", 
            type=str, 
            required=True, 
            help="The name of the input file (CSV). " + 
            "File structure: markerName,chromosome,position",
            action="store")

    requiredNamed.add_argument(
            "--trait",
            type=str,
            required=True,
            help="The trait table from which QTL are pulled. " + 
            "Trait categories include: leaf, maturity, panicle, " + 
            "resistance_abiotic, resistance_biotic, stem_composition, " + 
            "and stem_morphology",
            action="store")

    requiredNamed.add_argument(
            "--output", 
            type=str, 
            required=True, 
            help="The output file to be created (CSV).", 
            action="store")

    parser.add_argument(
            "--database", 
            type=str, 
            required=False, 
            default="/zfs/tillers/Reference_Genomes/BTx623/v3.1.1/" + 
            "annotation/SorghumQtlAtlas.db",
            help="The SorghumQtlAtlas database to use.", 
            action="store")

    parser.add_argument(
            "--distance", 
            type=float, 
            required=False,
            default=10.0,
            help="The distance in kb from a SNP to search for QTL (default: 10).", 
            action="store")

    parser.add_argument(
            "--column",
            type=str,
            required=False,
            default="None",
            help="To search for specific substrings within columns, use " + 
            "the following index numbers: " + 
            "{ 0: index, 1: QTL Id, 2: Publication, 3: Population, 4: Trait Description, 5: LG:Start-End (v3.0), 6: Genes Under QTL (v3.0), 7: Synteny, 8: Chr, 9: Start, 10: Stop}. Ex. --column 2 (this will use the Publication column to look for substrings). Multiple columns may also be designated: --column 2,8",
            action="store"
            )

    parser.add_argument(
            "--substring",
            type=str,
            required=False,
            default="None",
            help="Substring to search for within column (designated in " + 
            "--column). Ex. --column 4 --substring wax. Multiple substrings " + 
            "may be designated: --column 3,8 --substring bap,2",
            action="store"
            )

    return parser.parse_args()


def file_to_list(filename):
    with open(filename) as f:
        output = f.read().splitlines()
    return output


def build_filter(trait, engine, column, substring):
    if "," in column:
        column_list = column.split(',')
    else:
        column_list = [column]
    if "," in substring:
        substring_list = substring.split(',')
    else:
        substring_list = [substring]
    if len(column_list) != len(substring_list):
        sys.stderr.write("Different numbers in Column and Substring variables\n")
        sys.exit(1)
    column_dict = {}
    for i in engine.execute(f"PRAGMA table_info('{trait}')").fetchall():
        # column name [4][1]
        column_dict[str(i[0])] = i[1]
    additional_filter = ""
    for column_value, substring_value in zip(column_list, substring_list):
        column_name = column_dict[column_value]
        additional_filter = f"{additional_filter} \"{column_name}\" LIKE '%{substring_value}%' AND" 
    return additional_filter


def find_overlapping_features(input_file, output, 
        trait, distance, database, column, substring):
    engine = create_engine("sqlite:///" + database)
    additional_filter = ""
    if ((column.lower() != "none") and (substring.lower() != "none")):
        additional_filter = build_filter(trait, engine, column, substring) 
    with open(output, 'w') as f:
        f.write("Marker_Name,MyChr,MyPosition,QtlID,QtlSpan," + 
                "Trait_Description,Publication,Population," + 
                "Chrom:Start-End_v3.0," + 
                "Genes_Under_QTL_v3.0,Synteny,QtlChr,QtlStart,QtlStop\n")
        for line in input_file:
            split_line = line.split(",")
            chrom = int(split_line[1])
            position = int(split_line[2])
            results = engine.execute(f"SELECT * FROM {trait} WHERE {additional_filter} Chr == {chrom} AND {position} BETWEEN (Start - {distance}) AND (Stop + {distance})").fetchall()
            for result in results:
                writeable_results = [str(i) for i in list(result[1:])]
                url_link = "( https://aussorgm.org.au/" +\
                    "sorghum-qtl-atlas/study-details/?study_name=" +\
                    "%20".join(writeable_results[1].replace(",","%2C")
                            .replace("&","%26")
                            .split()) + " )"
                span = [str(int(writeable_results[9]) - int(writeable_results[8]))]
                writeable_results[1] = writeable_results[1] + url_link
                f.write(",".join(split_line + 
                    [writeable_results[0]] + span 
                    + [writeable_results[3]] + writeable_results[1:3] + writeable_results[4:] ) + "\n")


def main(args):
    """Main exection function"""
    input_file = file_to_list(args.input)
    distance   = int(args.distance * 1000)
    trait = (args.trait).lower()
    if args.column == "None" and args.substring != "None":
        sys.stderr.write("Column parameter required with substring.\n")
        sys.exit(1)
    elif args.column != "None" and args.substring == "None":
        sys.stderr.write("Substring parameter required with column.\n")
        sys.exit(1)

    find_overlapping_features(input_file,
            args.output,
            trait,
            distance,
            args.database,
            args.column,
            args.substring)


if __name__ == "__main__":
    args = parse_arguments()
    main(args)

