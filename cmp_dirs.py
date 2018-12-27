#!/opt/local/bin/python3
'''Compares the content in two directories'''
import argparse
import os
from termcolor import colored
import filecmp as fcmp

# Command-line parsing information
def parse_in_args():
    ''' Defines input arguments '''
    # place description
    parser = argparse.ArgumentParser(description='Compares the content of two directories.', add_help=False)

    # required arguments
    group = parser.add_argument_group('Required arguments')
    group.add_argument('-l', dest='dirl', help='First (left) directory', type=str, metavar='<dir 1>', required='True')
    group.add_argument('-r', dest='dirr', help='Second (right) directory', type=str, metavar='<dir 2>', required='True')

    # optional arguments
    group_opt = parser.add_argument_group('Optional arguments')

    group_opt.add_argument('-f', dest='chk_f', help='File list to compare. Default is all files.', type=str, nargs='+', \
                           metavar=('fn1', 'fn2'), default=list())
    group_opt.add_argument('-e', dest='ign_f', help='File list to ignore. Default is none.', type=str, nargs='+', \
                           metavar=('fn1', 'fn2'), default=list())
    group_opt.add_argument('-D', help='Enables debug prints.', action='store_true')
    group_opt.add_argument('-h', '--help', help='Displays usage information and exits.', action='help')

    return parser.parse_args(), parser.print_help


def print_base_cmp_dirs(var, name, colr):
    print(colored('\n\n{} {}', colr).format(len(var), name))
    for s in var: print(colored(s, colr), end=' ')

def print_cmp_dirs(args):
    cmp = fcmp.dircmp(args.dirl, args.dirr, args.ign_f)

    #print(cmp.report())
    # same files
    print_base_cmp_dirs(cmp.same_files, 'identical files:', 'green')

    # different version
    print_base_cmp_dirs(cmp.diff_files, 'with different versions:', 'red')
        
    # could not compare
    print_base_cmp_dirs(cmp.funny_files, 'could not compare:', 'white')

    # files and directories only in args.dirl
    print_base_cmp_dirs(cmp.left_only, 'are only in {}:'.format(args.dirl), 'magenta')

    # files and directories only in args.dirr
    print_base_cmp_dirs(cmp.right_only, 'are only in {}:'.format(args.dirr), 'cyan')
    print()
    

    
# Main function
# =============
def main():
    ''' Main body '''
    args, _ = parse_in_args()  # parse, validate and return input arguments
    if args.D: print('Comparing {} with {}...'.format(args.dirl, args.dirr))
    args.ign_f += ['.DS_Store'] 
    if args.chk_f:
        match, mismatch, errors = fcmp.cmpfiles(args.dirl, args.dirr, args.chk_f)
        if match: print_base_cmp_dirs(match, 'identical files:', 'green')
        if mismatch: print_base_cmp_dirs(mismatch, 'with different versions:', 'yellow')
        if errors: print_base_cmp_dirs(errors, 'missing files (in one or both directories):', 'red')
        print()
    else:
        print_cmp_dirs(args)
        
# =======================================================================================================================
if __name__ == "__main__":
    main()
else:
    print(__name__, 'has been imported.')

