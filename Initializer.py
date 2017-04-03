# Parses and uploads data to the DB, then calls the appropriate methods to generate the SNF

import FileParser
import argparse, sys

def main():
    f_parser = FileParser.FileParser()
    parser = argparse.ArgumentParser(description="Generate SNF using data provided in input files")
    #parser.add_argument('--create', action='create_true', required=False)

    # grab first file or error
    if (len(sys.argv) > 1):
        creator_file = sys.argv[1]
        f_parser.parseCreatorFile(creator_file)
    else:
        print("No input files specified")

    # add data from remaining files if more are given
    if(len(sys.argv) > 2):
        for i in range(len(sys.argv), 1):
            f_parser.parseNewDataType(sys.argv[i])

if __name__ == '__main__':
    main()