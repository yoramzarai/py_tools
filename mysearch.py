#!/opt/local/bin/python3
''' Searches strings or file names '''
import argparse
import os


# Command-line parsing information
def parse_in_args():
    ''' Defines input arguments '''
    # place description
    parser = argparse.ArgumentParser(description='Search a string or a file name in folders.', add_help=False)

    # required arguments
    group = parser.add_argument_group('Required arguments')

    # optional arguments
    group_opt = parser.add_argument_group('Optional arguments')
    group_opt.add_argument('-s', dest='strg', help='A string to search for.', type=str, metavar='<str>')
    group_opt.add_argument('-f', dest='fnm', help='(Alternatively) A file name to search for.', type=str,\
                           metavar='<fname>')
    group_opt.add_argument('-d', dest='sdir', help='Search directory. Default is current directory.', \
                           type=str, metavar='<search folder>', default='.')
    group_opt.add_argument('-r', help='Enables recursive search.', action='store_true')
    group_opt.add_argument('-e', dest='excl_f', help='Excluded file list.', type=str, nargs='+', \
                           metavar=('fn1', 'fn2'), default=list())
    group_opt.add_argument('-ed', dest='excl_d', help='Excluded folder list (relative to search folder).', type=str, nargs='+', \
                           metavar=('dn1', 'dn2'), default=list())
    group_opt.add_argument('-x', dest='extn', help='Use only files with these extensions. Default is all files. E.g. -x .m .c',\
                           type=str, nargs='+', metavar=('ext1', 'ext2'), default=[''])
    group_opt.add_argument('-D', help='Enables debug prints.', action='store_true')

    group_opt.add_argument('-h', '--help', help='Displays usage information and exits.', action='help')

    return parser.parse_args()


# search a string in a file
def parse_file(fname, strg):
    '''Looks for a given string in a file'''
    found_lines = list()
    with open(fname, 'rt') as file:
        #for lcnt, line in enumerate( file ):
        for line in file:
            line = line.strip()
            if strg in line:
                #print('L{}: {}'.format( lcnt, line ) )
                found_lines.append(line)
    return found_lines

# read folder and process files
def process_dir(dname, args):
    '''Reads folder content and parse using input arguments'''
    for fname in os.listdir(dname):
        dfname = os.path.join(dname, fname) # full path
        if os.path.isdir(dfname):
            if dfname in args.excl_d:
                if args.D: print('{} in excluded list, skipping it...'.format(dfname))
                continue
            if args.r:
                process_dir(dfname, args)
            continue
        if fname in args.excl_f:
            if args.D: print('{} in excluded list, skipping it...'.format(fname))
            continue
        if fname.endswith(tuple(args.extn)):
            if args.D: print('Searching file: ', dfname)
            if args.strg:
                found_lines = parse_file(dfname, args.strg)
                if found_lines:
                    print('Found {num} lines in file {fn}:'.format(num=len(found_lines), fn=dfname), end='\n\t')
                    print(*found_lines, sep='\n\t')
            elif fname == args.fnm:  # search for file name
                print('Found {file} in {folder}'.format(file=fname, folder=dname))

# Main function
# =============
def main():
    ''' Main body '''
    args = parse_in_args()  # parse, validate and return input arguments
    args.excl_f += ['.DS_Store'] # for MAC
    if args.strg or args.fnm:
        print('Searching folder {} for '.format(args.sdir), end='')
        print('the string \'{}\'...'.format(args.strg)) if(args.strg) else print('the file \'{}\'...'.format(args.fnm))
        process_dir(args.sdir, args)
    else:
        print('Nothing to do (see usage). Exiting...')


# ========================================================================================
if __name__ == "__main__":
    main()
