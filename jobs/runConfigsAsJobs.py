

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

from glob import glob
from time import sleep


########################################
# Main
########################################

parser = argparse.ArgumentParser()
parser.add_argument( '--test', action='store_true', help='Does not submit the job, but creates the .sh file and prints')
parser.add_argument( '-q', '--queue',
    type=str, choices=['short', 'all', 'long', '8nm', '1nh', '8nh', '1nd', '2nd', '1nw', '2nw' ],
    default='long', help='which queue to submit to')
parser.add_argument( '-n', '--normalmemory', action='store_true', help='By default more memory is requested; this option disables that')
parser.add_argument( '-k', '--keep', action='store_true', help='Does not clean the output and jobscript directories')
args = parser.parse_args()


# Figure out the platform
host = os.environ['HOSTNAME']
if host == 't3ui17':
    onPsi = True
    onLxplus = False
elif 'lxplus' in host:
    onPsi = False
    onLxplus = True



def main():

    if onLxplus and args.queue in ['short', 'all', 'long' ]:
        print 'Queue {0} does not exist on {1}; Please pick from {2}'.format(
            args.queue, host, ', '.join(['8nm', '1nh', '8nh', '1nd', '2nd', '1nw', '2nw'])    )
        return
    elif onPsi and args.queue in ['8nm', '1nh', '8nh', '1nd', '2nd', '1nw', '2nw']:
        print 'Queue {0} does not exist on {1}; Please pick from {2}'.format(
            args.queue, host, ', '.join(['short', 'all', 'long' ])    )
        return


    pwd = os.getcwd()

    jobscriptDir = os.path.join( pwd, 'jobscripts' )
    stdDir       = os.path.join( pwd, 'std' )
    LSFJOBdirs   = glob('LSFJOB_*')

    # Clean old directories
    if not args.keep:
        print 'Cleaning up old directories'
        shutil.rmtree( jobscriptDir )
        
        if onPsi:
            shutil.rmtree( stdDir )
        elif onLxplus: 
            for LSFJOBdir in LSFJOBdirs: shutil.rmtree(LSFJOBdir)

    # Make directories if necessary
    if not os.path.isdir(jobscriptDir): os.makedirs( jobscriptDir )
    if onPsi and not os.path.isdir(stdDir): os.makedirs( stdDir )
            

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

        # 'Config_Sep29_electron_EB_ECALonly.config',
        # 'Config_Sep29_electron_EE_ECALonly.config',

        # These succesfully ran
        # 'Config_Sep30_electron_EB_ECALTRK.config',
        # 'Config_Sep30_electron_EB_ECALonly.config',
        # 'Config_Sep30_electron_EE_ECALTRK.config',
        # 'Config_Sep30_electron_EE_ECALonly.config',
        # 'Config_Sep30_photon_EB_ECALonly.config',
        # 'Config_Sep30_photon_EE_ECALonly.config',

        'Config_Oct06_electron_EB_SAMETGT.config',
        'Config_Oct06_electron_EE_SAMETGT.config',

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

    if onPsi: 
        p( '#$ -o ' + stdDir )
        p( '#$ -e ' + stdDir )
        p( 'source /swshare/psit3/etc/profile.d/cms_ui_env.sh' )
        p( 'source $VO_CMS_SW_DIR/cmsset_default.sh' )


    # Going into right directory
    p( 'cd {0}/src'.format( os.path.abspath( os.environ['CMSSW_BASE'] ) ) )
    p( 'eval `scramv1 runtime -sh`' )
    p( 'cd RegressionTraining' )

    p( '#' + '-'*50 )
    p( 'echo "START OF RUN"' )
    p( '#' + '-'*50 )

    p( './regression.exe python/' + cfg )

    p( '#' + '-'*50 )
    p( 'echo "END OF RUN"' )
    p( '#' + '-'*50 )

    sh_fp.close()


    # ======================================
    # Setting permissions and submitting

    os.system( 'chmod 777 ' + sh_file  )


    # ------------------
    # Parsing the command

    if onPsi:

        # qsub part of command
        cmd = 'qsub -q {0}.q '.format(args.queue)

        # Request more memory by default, but don't if argument is passed
        if not args.normalmemory:
            cmd += '-l h_vmem=5g '

        # Pass the sh file
        cmd += os.path.relpath(sh_file)

    elif onLxplus:

        cmd = 'bsub -q {0} -J {1} < '.format(args.queue, sh_file.rsplit('/',1)[-1].replace('.sh','') ) + os.path.relpath(sh_file)


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