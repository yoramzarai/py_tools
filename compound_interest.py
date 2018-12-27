#!/opt/local/bin/python3

import argparse
#import myutils as mu
#import numpy as np

# Functions
# ============================================================================================================================

# Command-line parsing information
def parse_in_args():
    # place description 
    parser = argparse.ArgumentParser( description='Calculates compound interest.', add_help=False )

    # required arguments
    group = parser.add_argument_group('Required arguments')
    group.add_argument('-a', dest='amt', help='Total amount.', type=float, metavar='<amount>', required='True')
    group.add_argument('-i', dest='i', help='Yearly interest rate in percentage.', type=float, metavar='<interest>', required='True')
    group.add_argument('-n', dest='years', help='Total number of years of return.', type=float, metavar='<years>', required='True')

    # optional arguments
    group_opt = parser.add_argument_group('Optional arguments')
    group_opt.add_argument('-h', '--help', help='Displays usage information and exits.', action='help')

    return( parser.parse_args() )
    

# Main function
# =============
def main():
    args = parse_in_args()  # parse, validate and return input arguments
    pay = args.amt * (1 + args.i/100)**args.years
    print( 'Total return with interest = {:.4f}'.format(pay),
           ', monthly payment = {:.4f}'.format( pay / ( 12 * args.years ) ), sep='', end='.\n',  )


# =============================================================================================================================
if __name__ == "__main__":
    main()

