#!/usr/bin/env python
"""
Thomas:
"""

########################################
# Imports
########################################

# LATEST MODULE FOR CONFIGURATION FILES
from python.Make_conf_fromRafael import Make_conf

import os
import argparse


########################################
# Main
########################################

def main():

    # Make sure an argument is passed
    parser = argparse.ArgumentParser()
    parser.add_argument("particle")
    parser.add_argument( '--test', action='store_true', help='Does not run the config, but creates it and prints some info')
    args = parser.parse_args()
    

    ########################################
    # Create config files and select
    ########################################

    # Go into directory python (cleanest approach to get the config files in the right directory)
    os.chdir('python')

    # Create the configuration files in python/
    configs = Make_conf(Verbose=False)

    print
    for config in configs: print 'Created ' + config.Name + '.config'

    print '\nSelecting the first config that contains "{0}"'.format( args.particle )

    Found_config = False
    for config in configs:
        if args.particle in config.Name:
            run_this_config = config
            Found_config = True

    if not Found_config:
        print 'Could not find a config file with substring "{0}" in its name'.format( args.particle )
        return
    else:
        print '    Selected ' + run_this_config.Name

    # Go back up
    os.chdir('..')


    ########################################
    # Run the config file
    ########################################

    cmd = './regression.exe python/' + run_this_config.Name + '.config'
    print '\nRunning the following command:'
    print cmd

    if args.test:

        print '\n' + '='*70
        print 'Test mode: Not actually running the config'

        print 'Using the following branches for EE:'
        print '    ' + '\n    '.join( run_this_config.VariablesEE )
        print 'Using the following branches for EB:'
        print '    ' + '\n    '.join( run_this_config.VariablesEB )

        print '\nThe output file will be named:'
        print '    ' + run_this_config.Name + '_results.root'

        if os.path.isfile(run_this_config.Name + '_results.root'):
            print 'Warning: this file already exists'

    else:
        os.system(cmd)


########################################
# End of Main
########################################
if __name__ == "__main__":
    main()