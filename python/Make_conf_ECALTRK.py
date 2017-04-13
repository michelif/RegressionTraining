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

def Make_conf(Verbose=True):


    parser = argparse.ArgumentParser()
    parser.add_argument( '--inputrootfile', '-i', type=str, help='Path to root file',
        # default='/afs/cern.ch/work/t/tklijnsm/public/CMSSW_8_0_4/src/NTuples/Ntup_Jul22_fullpt_training.root'
        default='/afs/cern.ch/work/t/tklijnsm/public/CMSSW_8_0_4/src/NTuples/Ntup_Jul22_fullpt_training.root'
        )
    parser.add_argument(
        '--particle', metavar='N', type=str, nargs='+', help='Specify particles',
        default=['electron','photon'],choices=['electron','photon']
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


    # root_file = 'Ntup_Jul15_fullpt_training.root'

    # Small testing samples -- do NOT use these for plots!
    #    root_file = 'Ntup_Jun22_lowpt_testing_sample.root'
    # Low + high pt sample
    # root_file = 'Ntup_Jun22_fullpt_training.root'    
    # Only low pt sample
    # root_file = 'Ntup_Jun22_lowpt_training.root'

    # ------------------------------
    # 22 July samples - Latest set of branches
    # root_file = 'Ntup_Jul22_fullpt_testing_sample.root' # ONLY FOR QUICK TESTS
    root_file = 'Ntup_Jul22_fullpt_training.root'

    # ntup_path = os.path.join( '/data/userdata/rclsa/ElectronTrees/Jul17/' )
    # ntup_path = os.path.join( os.environ['CMSSW_BASE'], 'src/NTuples' )

    if os.environ['HOSTNAME'] == 't3ui17':
        ntup_path = os.path.join( '/mnt/t3nfs01/data01/shome/tklijnsm/Samples/RegressionSamples', '22Jul_samples' )
    else:
        ntup_path = '/afs/cern.ch/work/t/tklijnsm/public/CMSSW_8_0_4/src/NTuples'

    datestr = strftime( '%b%d' )

    if not os.path.isdir( ntup_path ):
        print 'Error: "{0}"" is not a directory'.format( ntup_path )
    physical_path = lambda input_root_file: os.path.join( ntup_path, input_root_file )


    return_configs = []

    # for region in [ 'EB', 'EE' ]:
    for region in args.region:
        for ECAL_AND_TRK in [ False ]:
            # for particle in [ 'electron', 'photon' ]:
            for particle in args.particle:
                if ECAL_AND_TRK and particle=='photon': continue # Photon doesn't have TRK vars

                # Instantiate the Config class which prints a .config file
                config = Config()

                config.Name       = 'Config_' + datestr + '_' + particle + '_' + region


                if ECAL_AND_TRK:
                    config.Name += '_ECALTRK'
                else:
                    config.Name += '_ECALonly'

                if args.name and args.name!='NONE' : config.Name += '_' + args.name


                config.InputFiles = physical_path( root_file )
                config.Tree       = 'een_analyzer/{0}Tree'.format( particle.capitalize() )


                ########################################
                # BDT settings
                ########################################

                # config.Options = [
                #     "MinEvents=200",
                #     "Shrinkage=0.1",
                #     "NTrees=1000",
                #     "MinSignificance=5.0",
                #     "EventWeight=1",
                #     ]

                config.Options = [
                    "MinEvents=300",
                    "Shrinkage=0.15",
                    "NTrees=1000",
                    "MinSignificance=5.0",
                    "EventWeight=1",
                    ]

                # Set the target - be careful to include the tracker energy in the target for the Ep combination
                if ECAL_AND_TRK:
                    config.Target           = "genEnergy * (ECALweight + TRKweight) / ( scRawEnergy*ECALweight + scPreshowerEnergy*ECALweight + trkMomentum*TRKweight )"
                else:
                    config.Target           = "genEnergy / ( scRawEnergy + scPreshowerEnergy )"
                # config.Target           = "genEnergy / ( scRawEnergy + scPreshowerEnergy )"

                config.TargetError      = "1.253*abs( BDTresponse - genEnergy / ( scRawEnergy + scPreshowerEnergy ) )"
                config.HistoConfig      = "jobs/dummy_Histo.config"
                
                config.CutEB            = "scIsEB"
                config.CutEE            = "!scIsEB"

                if region == 'EB':
                    config.DoEB         = "True"
                else:
                    config.DoEB         = "False"


                # ======================================
                # Sample division - need a part for the ECAL-only training, and a part for the combination


                # WITH EP COMBINATION TRAINING IN SERIES, THIS IS NO LONGER NEEDED

                # if particle == 'electron':
                #     # 66% for the main BDT - divide the sample in divideNumber pieces, and use all but one piece for the main BDT
                #     divideNumber            = 3
                #     config.CutBase          = "eventNumber%{0}!=0".format( divideNumber )

                #     # 17% for combination, 17% for error
                #     config.CutComb          = "eventNumber%{0}==0 && eventNumber%{1}==0".format( divideNumber, 2*divideNumber )
                #     config.CutError         = "eventNumber%{0}==0 && eventNumber%{1}!=0".format( divideNumber, 2*divideNumber )
                # elif particle == 'photon':
                #     config.CutBase          = '1.0'
                #     config.CutComb          = '1.0'
                #     config.CutError         = '1.0'


                config.CutBase          = '1.0'
                config.CutComb          = '1.0'
                config.CutError         = '1.0'


                # # TEMPORARY: cut events drastically for test mode
                config.CutBase  += " && NtupID<4000"
                config.CutComb  += " && NtupID<4000"
                config.CutError += " && NtupID<4000"


                ########################################
                # Order tree branches
                ########################################


                # Agreed list on November 23:

                # eval[0]  = raw_energy;
                # eval[1]  = the_sc->etaWidth();
                # eval[2]  = the_sc->phiWidth(); 
                # eval[3]  = full5x5_ess.e5x5/raw_energy;
                # eval[4]  = ele.hcalOverEcalBc();
                # eval[5]  = rhoValue_;
                # eval[6]  = theseed->eta() - the_sc->position().Eta();
                # eval[7]  = reco::deltaPhi( theseed->phi(),the_sc->position().Phi());
                # eval[8]  = full5x5_ess.r9;
                # eval[9]  = full5x5_ess.sigmaIetaIeta;
                # eval[10]  = full5x5_ess.sigmaIetaIphi;
                # eval[11]  = full5x5_ess.sigmaIphiIphi;
                # eval[12]  = full5x5_ess.eMax/full5x5_ess.e5x5;
                # eval[13]  = full5x5_ess.e2nd/full5x5_ess.e5x5;
                # eval[14]  = full5x5_ess.eTop/full5x5_ess.e5x5;
                # eval[15]  = full5x5_ess.eBottom/full5x5_ess.e5x5;
                # eval[16]  = full5x5_ess.eLeft/full5x5_ess.e5x5;
                # eval[17]  = full5x5_ess.eRight/full5x5_ess.e5x5;
                # eval[18]  = EcalClusterToolsT<true>::e2x5Max(*theseed, &*ecalRecHits, topology_)/full5x5_ess.e5x5;
                # eval[19]  = EcalClusterToolsT<true>::e2x5Left(*theseed, &*ecalRecHits, topology_)/full5x5_ess.e5x5;
                # eval[20]  = EcalClusterToolsT<true>::e2x5Right(*theseed, &*ecalRecHits, topology_)/full5x5_ess.e5x5;
                # eval[21]  = EcalClusterToolsT<true>::e2x5Top(*theseed, &*ecalRecHits, topology_)/full5x5_ess.e5x5;
                # eval[22]  = EcalClusterToolsT<true>::e2x5Bottom(*theseed, &*ecalRecHits, topology_)/full5x5_ess.e5x5;
                # eval[23]  = N_SATURATEDXTALS;
                # eval[24]  = std::max(0,numberOfClusters);
                # eval[25] = clusterRawEnergy[0]/raw_energy;
                # eval[26] = clusterRawEnergy[1]/raw_energy;
                # eval[27] = clusterRawEnergy[2]/raw_energy;
                # eval[28] = clusterDPhiToSeed[0];
                # eval[29] = clusterDPhiToSeed[1];
                # eval[30] = clusterDPhiToSeed[2];
                # eval[31] = clusterDEtaToSeed[0];
                # eval[32] = clusterDEtaToSeed[1];
                # eval[33] = clusterDEtaToSeed[2];

                # eval[34] = ieta;
                # eval[35] = iphi;
                # eval[36] = (ieta-signieta)%5;
                # eval[37] = (iphi-1)%2;
                # eval[38] = (abs(ieta)<=25)*((ieta-signieta)) + (abs(ieta)>25)*((ieta-26*signieta)%20);  
                # eval[39] = (iphi-1)%20;

                # eval[34] = raw_es_energy/raw_energy;
                # eval[35] = the_sc->preshowerEnergyPlane1()/raw_energy;
                # eval[36] = the_sc->preshowerEnergyPlane2()/raw_energy;
                # eval[37] = eeseedid.ix();
                # eval[38] = eeseedid.iy();


                common_vars = [

                    # ======================================
                    # Common variables

                    # 'pt',            # RCLSA: you cannot use the result of the previous training for the new one
                    # 'nVtx',          # rho should be enough information for the BDT
                    # 'scEta',         # Requires alignment information; use crystal number of the seed instead
                    # 'scPhi',         # Requires alignment information; use crystal number of the seed instead
                    #            'scSeedRawEnergy/scRawEnergy',  # RCLSA: Redundant with the one below

                    'scRawEnergy',
                    'scEtaWidth',
                    'scPhiWidth',
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

                if ECAL_AND_TRK:
                    # ADD THE TRK VARIABLES TO THE MAIN BDT
                    # Output should be compared to ECAL-only BDT output
                    common_vars += [

                        # '( scRawEnergy + scPreshowerEnergy ) * BDTresponse',
                        # This is simply the corrected energy, I don't we need to pass this (The BDT already has the target in there)

                        # 'BDTerror/BDTresponse',
                        # I guess the error we also don't have to pass -- The BDT will already be conscious of the error

                        'trkMomentumRelError',

                        # Replace this simply by the trkMomentum only
                        # 'trkMomentum/(( scRawEnergy + scPreshowerEnergy )*BDTresponse)',
                        'trkMomentum',

                        'eleEcalDriven',
                        # 'full5x5_r9',
                        'fbrem',
                        'gsfchi2',
                        'gsfndof', 
                        'trkEta',
                        'trkPhi'
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
                    # 'preshowerEnergyPlane1/scRawEnergy',
                    # 'preshowerEnergyPlane2/scRawEnergy',
                    ]

                if Verbose:
                    print '\n' + '-'*70
                    print 'Making config file ' + config.Name + '.config'
                    print '  Using the following branches for EE:'
                    print '    ' + '\n    '.join( config.VariablesEE )
                    print '  Using the following branches for EB:'
                    print '    ' + '\n    '.join( config.VariablesEB )


                ########################################
                # Ep combination
                ########################################

                # NOVEMBER 25: NO LONGER NECESSARY TO RUN OLD EP COMBO
                config.DoCombine        = "False"


                # # Only do the combination for the electron AND there are no tracking variables
                # if particle == 'electron' and not ECAL_AND_TRK:

                #     config.DoCombine        = "True"

                #     config.TargetComb       = "( genEnergy - ( scRawEnergy + scPreshowerEnergy )*BDTresponse ) / ( trkMomentum - ( scRawEnergy + scPreshowerEnergy )*BDTresponse )"
                #     config.TargetError      = "1.253*abs(BDTresponse - genEnergy/(scRawEnergy+scPreshowerEnergy))"

                #     config.VariablesComb = [
                #         '( scRawEnergy + scPreshowerEnergy ) * BDTresponse',
                #         'BDTerror/BDTresponse',
                #         'trkMomentumRelError',
                #         'trkMomentum/(( scRawEnergy + scPreshowerEnergy )*BDTresponse)',
                #         'eleEcalDriven',
                #         'full5x5_r9',
                #         'fbrem',
                #         'gsfchi2',
                #         'gsfndof', 
                #         'trkEta',
                #         'trkPhi'     # The best way to describe cracks is to use the track (unbiased) directorion
                #        # 'trkMomentum',                                # RCLSA Again, let us choose one absolute scale and the rest be relative
                #        # 'BDTerror/BDTresponse/trkMomentumRelError',   
                #        # ( '( scRawEnergy + scPreshowerEnergy )*BDTresponse/trkMomentum  *' +
                #        #   'sqrt( BDTerror/BDTresponse*BDTerror/BDTresponse + trkMomentumRelError*trkMomentumRelError)' ),
                #        # 'eleClass',
                #        # 'scIsEB',
                #         ]
                
                # else:
                #     config.DoCombine        = "False"




                ########################################
                # Output
                ########################################

                # if Verbose:
                #     # Print all branches as a check
                #     print "\nAll branches in root file:"
                #     Read_branches_from_rootfile( physical_path(root_file) , config.Tree )

                config.Parse()

                # # Test if the config file can be read by ROOT TEnv
                # print '\nReading in {0} and trying ROOT.TEnv( ..., 0 ):'.format( out_filename )
                # I_TEnv = ROOT.TEnv()
                # I_TEnv.ReadFile( out_filename, 0 )
                # I_TEnv.Print()
                # print 'Exited normally'
                # print '='*70
                # print

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
    Make_conf()
