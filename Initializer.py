# Parses and uploads data to the DB, then calls the appropriate methods to generate the SNF

import FileParser, Network
import argparse, sys, time

def main():
    t1 = time.time()
    # file parser
    f_parser = FileParser.FileParser()
    network = Network.Network()

    # command line argument parser
    parser = argparse.ArgumentParser(description="Generate SNF using data provided in input files")
    parser.add_argument('-d', '--delimiter', action='store', required=False, default=',', help='For tabs use "tab"')
    parser.add_argument('-f', '--file', action='store', required=True)
    parser.add_argument('-a', '--additional', action='append', required=False, help='Append additional data files')

    args = parser.parse_args()

    # change delimiter to tabs if specified
    if args.delimiter == 'tab':
        args.delimiter = '\t'

    # grab first file or error
    if args.file:
        f_parser.parseCreatorFile(args.file, args.delimiter)
    else:
        print("No input files specified")

    # add data from remaining files if more are given
    if args.additional:
        for data_type in args.additional:
            f_parser.parseNewDataType(data_type, args.delimiter)

    network.computeSimilarity()

    print("Delta: " + str((time.time() - t1) * 1000) + "ms")

if __name__ == '__main__':
    main()