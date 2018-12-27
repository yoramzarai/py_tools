#!/opt/local/bin/python3
'''Reads Python script descriptions.'''
import argparse
import os, re, subprocess
from termcolor import colored


# Command-line parsing information
def parse_in_args():
    ''' Defines input arguments '''
    # place description
    parser = argparse.ArgumentParser(description='Reads Python script descriptions.', add_help=False)

    # required arguments
    group = parser.add_argument_group('Required arguments')

    # optional arguments
    group_opt = parser.add_argument_group('Optional arguments')
    group_opt.add_argument('-d', dest='sdir', help='Search directory. Default is \'~/work/bin\'.', \
                           type=str, metavar='<search folder>', default='/Users/yoramzarai/work/bin')
    group_opt.add_argument('-e', dest='extn', help='Search only files with these extensions. Default is \'.py\'',\
                           type=str, nargs='+', metavar=('ext1', 'ext2'), default=['.py'])
    group_opt.add_argument('-u', help='Displays usage information as well.', action='store_true')
    group_opt.add_argument('-D', help='Enables debug prints.', action='store_true')

    group_opt.add_argument('-h', '--help', help='Displays usage information and exits.', action='help')

    return parser.parse_args()


def process_dir_files(args):
    '''Parses decsription in Python files in a specific folder'''
    tfind = re.compile('argparse.ArgumentParser\(')
    for fname in os.listdir(args.sdir):
        if os.path.isfile(os.path.join(args.sdir, fname)) and fname.endswith(tuple(args.extn)):
            if args.D: print('Processing {}...'.format(fname))
            with open(os.path.join(args.sdir, fname), 'rt') as file:
                for cnt, line in enumerate(file):
                    line = line.strip()
                    if tfind.search(line): # found a line with tfind text in it
                        if args.D: print('line {}: {}'.format(cnt, line))
                        #vals = re.split('\'', line)
                        vals = re.split(r"'", line)
                        #print( '{file}: {descr}'.format(file=fname, descr=vals[1]) )
                        print(colored(fname+':', 'red'), colored(vals[1], 'white'))
                        if args.u:
                            subprocess.run(fname + ' ' + '-h', shell=True)
                            print('')
                        break # found the description line, can move to next file



# Main function
# =============
def main():
    ''' Main body '''
    args = parse_in_args()  # parse, validate and return input arguments
    if args.D: print('Processing {ext} extension files from {dir} folder...'.format(ext=args.extn, dir=args.sdir))
    process_dir_files(args)


# ========================================================================================
if __name__ == "__main__":
    main()
