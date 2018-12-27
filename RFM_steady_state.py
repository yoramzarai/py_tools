#!/opt/local/bin/python3
import argparse

import numpy as np
from numpy import linalg as LA


# RFM steady-state function
def RFM_steady_state(rates):
    '''
    This function computes the RFM steady-states and the sensitivities.
    
    Usage: [ R, e, s ] = RFM_steady_state( rates_vector )
    
    Where:  s - sensitivities vector
    '''
    r = np.power(rates,-1/2)
    A = np.diag(r,1) + np.diag(r,-1)
    s, V = LA.eig(A)
    sigma = np.amax(s)
    zeta = V[:,np.argmax(s)]
    R = np.power(sigma,-2) # steady-state production rate
    e = np.power(sigma,-1) * np.divide(np.multiply(r[1:],zeta[2:]),zeta[1:-1]) # steady-state density
    s = 2 * np.power(sigma,-3) * np.power(r,3) * np.multiply(zeta[:-1],zeta[1:]) / LA.norm(zeta) # sensitivities
    return R,e,s


# Command-line parsing information
def parse_in_args():
    # place description 
    parser = argparse.ArgumentParser( description='Computes RFM steady-states', add_help=False )

    # required arguments
    group = parser.add_argument_group('Required arguments')
    group.add_argument('-l', dest='rates', help='Rates list.', type=float, nargs='+', metavar=('l0', 'l1'), required='True')

    # optional arguments
    group_opt = parser.add_argument_group('Optional arguments')
    group_opt.add_argument('-h', '--help', help='Displays usage information and exits.', action='help')

    return( parser.parse_args() )

# Main function
# =============
def main():
    args = parse_in_args()  # parse, validate and return input arguments

    R,e,s = RFM_steady_state(args.rates)
    np.set_printoptions( precision = 4, floatmode = 'fixed' )
    print('rates = ', args.rates, end=':\n')
    print('R = {0:2.4f}'.format( R ) )
    print('e = ', e, '\ns (sensitivities) = ', s, end='\n')

# =============================================================================================================================
if __name__ == "__main__":
    main()

