#!/usr/bin/env python

"""
Thomas:
"""

########################################
# Imports
########################################

import os
import shutil
import argparse
import sys

from glob import glob



########################################
# Main
########################################

parser = argparse.ArgumentParser()
parser.add_argument( '-o', action='store_true', help='also show .o files')
args = parser.parse_args()


def main():

    pwd = os.path.dirname(os.path.realpath(sys.argv[0]))

    jobscriptDir = os.path.join( pwd, 'jobscripts' )
    stdDir       = os.path.join( pwd, 'std' )


    # ======================================
    # Checking qstat

    print '\n' + '-'*70
    print 'Doing qstat:'
    print

    os.system( 'qstat' )


    # ======================================
    # Checking the error outputs

    eFiles = glob( stdDir + '/*.e*' )

    for eFile in eFiles:

        print '\n' + '-'*70
        print 'Contents of ' + os.path.basename( eFile ) + ':'
        print

        with open( eFile, 'r' ) as eFP:
            lines = eFP.readlines()

        if len(lines) > 60 :
            print ''.join(lines[:30])
            print
            print '----- Some lines not shown here -----'
            print
            print ''.join(lines[-30:])
        else:
            print ''.join(lines)



    # ======================================
    # Checking the error outputs

    if args.o:

        oFiles = glob( stdDir + '/*.o*' )

        see_last_n_lines = 50

        for oFile in oFiles:

            print '\n' + '-'*70
            print 'Contents of ' + os.path.basename( oFile ) + ':'
            print

            with open( oFile, 'r' ) as oFP:
                all_lines = oFP.readlines()

                if len(all_lines) > see_last_n_lines :
                    all_lines = all_lines[-see_last_n_lines:]

                print ''.join(all_lines)












########################################
# End of Main
########################################
if __name__ == "__main__":
    main()