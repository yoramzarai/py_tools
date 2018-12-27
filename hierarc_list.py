#!/opt/local/bin/python3
'''Displays directory structure in hierarchical form'''
import argparse
import os
from termcolor import colored


# Command-line parsing information
def parse_in_args():
    ''' Defines input arguments '''
    # place description
    parser = argparse.ArgumentParser(description='Displays a directory structure in hierarchical form.', add_help=False)

    # required arguments
    group = parser.add_argument_group('Required arguments')

    # optional arguments
    group_opt = parser.add_argument_group('Optional arguments')
    group_opt.add_argument('-d', dest='sdir', help='Parent directory. Default is current directory.', \
                           type=str, metavar='<folder>', default='.')

    group_opt.add_argument('-D', help='Enables debug prints.', action='store_true')
    group_opt.add_argument('-h', '--help', help='Displays usage information and exits.', action='help')

    return parser.parse_args(), parser.print_help


def print_info(dir, level):
    num_f = len(os.listdir(dir))
    print('[L0]:', colored('{}','red').format(dir), '({} files)'.format(num_f)) if level==0 else \
        print(' ' * 3 * level, '[L{}]: '.format(level), colored('{}','red').format(os.path.basename(dir)), \
              ' ({} files)'.format(num_f), sep='')
    return num_f


def dirtree(dir, tnum_f=0, tnum_d=0, level=0):
    tnum_f += print_info(dir, level)
    for d in [os.path.join(dir, d) for d in os.listdir(dir) if os.path.isdir(os.path.join(dir, d))]:
        tnum_f, tnum_d = dirtree(d, tnum_f, tnum_d+1, level+1)
    return tnum_f, tnum_d

# Main function
# =============
def main():
    ''' Main body '''
    args, _ = parse_in_args()  # parse, validate and return input arguments
    if args.D: print('Analyzing folder {}'.format(args.sdir))
    tnum_f, tnum_d = dirtree(args.sdir)
    print('Total: {} sub-directories and {} files.'.format(tnum_d, tnum_f))
# =======================================================================================================================
if __name__ == "__main__":
    main()
else:
    print(__name__, 'has been imported.')

