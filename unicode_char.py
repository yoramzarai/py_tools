#!/opt/local/bin/python3
import argparse
import myutils


# Command-line parsing information
def parse_in_args():
    # place description 
    parser = argparse.ArgumentParser( description='Converts Unicode code point to character', add_help=False )

    # required arguments
    group = parser.add_argument_group('Required arguments')
    group.add_argument('-u', dest='ucp', help='Unicode code point with 0x prefix (e.g. 0x00a3)', \
                       type=lambda x: int(x,0), metavar='<code point>', required='True')
    
    # optional arguments
    group_opt = parser.add_argument_group('Optional arguments')
    group_opt.add_argument('-h', '--help', help='Displays usage information and exits.', action='help')

    return( parser.parse_args() )

#@myutils.fdump
def unicode_trans( val ):
    import unicodedata
    name = unicodedata.name( val )
    print( 'code point = {}, name = {}, char = {}'.format( hex(ord(val)), name, unicodedata.lookup( name ) ) ) 


# Main function
# =============
def main():
    args = parse_in_args()  # parse, validate and return input arguments
    unicode_trans( chr( args.ucp ) )


# =============================================================================================================================
if __name__ == "__main__":
    main()
