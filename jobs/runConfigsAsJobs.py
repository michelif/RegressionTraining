

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

from time import sleep


########################################
# Main
########################################

parser = argparse.ArgumentParser()
parser.add_argument( '--test', action='store_true', help='Does not submit the job, but creates the .sh file and prints')
parser.add_argument( '-q', '--queue', type=str, choices=['short', 'all', 'long'], default='long', help='which queue to submit to')
parser.add_argument( '-n', '--normalmemory', action='store_true', help='By default more memory is requested; this option disables that')
args = parser.parse_args()


def main():

    pwd = os.getcwd()

    jobscriptDir = os.path.join( pwd, 'jobscripts' )
    stdDir       = os.path.join( pwd, 'std' )

    if os.path.isdir( jobscriptDir ): shutil.rmtree( jobscriptDir )
    if os.path.isdir( stdDir ):       shutil.rmtree( stdDir )

    os.makedirs( jobscriptDir )
    os.makedirs( stdDir )


    cfgs = [
        # 'Config_electron_fullpt_Jun25.config',
        # 'Config_electron_fullpt_Jun25_OLDVARS.config',
        # 'Config_electron_lowpt_Jun25.config',
        # 'Config_electron_lowpt_Jun25_OLDVARS.config',
        # 'Config_photon_fullpt_Jun25.config',
        # 'Config_photon_fullpt_Jun25_OLDVARS.config',
        # 'Config_photon_lowpt_Jun25.config',
        # 'Config_photon_lowpt_Jun25_OLDVARS.config',
        # 'Config_electron_Jul12.config',
        # 'Config_photon_Jul12.config',
        # 'Config_electron_Jul13.config',
        # 'Config_photon_Jul13.config',

        # 'Config_Sep26_electron_EB_ECALTRK.config',
        # 'Config_Sep26_electron_EB_ECALonly.config',
        # 'Config_Sep26_electron_EE_ECALTRK.config',
        # 'Config_Sep26_electron_EE_ECALonly.config',
        # 'Config_Sep26_photon_EB_ECALonly.config',
        # 'Config_Sep26_photon_EE_ECALonly.config',

        'Config_Sep29_electron_EB_ECALonly.config',
        'Config_Sep29_electron_EE_ECALonly.config',

        ]

    for cfg in cfgs:
        Make_jobscript( cfg, jobscriptDir, stdDir )

        if cfg != cfgs[-1] and not args.test:
            nSleep = 5
            print 'Sleeping {0} seconds to prevent jobs from interfering with one another'.format(nSleep)
            sleep(nSleep)



########################################
# Functions
########################################

def Make_jobscript( cfg, jobscriptDir, stdDir ):

    # ======================================
    # Creating the sh file

    sh_file = jobscriptDir + '/run_' + cfg.replace( '.config', '.sh' )

    sh_fp = open( sh_file, 'w' )
    p = lambda text: sh_fp.write( text + '\n' )

    # Setup

    p( '#$ -o ' + stdDir )
    p( '#$ -e ' + stdDir )

    p( 'source /swshare/psit3/etc/profile.d/cms_ui_env.sh' )
    p( 'source $VO_CMS_SW_DIR/cmsset_default.sh' )

    # Going into right directory
    p( 'cd {0}/src'.format( os.path.abspath( os.environ['CMSSW_BASE'] ) ) )
    p( 'eval `scramv1 runtime -sh`' )
    p( 'cd RegressionTraining' )


    p( '#' + '-'*50 )
    p( 'echo "Number of threads:"' )
    p( 'echo $OMP_NUM_THREADS' )
    p( '#' + '-'*50 )

    p( './regression.exe python/' + cfg )

    p( '#' + '-'*50 )
    p( 'echo "Number of threads:"' )
    p( 'echo $OMP_NUM_THREADS' )
    p( '#' + '-'*50 )


    sh_fp.close()


    # ======================================
    # Setting permissions and submitting

    os.system( 'chmod 777 ' + sh_file  )


    # ------------------
    # Parsing the command

    # qsub part of command
    cmd = 'qsub -q {0}.q '.format(args.queue)

    # Request more memory by default, but don't if argument is passed
    if not args.normalmemory:
        cmd += '-l h_vmem=5g '

    # Pass the sh file
    cmd += os.path.relpath(sh_file)


    # ------------------
    # Submission

    if args.test:
        print 'TEST MODE. Would now run: ' + cmd
    else:
        # os.system( 'bsub -q 2nw ' + sh_file )
        os.system( cmd )
        # print 'Script disabled'



########################################
# End of Main
########################################
if __name__ == "__main__":
    main()