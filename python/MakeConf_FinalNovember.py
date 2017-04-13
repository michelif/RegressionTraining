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
        default='/afs/cern.ch/work/r/rcoelhol/public/CMSSW_8_0_12/src/NTuples/Ntup_10Nov_ElectronPhoton.root'
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


    datestr = strftime( '%b%d' )
    return_configs = []

    for region in args.region:
        for particle in args.particle:

            # Instantiate the Config class which prints a .config file
            config = Config()

            config.Name       = 'Config_' + datestr + '_' + particle + '_' + region

            if args.name and args.name!='NONE' : config.Name += '_' + args.name


            config.InputFiles = os.path.abspath( args.inputrootfile )
            config.Tree       = 'een_analyzer/{0}Tree'.format( particle.capitalize() )


            ########################################
            # BDT settings
            ########################################

            if args.fast:

                config.Options = [
                    "MinEvents=300",
                    "Shrinkage=0.15",
                    "NTrees=1000",
                    "MinSignificance=5.0",
                    "EventWeight=1",
                    ]
                config.Name += '_FastOptions'

            else:

                config.Options = [
                    "MinEvents=200",
                    "Shrinkage=0.1",
                    "NTrees=1000",
                    "MinSignificance=5.0",
                    "EventWeight=1",
                    ]


            config.Target           = "genEnergy / ( scRawEnergy + scPreshowerEnergy )"

            # Probably not needed
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


            config.CutBase          = '1.0'

            # These are for the old (regular BDT) EP combination - no longer needed
            config.CutComb          = '1.0'
            config.CutError         = '1.0'


            # Cut events (otherwise running into CPU limits)
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

                'full5x5_r9',
                'full5x5_sigmaIetaIeta',
                'full5x5_sigmaIetaIphi',
                'full5x5_sigmaIphiIphi',
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


                # ======================================
                # Cluster variables

                'N_ECALClusters',

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

            # EB specific
            config.VariablesEB = common_vars + [
                'iEtaCoordinate',
                'iPhiCoordinate',
                'iEtaMod5',
                'iPhiMod2',
                'iEtaMod20',
                'iPhiMod20',
                ]

            # EE specific
            config.VariablesEE = common_vars + [
                'iXCoordinate',
                'iYCoordinate',
                'scPreshowerEnergy/scRawEnergy',
                # 'preshowerEnergyPlane1/scRawEnergy', # Disabled as of November 2016 (did not influence regression)
                # 'preshowerEnergyPlane2/scRawEnergy',# Disabled as of November 2016 (did not influence regression)
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
            config.DoErrors         = "False"


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
