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
    # fullpt_root_file = 'Ntup_Jun22_fullpt_testing_sample.root'
    # lowpt_root_file  = 'Ntup_Jun22_lowpt_testing_sample.root'

    # Low + high pt sample
    fullpt_root_file = 'Ntup_Jun22_fullpt_training.root'
    
    # Only low pt sample
    lowpt_root_file = 'Ntup_Jun22_lowpt_training.root'


    ntup_path = os.path.join( os.environ['CMSSW_BASE'], 'src/NTuples' )
    datestr = strftime( '%b%d' )

    if not os.path.isdir( ntup_path ):
        print 'Error: "{0}"" is not a directory'.format( ntup_path )
    physical_path = lambda input_root_file: os.path.join( ntup_path, input_root_file )



    ########################################
    # BASE CONFIG - This is low pt electrons
    #   Configs for photons and and other pt ranges are created by altering this one
    ########################################

    # Instantiate the Config class which prints a .config file
    base_config = Config()

    base_config.Name       = 'Config_electron_lowpt_' + datestr

    base_config.InputFiles = physical_path( lowpt_root_file )
    base_config.Tree       = 'een_analyzer/ElectronTree'


    ########################################
    # BDT settings
    ########################################

    base_config.Options = [
        "MinEvents=200",
        "Shrinkage=0.1",
        "NTrees=1000",
        "MinSignificance=5.0",
        "EventWeight=max( min(1,exp(-(genPt-50)/50)), 0.1 )", # <-- What to do?
        ]

    base_config.Target           = "genEnergy / ( scRawEnergy + scPreshowerEnergy )"
    base_config.TargetError      = "1.253*abs( BDTresponse - genEnergy / ( scRawEnergy + scPreshowerEnergy ) )"
    base_config.HistoConfig      = "jobs/dummy_Histo.config"
    
    base_config.CutBase          = "eventNumber%2==0"
    base_config.CutEB            = "scIsEB"
    base_config.CutEE            = "!scIsEB"
    base_config.CutError         = "(eventNumber%2!=0) && (((eventNumber-1)/2)%4==3)"

    # Add an additional cut so that the regression is fast
    # NtupIDcut = 10000
    # base_config.CutBase  += ' && (NtupID<={0})'.format( NtupIDcut )
    # base_config.CutError += ' && (NtupID<={0})'.format( NtupIDcut )
    # base_config.CutComb  += ' && (NtupID<={0})'.format( NtupIDcut )


    ########################################
    # Order tree branches
    ########################################

    common_vars = [

        # ======================================
        # Common variables

        'pt',
        # 'nVtx',          # rho should be enough information for the BDT
        'scRawEnergy',
        # 'scEta',         # Requires alignment information; use crystal number of the seed instead
        # 'scPhi',         # Requires alignment information; use crystal number of the seed instead
        'scEtaWidth',
        'scPhiWidth',
        'scSeedRawEnergy/scRawEnergy',
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
        'full5x5_eHorizontal',
        'full5x5_eVertical',
        'full5x5_sigmaIetaIeta',
        'full5x5_sigmaIetaIphi',
        'full5x5_sigmaIphiIphi',
        'full5x5_e5x5',
        'full5x5_e3x3',
        'full5x5_eMax',
        'full5x5_e2nd',
        'full5x5_eTop',
        'full5x5_eBottom',
        'full5x5_eLeft',
        'full5x5_eRight',
        'full5x5_e2x5Max',
        'full5x5_e2x5Left',
        'full5x5_e2x5Right',
        'full5x5_e2x5Top',
        'full5x5_e2x5Bottom',


        # ======================================
        # Saturation variables

        'N_SATURATEDXTALS',
        'seedIsSaturated',
        'seedCrystalEnergy/scRawEnergy',


        # ======================================
        # Cluster variables

        'N_ECALClusters',
        'clusterMaxDR',
        'clusterMaxDRDPhi',
        'clusterMaxDRDEta',
        'clusterMaxDRRawEnergy',

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


    base_config.VariablesEB = common_vars + [
        # 'cryEtaCoordinate',  # Requires alignment information; use crystal number of the seed instead
        # 'cryPhiCoordinate',  # Requires alignment information; use crystal number of the seed instead
        'iEtaCoordinate',
        'iPhiCoordinate',
        'iEtaMod5',
        'iPhiMod2',
        'iEtaMod20',
        'iPhiMod20',
        ]

    base_config.VariablesEE = common_vars + [
        # 'cryXCoordinate',  # Requires alignment information; use crystal number of the seed instead
        # 'cryYCoordinate',  # Requires alignment information; use crystal number of the seed instead
        'iXCoordinate',
        'iYCoordinate',
        'scPreshowerEnergy/scRawEnergy',
        'preshowerEnergyPlane1/scRawEnergy',
        'preshowerEnergyPlane2/scRawEnergy',
        ]


    # print 'Using the following branches for EE:'
    # print '    ' + '\n    '.join( base_config.VariablesEE )
    # print 'Using the following branches for EB:'
    # print '    ' + '\n    '.join( base_config.VariablesEB )


    ########################################
    # Ep combination
    ########################################

    # Only do the combination for the electron
    base_config.DoCombine        = "True"

    base_config.TargetComb       = "( genEnergy - ( scRawEnergy + scPreshowerEnergy )*BDTresponse ) / ( trkMomentum - ( scRawEnergy + scPreshowerEnergy )*BDTresponse )"
    base_config.CutComb          = "(eventNumber%2!=0) && (((eventNumber-1)/2)%4!=3)"

    base_config.VariablesComb = [
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




    ########################################
    # Output
    ########################################

    # lowpt electrons - this is simply the base config defined above
    base_config.Parse()

    # fullpt electrons - only change the root file
    base_config.Name       = 'Config_electron_fullpt_' + datestr
    base_config.InputFiles = physical_path( fullpt_root_file )
    base_config.Parse()

    # lowpt photons
    base_config.Name       = 'Config_photon_lowpt_' + datestr
    base_config.InputFiles = physical_path( lowpt_root_file )
    base_config.Tree       = 'een_analyzer/PhotonTree'
    base_config.DoCombine  = "False"
    base_config.Parse()

    # fullpt photons
    base_config.Name       = 'Config_photon_fullpt_' + datestr
    base_config.InputFiles = physical_path( fullpt_root_file )
    base_config.Tree       = 'een_analyzer/PhotonTree'
    base_config.DoCombine  = "False"
    base_config.Parse()



    ########################################
    # OLD VARIABLES
    ########################################

    # Remove the max( ..., 0.1, ) from the eventweight
    base_config.Options = [
        "MinEvents=200",
        "Shrinkage=0.1",
        "NTrees=1000",
        "MinSignificance=5.0",
        "EventWeight=min(1,exp(-(genPt-50)/50))",
        ]


    # lowpt electrons
    base_config.Name       = 'Config_electron_lowpt_' + datestr + '_OLDVARS'
    base_config.InputFiles = physical_path( lowpt_root_file )
    base_config.Tree       = 'een_analyzer/ElectronTree'
    base_config.DoCombine  = "True"

    OLD_common_electron_vars = [
        'nVtx',
        'scRawEnergy',
        'scEta',
        'scPhi',
        'scEtaWidth',
        'scPhiWidth',
        'r9',
        'scSeedRawEnergy/scRawEnergy',
        'eMax',
        'e2nd',
        'eHorizontal',  # 'scSeedLeftRightAsym',
        'eVertical',    # 'scSeedTopBottomAsym',
        'sigmaIetaIeta',
        'sigmaIetaIphi',
        'sigmaIphiIphi',
        'N_ECALClusters',
        'clusterMaxDR',
        'clusterMaxDRDPhi',
        'clusterMaxDRDEta',
        'clusterMaxDRRawEnergy/scRawEnergy',

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

    base_config.VariablesEB = OLD_common_electron_vars + [
        'cryEtaCoordinate',
        'cryPhiCoordinate',
        'iEtaCoordinate',
        'iPhiCoordinate',
        # 'scSeedCryEta',
        # 'scSeedCryPhi',
        # 'scSeedCryIetaV2',
        # 'scSeedCryIphiV2',
        ]

    base_config.VariablesEE = OLD_common_electron_vars + [
        'scPreshowerEnergy/scRawEnergy',
        # 'scSeedCryIxV2',
        # 'scSeedCryIyV2',
        'iXCoordinate',
        'iYCoordinate',
        ]

    base_config.Parse()

    # fullpt oldvars
    base_config.Name       = 'Config_electron_fullpt_' + datestr + '_OLDVARS'
    base_config.InputFiles = physical_path( fullpt_root_file )
    base_config.Parse()


    # lowpt photons
    base_config.Name       = 'Config_photon_lowpt_' + datestr + '_OLDVARS'
    base_config.InputFiles = physical_path( lowpt_root_file )
    base_config.Tree       = 'een_analyzer/PhotonTree'
    base_config.DoCombine  = "False"

    OLD_common_photon_vars = [
        'nVtx',
        'scRawEnergy',
        # 'scEta',
        # 'scPhi',
        'scEtaWidth',
        'scPhiWidth',
        'r9',
        'scSeedRawEnergy/scRawEnergy',
        # 'scSeedLeftRightAsym',
        # 'scSeedTopBottomAsym',
        'sigmaIetaIeta',
        'sigmaIetaIphi',
        'sigmaIphiIphi',
        'N_ECALClusters',        

        'hadronicOverEm',
        'rhoValue',
        'delEtaSeed',
        'delPhiSeed',

        'e3x3/e5x5',
        'eMax/e5x5',
        'e2nd/e5x5',
        'eTop/e5x5',
        'eBottom/e5x5',
        'eLeft/e5x5',
        'eRight/e5x5',
        'e2x5Max/e5x5',
        'e2x5Left/e5x5',
        'e2x5Right/e5x5',
        'e2x5Top/e5x5',
        'e2x5Bottom/e5x5',
        ]

    base_config.VariablesEB = OLD_common_photon_vars + [
        'e5x5/scSeedRawEnergy',
        'iEtaCoordinate',
        'iPhiCoordinate',
        'iEtaMod5',
        'iPhiMod2',
        'iEtaMod20',
        'iPhiMod20',
        ]

    base_config.VariablesEE = OLD_common_photon_vars + [
        'scPreshowerEnergy/scRawEnergy',
        'preshowerEnergyPlane1/scRawEnergy',
        'preshowerEnergyPlane2/scRawEnergy',
        'iXCoordinate',
        'iYCoordinate',
        ]

    base_config.Parse()


    # fullpt photons    
    base_config.Name       = 'Config_photon_fullpt_' + datestr + '_OLDVARS'
    base_config.InputFiles = physical_path( fullpt_root_file )
    base_config.Parse()



    # Print all branches as a check
    print "\nAll branches in lowpt root file:"
    Read_branches_from_rootfile( physical_path(lowpt_root_file) , base_config.Tree )

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