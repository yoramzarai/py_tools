#!/opt/local/bin/python3
'''Executes basic math expressions.'''
import argparse
import re,math

# Command-line parsing information
def parse_in_args():
    ''' Defines input arguments '''
    # place description
    parser = argparse.ArgumentParser(description='Executes basic math expressions.', add_help=False)

    # required arguments
    group = parser.add_argument_group('Required arguments')
    group.add_argument('-e', dest='estr', help='Expression to execute enclosed in quotes. E.g. \'( 2+3 )/4 - 0.45\'', \
                       type=str, metavar='<expr>', required='True')

    # optional arguments
    group_opt = parser.add_argument_group('Optional arguments')
    group_opt.add_argument('-h', '--help', help='Displays usage information and exits.', action='help')

    return parser.parse_args()


# Main function
# =============
def main():
    args = parse_in_args()  # parse, validate and return input arguments
    cmd = re.sub('\^', '**', args.estr) # user may use ^ for exponentiation
    cmd = re.sub('sqrt', 'math.sqrt', cmd) # user may use sqrt() for square root
    print('{expr} = {result}'.format(expr=cmd, result=eval(cmd)))
# =============================================================================================================================
if __name__ == "__main__":
    main()

