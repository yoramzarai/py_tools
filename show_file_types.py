#!/opt/local/bin/python3
'''Displays the different file types in a directory'''
import argparse
import os
from termcolor import colored
from collections import defaultdict
from pprint import pprint
import re


# Command-line parsing information
def parse_in_args():
    ''' Defines input arguments '''
    # place description
    parser = argparse.ArgumentParser(description='Displays the different file types in a directory.', add_help=False)

    # required arguments
    group = parser.add_argument_group('Required arguments')

    # optional arguments
    group_opt = parser.add_argument_group('Optional arguments')
    group_opt.add_argument('-d', dest='sdir', help='Directory to analyze. Default is current directory.', \
                           type=str, metavar='<folder>', default='.')
    group_opt.add_argument('-v', help='Verbose (displays the files as well).', action='store_true')

    group_opt.add_argument('-D', help='Enables debug prints.', action='store_true')
    group_opt.add_argument('-h', '--help', help='Displays usage information and exits.', action='help')

    return parser.parse_args(), parser.print_help


def print_ftypes(ftypes, vrbs=False):
    '''Displays results'''
    print(colored('Found {} different extension types:', 'green').format(len(ftypes)))
    for k, v in ftypes.items():
        print(colored('{}: {} files','red').format(k,len(v)), end='')
        if vrbs: print(': {}'.format(', '.join(v)))
        print()

def analyze_file_types(sdir):
    '''Creates a dictionary with extensions as keys and number of files and files as values'''
    files = [f for f in os.listdir(sdir) if not os.path.isdir(os.path.join(sdir, f))]
    ftypes = {}
    for x in {os.path.splitext(f)[-1][1:] for f in files if os.path.splitext(f)[-1] != ''}:
        ftypes[x] = [f for f in files if f.endswith(x)]
    ftypes['<no ext>'] = [f for f in files if re.search(r'^[^.]+$',f)] # files with no extension
    return ftypes

# Main function
# =============
def main():
    ''' Main body '''
    args, _ = parse_in_args()  # parse, validate and return input arguments
    if args.D: print('Analyzing folder {}'.format(args.sdir))
    print_ftypes(analyze_file_types(args.sdir), args.v)
# =======================================================================================================================
if __name__ == "__main__":
    main()
else:
    print(__name__, 'has been imported.')

