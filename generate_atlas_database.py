#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
By J. Lucas Boatwright

Generate an SQL database from the Sorghum QTL Atlas Excel files
"""

import argparse
import pandas as pd
from sqlalchemy import create_engine


def parse_arguments():
    """Parse arguments passed to script"""
    parser = argparse.ArgumentParser(description="This script was " +
                                                 "designed to build a local instance of the Sorghum " +
                                                 "QTL Atlas (https://aussorgm.org.au/sorghum-qtl-atlas/search/)\n\n")

    required_named = parser.add_argument_group('required arguments')

    required_named.add_argument(
        "--input",
        type=str,
        required=True,
        help="The name of the input files (Excel) as a comma-separated list. " +
             "Ex. Atlas_leaf.xlsx,Atlas_maturity.xlsx",
        action="store")

    parser.add_argument(
        "--database",
        type=str,
        required=False,
        default="SorghumQtlAtlas.db",
        help="The SorghumQtlAtlas database output name. (Default: SorghumQtlAtlas.db)",
        action="store")

    return parser.parse_args()


def read_excel_files(excels):
    """Take comma-separated list of Excel files, return combined dataframe"""
    excel_df = pd.DataFrame()
    for x, excel in enumerate(excels.split(',')):
        if x == 0:
            excel_df = pd.read_excel(excel, skiprows=1)
        else:
            excel_df = pd.concat([excel_df, pd.read_excel(excel, skiprows=1)], axis=0)
    return excel_df


def add_positional_columns(df):
    """Split 'LG:Start-End (v3.0)' into Chr|Start|Stop columns"""
    # Example, 1:2246707-10368475
    df[["Chr", "Start", "Stop"]] = df["LG:Start-End (v3.0)"].str.split(pat=r'\D', expand=True)
    return df


def write_dataframe_to_database(df, database):
    """Write complete dataframe to SQLite database"""
    engine = create_engine("sqlite:///" + database)
    df.to_sql("atlas", engine)


if __name__ == "__main__":
    args = parse_arguments()
    qtl_df = read_excel_files(args.input)
    qtl_df = add_positional_columns(qtl_df)
    write_dataframe_to_database(qtl_df, args.database)
