#!/opt/local/bin/python3
#
# Python utils.
#
#
# Yoram Zarai, 10/11/18
# ==========================================================================================

import sys
from os.path import basename

# Functions
# =========================================================================

# Usage information to stdout (USE argparse instead)
def myusage( usg_info):
    print( usg_info[0], ( 'Usage: ' + basename( sys.argv[0] ) + ' ' + usg_info[1] ), \
           usg_info[2], sep='\n\n', end='\n', file=sys.stdout )

# check iuput arguments validity
def examine_input_args( num_args, usg_info ):
    if( ( len( sys.argv ) > 1 ) and ( sys.argv[1] == '-h' ) ):
        myusage( usg_info )
        quit()
    elif( len( sys.argv ) != num_args ):
        print( 'Received', len( sys.argv ), 'arguments, require', num_args, '!!' );
        myusage( usg_info )
        quit()
    else:
        return( sys.argv )

    
# A decorator to dump finction inputs and outputs
def fdump( func ):
    ''' Prints function input and output variables. '''
    def dump_cont( *args, **kwargs ):
        print( 'Function name: ', func.__name__ )
        print( 'Function document: ', func.__doc__ )
        print( 'Input argumens: ', ' '.join( map( str, args ) ) )
        print( 'Input keyword arguments: ', kwargs.items() )
        out = func( *args, **kwargs )
        print( 'Output: ', out )
        return out
    return dump_cont

