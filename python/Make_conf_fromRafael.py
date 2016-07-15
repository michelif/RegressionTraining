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


########################################
# Main
########################################

def main():

    # Small testing samples -- do NOT use these for plots!
    # root_file = 'Ntup_Jun22_fullpt_testing_sample.root'
    #    root_file = 'Ntup_Jun22_lowpt_testing_sample.root'

    # Low + high pt sample
    root_file = 'Ntup_Jun22_fullpt_training.root'
    
    # Only low pt sample
    # root_file = 'Ntup_Jun22_lowpt_training.root'


    # ntup_path = os.path.join( '/data/userdata/rclsa/ElectronTrees/' )
    ntup_path = os.path.join( os.environ['CMSSW_BASE'], 'src/NTuples' )


    datestr = strftime( '%b%d' )

    if not os.path.isdir( ntup_path ):
        print 'Error: "{0}"" is not a directory'.format( ntup_path )
    physical_path = lambda input_root_file: os.path.join( ntup_path, input_root_file )



    for particle in [ 'electron', 'photon' ]:

        # Instantiate the Config class which prints a .config file
        config = Config()

        config.Name       = 'Config_' + particle + '_' + datestr

        config.InputFiles = physical_path( root_file )
        config.Tree       = 'een_analyzer/{0}Tree'.format( particle.capitalize() )


        ########################################
        # BDT settings
        ########################################

        config.Options = [
            "MinEvents=200",
            "Shrinkage=0.1",
            "NTrees=1000",
            "MinSignificance=5.0",
            # "EventWeight=max( min(1,exp(-(genPt-50)/50)), 0.1 )", # <-- What to do?
            "EventWeight=1", # <-- No one really likes the weights
            ]

        config.Target           = "genEnergy / ( scRawEnergy + scPreshowerEnergy )"
        config.TargetError      = "1.253*abs( BDTresponse - genEnergy / ( scRawEnergy + scPreshowerEnergy ) )"
        config.HistoConfig      = "jobs/dummy_Histo.config"
        
        # config.CutBase          = "eventNumber%2==0"
        # Remove 2/7th of the events (reduces training from 70% to 50%)
        config.CutBase          = "eventNumber%2==0 && ( (eventNumber/2)%7==0 || (eventNumber/2)%7==1 )"

        config.CutEB            = "scIsEB"
        config.CutEE            = "!scIsEB"
        config.CutError         = "(eventNumber%2!=0) && (((eventNumber-1)/2)%4==3)"

        # Add an additional cut so that the regression is fast
        # NtupIDcut = 10000
        # config.CutBase  += ' && (NtupID<={0})'.format( NtupIDcut )
        # config.CutError += ' && (NtupID<={0})'.format( NtupIDcut )
        # config.CutComb  += ' && (NtupID<={0})'.format( NtupIDcut )


        ########################################
        # Order tree branches
        ########################################

        common_vars = [

            # ======================================
            # Common variables

            # 'pt',            # RCLSA: you cannot use the result of the previous training for the new one
            # 'nVtx',          # rho should be enough information for the BDT
            'scRawEnergy',
            # 'scEta',         # Requires alignment information; use crystal number of the seed instead
            # 'scPhi',         # Requires alignment information; use crystal number of the seed instead
            'scEtaWidth',
            'scPhiWidth',
            #            'scSeedRawEnergy/scRawEnergy',  # RCLSA: Redundant with the one below
            'full5x5_e5x5/scRawEnergy',
            'hadronicOverEm',
            'rhoValue',
            'delEtaSeed',
            'delPhiSeed',


            # ======================================
            # Showershape variables

            # Use full 5x5 instead
            # 'r9',
            # 'eHorizontal',
            # 'eVertical',
            # 'sigmaIetaIeta',
            # 'sigmaIetaIphi',
            # 'sigmaIphiIphi',
            # 'e5x5',
            # 'e3x3',
            # 'eMax',
            # 'e2nd',
            # 'eTop',
            # 'eBottom',
            # 'eLeft',
            # 'eRight',
            # 'e2x5Max',
            # 'e2x5Left',
            # 'e2x5Right',
            # 'e2x5Top',
            # 'e2x5Bottom',

            # Normalization to scRawEnergy necessary?

            'full5x5_r9',
            #            'full5x5_eHorizontal',   # RCLSA: Redundant
            #            'full5x5_eVertical',     # RCLSA: Redundant
            'full5x5_sigmaIetaIeta',
            'full5x5_sigmaIetaIphi',
            'full5x5_sigmaIphiIphi',
            # 'full5x5_e5x5',               # RCLSA: Use ratios
            # 'full5x5_e3x3/full5x5_e5x5',  # RCLSA: Redundant, this is R9
            'full5x5_eMax/full5x5_e5x5',
            'full5x5_e2nd/full5x5_e5x5',
            'full5x5_eTop/full5x5_e5x5',
            'full5x5_eBottom/full5x5_e5x5',
            'full5x5_eLeft/full5x5_e5x5',
            'full5x5_eRight/full5x5_e5x5',
            'full5x5_e2x5Max/full5x5_e5x5',
            'full5x5_e2x5Left/full5x5_e5x5',
            'full5x5_e2x5Right/full5x5_e5x5',
            'full5x5_e2x5Top/full5x5_e5x5',
            'full5x5_e2x5Bottom/full5x5_e5x5',


            # ======================================
            # Saturation variables

            'N_SATURATEDXTALS',
            #            'seedIsSaturated',   # RCLSA: probably overkill
            #            'seedCrystalEnergy/scSeedRawEnergy',   # RCLSA: There is only 1/1e6 cases in which the max energy is not the seed


            # ======================================
            # Cluster variables

            'N_ECALClusters',
            #            'clusterMaxDR',          # RCLSA Very mismodelled variables
            #            'clusterMaxDRDPhi',
            #            'clusterMaxDRDEta',
            #            'clusterMaxDRRawEnergy',

            'clusterRawEnergy[0]/scRawEnergy',
            'clusterRawEnergy[1]/scRawEnergy',
            'clusterRawEnergy[2]/scRawEnergy',
            'clusterDPhiToSeed[0]',
            'clusterDPhiToSeed[1]',
            'clusterDPhiToSeed[2]',
            'clusterDEtaToSeed[0]',
            'clusterDEtaToSeed[1]',
            'clusterDEtaToSeed[2]',

            ]


        config.VariablesEB = common_vars + [
            # 'cryEtaCoordinate',  # Requires alignment information; use crystal number of the seed instead
            # 'cryPhiCoordinate',  # Requires alignment information; use crystal number of the seed instead
            'iEtaCoordinate',
            'iPhiCoordinate',
            'iEtaMod5',
            'iPhiMod2',
            'iEtaMod20',
            'iPhiMod20',
            ]

        config.VariablesEE = common_vars + [
            # 'cryXCoordinate',  # Requires alignment information; use crystal number of the seed instead
            # 'cryYCoordinate',  # Requires alignment information; use crystal number of the seed instead
            'iXCoordinate',
            'iYCoordinate',
            'scPreshowerEnergy/scRawEnergy',
            'preshowerEnergyPlane1/scRawEnergy',
            'preshowerEnergyPlane2/scRawEnergy',
            ]


        print 'Using the following branches for EE:'
        print '    ' + '\n    '.join( config.VariablesEE )
        print 'Using the following branches for EB:'
        print '    ' + '\n    '.join( config.VariablesEB )


        ########################################
        # Ep combination
        ########################################

        # Only do the combination for the electron
        if particle == 'electron':

            config.DoCombine        = "True"

            config.TargetComb       = "( genEnergy - ( scRawEnergy + scPreshowerEnergy )*BDTresponse ) / ( trkMomentum - ( scRawEnergy + scPreshowerEnergy )*BDTresponse )"
            config.CutComb          = "(eventNumber%2!=0) && (((eventNumber-1)/2)%4!=3)"

            config.VariablesComb = [
                '( scRawEnergy + scPreshowerEnergy ) * BDTresponse',
                'BDTerror/BDTresponse',
                'trkMomentum',
                'trkMomentumRelError',
                'BDTerror/BDTresponse/trkMomentumRelError',
                '( scRawEnergy + scPreshowerEnergy )*BDTresponse/trkMomentum',
                ( '( scRawEnergy + scPreshowerEnergy )*BDTresponse/trkMomentum  *' +
                  'sqrt( BDTerror/BDTresponse*BDTerror/BDTresponse + trkMomentumRelError*trkMomentumRelError)' ),
                'eleEcalDriven',
                'eleTrackerDriven',
                'eleClass',
                'scIsEB',
                ]
        
        else:
            config.DoCombine        = "False"


        ########################################
        # Output
        ########################################

        # Print all branches as a check
        print "\nAll branches in root file:"
        Read_branches_from_rootfile( physical_path(root_file) , config.Tree )

        config.Parse()

        # # Test if the config file can be read by ROOT TEnv
        # print '\nReading in {0} and trying ROOT.TEnv( ..., 0 ):'.format( out_filename )
        # I_TEnv = ROOT.TEnv()
        # I_TEnv.ReadFile( out_filename, 0 )
        # I_TEnv.Print()
        # print 'Exited normally'
        # print '='*70
        # print


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
    main()