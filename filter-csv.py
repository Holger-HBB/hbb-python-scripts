#
#   HBB's Python Script Collection
#
#   Filter CSV using another CSV
#
#   Copyright (C) 2020  Holger Burghardt
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published
#   by the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#
#   Based upon https://repl.it/@rplrpl/Filter-Large-CSV created 2019-01-08 by rplrpl
#
#   Requires Pandas 0.23.4 or later
#
#   Version 0.1

"""
Script to filter a CSV file using values from a second CSV file.
Usage: filter-csv.py -i INFILE [-c COLUMN] -l FILTERLIST [-f FILTERCOLUMN] [-m MODE] [-o OUTFILE]
"""

import pandas
import datetime
import sys
from optparse import OptionParser


# Parsing option

def get_options(parser):
    """ Define command line options."""
    parser.add_option("-i", "--infile", dest="infile", default=None,
                      help="Input file - the CSV file on which the filter will be applied.")
    parser.add_option("-c", "--column", dest="column", default=None,
                      help="The column of the input file on which the filter will be applied. Default is the first column.")
    parser.add_option("-l", "--list", dest="filterlist", default=None,
                      help="Filter list - the CSV file containing the values of the filter.")
    parser.add_option("-f", "--filter", dest="filtercolumn", default=None,
                      help="The column of the filter list file containing the values of the filter. Default is the first column.")
    parser.add_option("-m", "--mode", dest="mode", type="int", default=0,
                      help="Mode - what data will be removed - 0 or 1: 0 if only the rows corresponding to the filter values with be retained; 1 if all rows corresponding to the filter values with be removed. Default is 0")
    parser.add_option("-o", "--outfile", dest="outfile", default=None,
                      help="Output file - the CSV file to which the filtered data will be written. By default the input file with ""out_"" prefix")
    options, args = parser.parse_args()

    if not options.infile:
        sys.exit("Input file not specified, see --help")

    if not options.column:
        sys.exit("Filter list not specified, see --help")

    if not options.filterlist:
        sys.exit("Input file not specified, see --help")

    if not options.filtercolumn:
        sys.exit("Filter list not specified, see --help")

    if not options.outfile:
        options.outfile = 'out_' + options.infile

    return options.infile, options.column, options.filterlist, options.filtercolumn, options.mode, options.outfile

parser = OptionParser()
infile, column, filterlist, filtercolumn, mode, outfile = get_options(parser)

# Read input CSV file

df = pandas.read_csv(infile)

# Column to filter the input CSV file has been an option, setting to first column if empty

if not column:
    col = df.columns[0]
else:
    col = column

# Read input CSV file with filter values

df2 = pandas.read_csv(filterlist)

# Column to filter the input CSV filter file has been an option, setting to first column if empty

if not column:
    filtercolumn = df2.columns[0]
    
# Turning CSV filter dataset column into a list

filter_list = df2[filtercolumn].values.tolist()

# Print info on original file.

print('There are ' + str(len(df)) + ' rows in the original CSV file at ' + infile + ' before deleting the unwanted rows.')

print()

# Doing the actual job

t1 = datetime.datetime.now()

if mode == 1:
    df = df[~df[col].isin(filter_list)]
else:
    df = df[df[col].isin(filter_list)]

t2 = datetime.datetime.now()

tm = round((t2 - t1).total_seconds(), 2)

# Reporting on the work.

print('It took ' + str(tm) + ' seconds to delete the unwanted rows.')

print()

# Exporting to CSV outfile and final report.

df.to_csv(outfile, index=False)

print(str(len(df)) + ' rows have been written to' + outfile '.')