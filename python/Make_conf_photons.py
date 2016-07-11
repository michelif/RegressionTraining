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


########################################
# Main
########################################

def main():

    # Instantiate the Config class which prints a .config file
    config = Config()

    config.Name = "photonConfig"

    # filename of the input root file
    #root_file = 'FlatNtupFull_13May_SepTrees.root'
    #root_file = 'FlatNtupFull_18May_DoubleElectron.root'
    #root_file = 'Ntup_20May_DoubleElectron.root'
    #root_file = 'Ntup_30May_DoublePhoton_somefailed.root'
    #root_file = 'Ntup_01June_DoublePhoton.root'
    #root_file = 'Ntup_05June_photons_LowHighPt.root'
    # root_file = 'Ntup_12June_photons_lowhighpt.root'
    

    # root_file = 'Ntup_Jun22_lowpt_training.root'
    root_file = 'Ntup_Jun22_fullpt_training.root'

    # out_filename = 'Config_24Jun_photon_lowpt_OLDVARS.config'
    out_filename = 'Config_24Jun_photon_fullpt_OLDVARS.config'


    config.Name = out_filename.replace('.config','')

    ntup_path = os.path.abspath('../../NTuples/')

    # For iterating:
    #root_file = 'output.root'
    #ntup_path = '/afs/cern.ch/work/t/tklijnsm/EGM/CMSSW_8_0_4/src/SimpleFlatTreeProducer/SimpleNtuplizer/cfgs/'

    if not os.path.isdir( ntup_path ):
        print 'Error: "{0}"" is not a directory'.format( ntup_path )
    physical_path = lambda input_root_file: os.path.join( ntup_path, input_root_file )


    ########################################
    # BDT settings
    ########################################

    config.InputFiles = physical_path( root_file )

    # Don't run the Ep combination for photons
    config.DoCombine        = "False"

    config.Options = [
        "MinEvents=200",
        "Shrinkage=0.1",
        "NTrees=1000",
        "MinSignificance=5.0",
        "EventWeight=min(1,exp(-(genPt-50)/50))",
        ]

    config.Target           = "genEnergy / ( scRawEnergy + scPreshowerEnergy )"
    config.TargetError      = "1.253*abs( BDTresponse - genEnergy / ( scRawEnergy + scPreshowerEnergy ) )"
    #config.TargetComb       = "( genEnergy - ( scRawEnergy + scPreshowerEnergy )*BDTresponse ) / ( trkMomentum - ( scRawEnergy + scPreshowerEnergy )*BDTresponse )"
    config.HistoConfig      = "jobs/dummy_Histo.config"
    
    config.CutBase          = "eventNumber%2==0 && genPt<2000"
    config.CutEB            = "scIsEB"
    config.CutEE            = "!scIsEB"
    config.CutError         = "(eventNumber%2!=0) && (((eventNumber-1)/2)%4==3)"
    #config.CutComb          = "(eventNumber%2!=0) && (((eventNumber-1)/2)%4!=3)"

    # # Add an additional cut so that the regression is fast
    # NtupIDcut = 200
    # config.CutBase  += ' && (NtupID<={0})'.format( NtupIDcut )
    # config.CutError += ' && (NtupID<={0})'.format( NtupIDcut )
    # config.CutComb  += ' && (NtupID<={0})'.format( NtupIDcut )


    ########################################
    # Order Electron tree branches
    ########################################

    # Try to read tree branches from the input root file
    #tree_gDirectory = 'een_analyzer/ElectronTree'
    tree_gDirectory = 'een_analyzer/PhotonTree'

    # ---------------------
    # JBs branches for EE (order is important)
    # ---------------------

    common_vars = [
        
        # Same as in electron case
        'nVtx',
        'scRawEnergy',
        # 'scEta',
        # 'scPhi',
        'scEtaWidth',
        'scPhiWidth',
        'scSeedR9',
        'scSeedRawEnergy/scRawEnergy',
        # 'scSeedLeftRightAsym',
        # 'scSeedTopBottomAsym',
        'scSeedSigmaIetaIeta',
        'scSeedSigmaIetaIphi',
        'scSeedSigmaIphiIphi',
        'N_ECALClusters',
        
        # 'clusterMaxDR',
        # 'clusterMaxDRDPhi',
        # 'clusterMaxDRDEta',
        # 'clusterMaxDRRawEnergy/scRawEnergy',
        # 'clusterRawEnergy[0]/scRawEnergy',
        # 'clusterRawEnergy[1]/scRawEnergy',
        # 'clusterRawEnergy[2]/scRawEnergy',
        # 'clusterDPhiToSeed[0]',
        # 'clusterDPhiToSeed[1]',
        # 'clusterDPhiToSeed[2]',
        # 'clusterDEtaToSeed[0]',
        # 'clusterDEtaToSeed[1]',
        # 'clusterDEtaToSeed[2]',
        
        # Only for photons
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

    EE_vars = common_vars + [
        'scPreshowerEnergy/scRawEnergy',
        'preshowerEnergyPlane1/scRawEnergy',
        'preshowerEnergyPlane2/scRawEnergy',
        'iXCoordinate',
        'iYCoordinate',
        ]

    EB_vars = common_vars + [
        'e5x5/scSeedRawEnergy',
        'iEtaCoordinate',
        'iPhiCoordinate',
        'iEtaMod5',
        'iPhiMod2',
        'iEtaMod20',
        'iPhiMod20',
        ]


    print 'Using the following branches for EE:'
    print '    ' + '\n    '.join( EE_vars )
    print 'Using the following branches for EB:'
    print '    ' + '\n    '.join( EB_vars )

    # Write to class
    #config.Tree        = tree_gDirectory
    config.Tree          = tree_gDirectory
    config.VariablesEE   = EE_vars
    config.VariablesEB   = EB_vars

    print "\nAll branches in root file:"
    Read_branches_from_rootfile( physical_path(root_file) , tree_gDirectory )


    ########################################
    # Output config file
    ########################################

    # out_filename = 'photon_config.config'
    # out_filename = 'Config_24Jun_photons_OLDVARS.config'
    config.Parse( out_filename )

    # Test if the config file can be read by ROOT TEnv
    print '\nReading in {0} and trying ROOT.TEnv( ..., 0 ):'.format( out_filename )
    I_TEnv = ROOT.TEnv()
    I_TEnv.ReadFile( out_filename, 0 )
    I_TEnv.Print()
    print 'Exited normally'
    print '='*70
    print


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