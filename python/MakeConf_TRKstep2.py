#!/usr/bin/env python
"""
Thomas:
"""

########################################
# Imports
########################################

import os
import ROOT
from Config import Config
from time import strftime

import argparse

########################################
# Main
########################################

def MakeConf(Verbose=True):

    parser = argparse.ArgumentParser()
    parser.add_argument( '--inputrootfile', '-i', type=str, help='Path to root file',
        # default='../applyRegression/Config_Sep30_electron_EB_ECALonly_appliedRegression_training.root'
        default='../Config_Oct25_electron_EB_ECALonly_appliedRegression_training_ptWeight.root'
        )
    parser.add_argument(
        '--region', metavar='N', type=str, nargs='+', help='Specify regions',
        default=['EB','EE'],choices=['EE','EB']
        )
    parser.add_argument(
        '-n', '--name', type=str, default='NONE', help='Append a string at the end of the name of this config'
        )
    parser.add_argument( '--fast', action='store_true', help='Change some BDT options to be faster (but maybe less precise)')
    args = parser.parse_args()

    datestr = strftime( '%b%d' )

    # Photon does not have TRK vars
    particle = 'electron'

    # Reads off the name of this .py file, so it's clear what made this.
    moduleName = os.path.basename(__file__).replace('MakeConf_','').replace('.py','')

    return_configs = []
    for region in args.region:

        # Instantiate the Config class which prints a .config file
        config = Config()

        config.Name       = 'Config_' + datestr + '_' + particle + '_' + region + '_' + moduleName

        # Append a string to the name if given by the user
        if not args.name == 'NONE':
            config.Name += '_' + args.name

        if args.fast: config.Name += '_FastOptions'

        config.InputFiles = os.path.abspath(args.inputrootfile)

        # config.Tree       = 'een_analyzer/{0}Tree'.format( particle.capitalize() )
        config.Tree       = 'een_analyzer/correction' # <-- May want to change this some time.


        ########################################
        # BDT settings
        ########################################

        if not args.fast:
            config.Options = [
                "MinEvents=200",
                "Shrinkage=0.1",
                "NTrees=1000",
                "MinSignificance=5.0",
                "EventWeight=1",
                ]
        else:
            config.Options = [
                "MinEvents=300", # Down from 200
                "Shrinkage=0.2",
                "NTrees=1000",
                "MinSignificance=5.0", # Down from 5.0
                "EventWeight=1",
                ]

        # config.Target           = "genEnergy / ( scRawEnergy + scPreshowerEnergy )"
        config.Target           = "(genEnergy * (trkMomentum*trkMomentum*trkMomentumRelError*trkMomentumRelError + (scRawEnergy+scPreshowerEnergy)*(scRawEnergy+scPreshowerEnergy)*resolution*resolution) / ( (scRawEnergy+scPreshowerEnergy)*response*trkMomentum*trkMomentum*trkMomentumRelError*trkMomentumRelError + trkMomentum*(scRawEnergy+scPreshowerEnergy)*(scRawEnergy+scPreshowerEnergy)*resolution*resolution ))"

        # Probably neither of these are necessary
        config.TargetError      = "1.253*abs( BDTresponse - genEnergy / ( scRawEnergy + scPreshowerEnergy ) )"
        config.HistoConfig      = "jobs/dummy_Histo.config"
        
        config.CutEB            = "scIsEB"
        config.CutEE            = "!scIsEB"

        if region == 'EB':
            config.DoEB         = "True"
        else:
            config.DoEB         = "False"


        # # ======================================
        # # Sample division - need a part for the ECAL-only training, and a part for the combination

        # # 80% for the main BDT - divide the sample in divideNumber pieces, and use all but one piece for the main BDT
        # divideNumber            = 3
        # config.CutBase          = "eventNumber%{0}!=0".format( divideNumber )

        # # 10% for combination, 10% for error
        # config.CutComb          = "eventNumber%{0}==0 && eventNumber%{1}==0".format( divideNumber, 2*divideNumber )
        # config.CutError         = "eventNumber%{0}==0 && eventNumber%{1}!=0".format( divideNumber, 2*divideNumber )


        # config.CutBase  += " && NtupID<5000"
        # config.CutComb  += " && NtupID<5000"
        # config.CutError += " && NtupID<5000"


        # Limit number of events in training
        # config.CutBase  = "NtupID<1000"
        # config.CutComb  = "NtupID<1000"
        # config.CutError = "NtupID<1000"

        # Pre-selected events have this variable set to 1.0
        config.CutBase  = "(ptWeightCut)"
        config.CutComb  = "(ptWeightCut)"
        config.CutError = "(ptWeightCut)"


        ########################################
        # Order tree branches
        ########################################

        common_vars = [
            "(scRawEnergy+scPreshowerEnergy)*response",
            "resolution/response",
            "trkMomentumRelError",
            "trkMomentum/((scRawEnergy+scPreshowerEnergy)*response)",
            "eleEcalDriven",
            "fbrem",
            "gsfchi2",
            "gsfndof",
            "trkEta",
            "trkPhi",
            ]

        config.VariablesEB = common_vars + [
            ]

        config.VariablesEE = common_vars + [
            ]

        if Verbose:
            print '\n' + '-'*70
            print 'Making config file ' + config.Name + '.config'
            print '  Using the following branches for EE:'
            print '    ' + '\n    '.join( config.VariablesEE )
            print '  Using the following branches for EB:'
            print '    ' + '\n    '.join( config.VariablesEB )

        config.DoCombine        = "False"


        ########################################
        # Output
        ########################################

        config.Parse()
        return_configs.append( config )


    return return_configs


########################################
# Functions
########################################

def Filter( full_list, sel_list ):
    # Functions that FILTERS OUT selection criteria

    # Return the full list if sel_list is empty or None
    if not sel_list:
        return full_list
    elif len(sel_list)==0:
        return full_list

    ret_list = []

    for item in full_list:
        
        # Loop over selection criteria; if found, don't add the item to the output list
        add_item = True
        for sel in sel_list:
            if sel in item:
                add_item = False

        if add_item:
            ret_list.append( item )

    return ret_list



def Read_branches_from_rootfile( root_file, tree_gDirectory ):

    root_fp = ROOT.TFile.Open( root_file )
    tree = root_fp.Get( tree_gDirectory )
    all_branches = [ i.GetName() for i in tree.GetListOfBranches() ]

    print '    ' + '\n    '.join(all_branches)


########################################
# End of Main
########################################
if __name__ == "__main__":
    MakeConf()
