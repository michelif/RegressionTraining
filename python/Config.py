########################################
# Main
########################################

class Config:

    # ======================================
    def __init__( self ):


        ########################################
        # Non-regression parameters
        ########################################

        self.Trainer             = 'GBRLikelihoodTrain'
        self.NumberOfRegressions = '1'
        self.TMVAFactoryOptions  = [ '!V' , '!Silent' , '!Color' , '!DrawProgressBar' ]
        self.OutputDirectory     = './'


        ########################################
        # Regression parameters
        ########################################
        
        self.Name             = "default_config"
        self.InputFiles       = "input_needs_to_be_given.root"
        self.Tree             = "een_analyzer/ElectronTree"
        self.Method           = "BDT"
        self.trainingOptions  = "SplitMode=random:!V"
        
        self.Options          = [
            "MinEvents=200",
            "Shrinkage=0.1",
            "NTrees=1000",
            "MinSignificance=5.0",
            "EventWeight=min(1,exp(-(genPt-50)/50))",
            ]

        self.DoErrors         = "True"
        self.DoCombine        = "True"
        self.DoEB             = "True"

        self.VariablesEB      = [
            "nVtx",
            "scRawEnergy",
            "scEta",
            "scPhi",
            "scEtaWidth",
            "scPhiWidth",
            "scSeedR9",
            "scSeedRawEnergy/scRawEnergy",
            "scSeedEmax/scRawEnergy",
            "scSeedE2nd/scRawEnergy",
            "scSeedLeftRightAsym",
            "scSeedTopBottomAsym",
            "scSeedSigmaIetaIeta",
            "scSeedSigmaIetaIphi",
            "scSeedSigmaIphiIphi",
            "N_ECALClusters",
            "clusterMaxDR",
            "clusterMaxDRDPhi",
            "clusterMaxDRDEta",
            "clusterMaxDRRawEnergy/scRawEnergy",
            "clusterRawEnergy[0]/scRawEnergy",
            "clusterRawEnergy[1]/scRawEnergy",
            "clusterRawEnergy[2]/scRawEnergy",
            "clusterDPhiToSeed[0]",
            "clusterDPhiToSeed[1]",
            "clusterDPhiToSeed[2]",
            "clusterDEtaToSeed[0]",
            "clusterDEtaToSeed[1]",
            "clusterDEtaToSeed[2]",
            "scSeedCryEta",
            "scSeedCryPhi",
            "scSeedCryIetaV2",
            "scSeedCryIphiV2",
            ]

        self.VariablesEE      = [
            "nVtx",
            "scRawEnergy",
            "scEta",
            "scPhi",
            "scEtaWidth",
            "scPhiWidth",
            "scSeedR9",
            "scSeedRawEnergy/scRawEnergy",
            "scSeedEmax/scRawEnergy",
            "scSeedE2nd/scRawEnergy",
            "scSeedLeftRightAsym",
            "scSeedTopBottomAsym",
            "scSeedSigmaIetaIeta",
            "scSeedSigmaIetaIphi",
            "scSeedSigmaIphiIphi",
            "N_ECALClusters",
            "clusterMaxDR",
            "clusterMaxDRDPhi",
            "clusterMaxDRDEta",
            "clusterMaxDRRawEnergy/scRawEnergy",
            "clusterRawEnergy[0]/scRawEnergy",
            "clusterRawEnergy[1]/scRawEnergy",
            "clusterRawEnergy[2]/scRawEnergy",
            "clusterDPhiToSeed[0]",
            "clusterDPhiToSeed[1]",
            "clusterDPhiToSeed[2]",
            "clusterDEtaToSeed[0]",
            "clusterDEtaToSeed[1]",
            "clusterDEtaToSeed[2]",
            "scPreshowerEnergy/scRawEnergy",
            "scSeedCryIxV2",
            "scSeedCryIyV2",
            ]

        self.VariablesComb    = [
            "(scRawEnergy+scPreshowerEnergy)*BDTresponse",
            "BDTerror/BDTresponse",
            "trkMomentum",
            "trkMomentumRelError",
            "BDTerror/BDTresponse/trkMomentumRelError",
            "(scRawEnergy+scPreshowerEnergy)*BDTresponse/trkMomentum",
            "(scRawEnergy+scPreshowerEnergy)*BDTresponse/trkMomentum*sqrt(BDTerror/BDTresponse*BDTerror/BDTresponse+trkMomentumRelError*trkMomentumRelError)",
            "eleEcalDriven",
            "eleTrackerDriven",
            "eleClass",
            "scIsEB",
            ]

        self.Target           = "genEnergy/(scRawEnergy+scPreshowerEnergy)"
        self.TargetError      = "1.253*abs(BDTresponse - genEnergy/(scRawEnergy+scPreshowerEnergy))"
        self.TargetComb       = "(genEnergy-(scRawEnergy+scPreshowerEnergy)*BDTresponse)/(trkMomentum-(scRawEnergy+scPreshowerEnergy)*BDTresponse)"
        self.HistoConfig      = "jobs/dummy_Histo.config"
        self.CutBase          = "(eventNumber%2==0)&&(isMatched==1)"
        self.CutEB            = "scIsEB"
        self.CutEE            = "!scIsEB"
        self.CutError         = "((eventNumber%2!=0)&&(((eventNumber-1)/2)%4==3)&&(isMatched==1))"
        self.CutComb          = "((eventNumber%2!=0)&&(((eventNumber-1)/2)%4!=3)&&(isMatched==1))"


    # ======================================
    def Parse( self, out_filename = None ):

        if not out_filename:
            out_filename = self.Name + '.config'

        self.basename = 'Regression.1'
        out_fp = open( out_filename, 'w' )

        # Function to write a line to the file
        self.w = lambda text: out_fp.write( text + '\n' )

        # Standard parse functions

        self.parse_BDT_settings = lambda var: '{0}: {1}'.format( var, getattr( self, var ) )
        self.parse_BDT_settings_list = lambda var: '{0}: {1}'.format( var, ':'.join(getattr( self, var )) )

        self.parse_normal = lambda var: '{0}.{1}: {2}'.format( self.basename, var, getattr( self, var ) )
        self.parse_list = lambda var: '{0}.{1}: {2}'.format( self.basename, var, ':'.join(getattr( self, var )) )


        self.w( '## Config file generated by default_config.py\n')

        self.w( self.parse_BDT_settings( "Trainer" ) )
        self.w( self.parse_BDT_settings( "NumberOfRegressions" ) )
        self.w( self.parse_BDT_settings_list( "TMVAFactoryOptions" ) )
        self.w( self.parse_BDT_settings( "OutputDirectory" ) )

        self.w( '\n' )

        self.w( self.parse_normal( "Name" ) )
        self.w( self.parse_normal( "InputFiles" ) )
        self.w( self.parse_normal( "Tree" ) )
        self.w( self.parse_normal( "Method" ) )
        self.w( self.parse_normal( "trainingOptions" ) )
        
        self.w( self.parse_list( "Options" ) )
        
        self.w( self.parse_normal( "DoErrors" ) )
        self.w( self.parse_normal( "DoCombine" ) )
        self.w( self.parse_normal( "DoEB" ) )

        self.w( self.parse_list( "VariablesEB" ) )
        self.w( self.parse_list( "VariablesEE" ) )

        if self.DoCombine == "True":
            self.w( self.parse_list( "VariablesComb" ) )
        self.w( self.parse_normal( "Target" ) )
        self.w( self.parse_normal( "TargetError" ) )
        if self.DoCombine == "True":
            self.w( self.parse_normal( "TargetComb" ) )
        self.w( self.parse_normal( "HistoConfig" ) )
        self.w( self.parse_normal( "CutBase" ) )
        self.w( self.parse_normal( "CutEB" ) )
        self.w( self.parse_normal( "CutEE" ) )
        self.w( self.parse_normal( "CutError" ) )
        if self.DoCombine == "True":
            self.w( self.parse_normal( "CutComb" ) )

        out_fp.close()
