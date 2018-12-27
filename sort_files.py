#!/opt/local/bin/python3
'''Sorts files based on size or modification time'''
import argparse
import os
from termcolor import colored
from pprint import pprint
from time import localtime, strftime

# Command-line parsing information
def parse_in_args():
    ''' Defines input arguments '''
    # place description
    parser = argparse.ArgumentParser(description='Sorts files based on size or modification time.', add_help=False)

    # required arguments
    group = parser.add_argument_group('Required arguments')

    # optional arguments
    group_opt = parser.add_argument_group('Optional arguments')
    group_opt.add_argument('-m', help='Selects sorting by file modification time. Default is sorting by file size.', \
                           action='store_true')
    group_opt.add_argument('-s', help='Sorts by smallest size [older file]. Default is by largest [newer].', action='store_true')
    group_opt.add_argument('-d', dest='sdir', help='Directory to sort. Default is current directory.', \
                           type=str, metavar='<folder>', default='.')
    group_opt.add_argument('-r', help='Enables recursive directory sorting.', action='store_true')
    group_opt.add_argument('-n', dest='num', help='Analyses only top <num_disp> files. Default is analyzing all files.', \
                           type=int, metavar='<num_disp>', default=None)
    group_opt.add_argument('-t', help='Displays only summary. Default is displaying all files.', \
                           action='store_true')

    group_opt.add_argument('-D', help='Enables debug prints.', action='store_true')
    group_opt.add_argument('-h', '--help', help='Displays usage information and exits.', action='help')

    return parser.parse_args(), parser.print_help

def analyze_stats_recursive(args):
    '''Saves size and modification time of all files in tree rooted by main directory'''
    info=[] # each element in the list is a tuple: (file name, size, modification time)
    for root, dirs, fnames in os.walk(args.sdir, topdown=False):
        for dn in [os.path.join(root, fn) for fn in fnames if os.path.isfile(os.path.join(root, fn))]:
            info.append((dn, os.path.getsize(dn), os.path.getmtime(dn)))
        info.append((root,sum(os.path.getsize(os.path.join(root, fname)) for fname in fnames), os.path.getmtime(root)))
    return info

def analyze_stats(args):
    '''Saves size and modification time of all files in the main directory'''
    info = [] # each element in the list is a tuple: (file name, size, modification time)
    for dn in [os.path.join(args.sdir, fn) for fn in os.listdir(args.sdir) if os.path.isfile(os.path.join(args.sdir, fn))]:
        info.append((dn, os.path.getsize(dn), os.path.getmtime(dn)))
    return info

# Main function
# =============
def main():
    ''' Main body '''
    args, _ = parse_in_args()  # parse, validate and return input arguments
    if args.D: print('Analyzing folder {}'.format(args.sdir))

    if args.r:
        info = analyze_stats_recursive(args)
    else:
        info = analyze_stats(args)

    l = len(info) if not args.num else args.num
    if args.D and not args.t: print('{} sorted files:'.format(l))

    if args.m: # sort by modification date
        info.sort(key=lambda x: x[2], reverse=not args.s)
        dmin = min(x[2] for x in info[:l])
        dmax = max(x[2] for x in info[:l])
        if not args.t:
            for c,(x,y,z) in enumerate(info[:l]):
                print('{indx}. {fname:<60}: {date}'.format(indx=c+1, fname=x,\
                                                           date=strftime('%b %d %Y, %H:%M:%S', localtime(z))))
        print(colored('Date range over {} files in {} is {dmin} : {dmax}', 'red').format(l, args.sdir,\
                                                              dmin=strftime('%b %d %Y, %H:%M:%S', localtime(dmin)),\
                                                              dmax=strftime('%b %d %Y, %H:%M:%S', localtime(dmax))))
    else: # sort by size
        info.sort(key=lambda x: x[1], reverse=not args.s)
        if not args.t:
            for c,(x,y,z) in enumerate(info[:l]):
                print('{indx}. {fname:<60}: {size:0.5f} [Mb]'.format(indx=c+1, fname=x, size=y/(1<<10)**2))
        print(colored('Total size over {} files in {} is {:0.5f} [Mb]','red').format(l, args.sdir,\
                                                                               sum(x[1] for x in info[:l])/(1<<10)**2))
# =======================================================================================================================
if __name__ == "__main__":
    main()
else:
    print(__name__, 'has been imported.')

