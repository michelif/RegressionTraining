#!/usr/bin/env python
"""
Thomas:
"""

########################################
# Imports
########################################

import os
import argparse
import pickle

import sys
sys.path.append('src')
from SlicePlot import SlicePlot


import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = kError;")
ROOT.RooMsgService.instance().setSilentMode(True)

ROOT.RooMsgService.instance().getStream(1).removeTopic( ROOT.RooFit.Eval )
ROOT.RooMsgService.instance().getStream(1).removeTopic( ROOT.RooFit.Generation )
ROOT.RooMsgService.instance().getStream(1).removeTopic( ROOT.RooFit.Minimization )
ROOT.RooMsgService.instance().getStream(1).removeTopic( ROOT.RooFit.Plotting )
ROOT.RooMsgService.instance().getStream(1).removeTopic( ROOT.RooFit.Fitting )
ROOT.RooMsgService.instance().getStream(1).removeTopic( ROOT.RooFit.Integration )
ROOT.RooMsgService.instance().getStream(1).removeTopic( ROOT.RooFit.LinkStateMgmt )
ROOT.RooMsgService.instance().getStream(1).removeTopic( ROOT.RooFit.Caching )
ROOT.RooMsgService.instance().getStream(1).removeTopic( ROOT.RooFit.Optimization )
ROOT.RooMsgService.instance().getStream(1).removeTopic( ROOT.RooFit.ObjectHandling )
ROOT.RooMsgService.instance().getStream(1).removeTopic( ROOT.RooFit.InputArguments )
ROOT.RooMsgService.instance().getStream(1).removeTopic( ROOT.RooFit.Tracing )
ROOT.RooMsgService.instance().getStream(1).removeTopic( ROOT.RooFit.Contents )
ROOT.RooMsgService.instance().getStream(1).removeTopic( ROOT.RooFit.DataHandling )
ROOT.RooMsgService.instance().getStream(1).removeTopic( ROOT.RooFit.NumIntegration )
ROOT.RooMsgService.instance().getStream(1).removeTopic( ROOT.RooFit.Eval )

ROOT.gSystem.Load("libHiggsAnalysisGBRLikelihood")
ROOT.gROOT.LoadMacro( os.getcwd() + "/src/LoadDataset.C" )

# Paths to regression results
result_path = os.getcwd()
# result_path = '/mnt/t3nfs01/data01/shome/tklijnsm/EGM/CMSSW_8_0_4/src/RegressionTraining/Plotting'
physpath_ws = lambda filename: os.path.join( result_path, filename )

# Paths to Ntuples
if os.environ['USER'] == 'tklijnsm':
    ntup_path = '/mnt/t3nfs01/data01/shome/tklijnsm/EGM/CMSSW_8_0_4/src/NTuples'
else:
    # Different users can implement different paths here
    ntup_path = '/mnt/t3nfs01/data01/shome/tklijnsm/EGM/CMSSW_8_0_4/src/NTuples'

physpath_ntup = lambda filename: os.path.join( ntup_path, filename )


########################################
# Main
########################################

def Fit():

    ########################################
    # Command line options
    ########################################

    parser = argparse.ArgumentParser()
    parser.add_argument( 'resultfile', type=str )
    parser.add_argument( '--particle', type=str, default='TODO', choices=[ 'electron', 'photon', 'TODO' ] )
    parser.add_argument( '--region', type=str, default='TODO', choices=[ 'EB', 'EE', 'TODO' ] )
    parser.add_argument( '--ecaltrk', action='store_true', help='Tells the program trk variables are included')
    parser.add_argument( '--testrun', action='store_true', help='selects only a few events for testing purposes')
    args = parser.parse_args()


    ########################################
    # Settings
    ########################################

    # This is the _results.root filename
    ws_file = args.resultfile

    # Region needs to be determined carefully because the right workspace needs to be loaded
    if args.region == 'TODO':
        if 'EB' in ws_file:
            region = 'EB'
            dobarrel = True
        elif 'EE' in ws_file:
            region = 'EE'
            dobarrel = False
        else:
            print 'Could not determine region (EB or EE) from the filename; pass it manually using the flag --region **'
            return
    else:
        if args.region == 'EB':
            region = 'EB'
            dobarrel = True
        elif args.region == 'EE':
            region = 'EE'
            dobarrel = False


    if args.particle == 'TODO':
        if 'electron' in ws_file:
            particle = 'electron'
        elif 'photon' in ws_file:
            particle = 'photon'
        else:
            print 'Could not determine particle (electron or photon) from the filename; pass it manually using the flag --region **'
            return
    else:
        particle = args.particle


    if args.ecaltrk:
        # User explicitely tells to use ecaltrk variables
        ecaltrk = True
        ecaltrkstr = 'TRK'
    else:
        # Find out if trk variables were included
        if 'ECALonly' in ws_file:
            ecaltrk = False
            ecaltrkstr = ''
        elif 'ECALTRK' in ws_file:
            ecaltrk = True
            ecaltrkstr = 'TRK'
        else:
            ecaltrk = False
            ecaltrkstr = ''


    plotdir = 'plotsPY_{0}_{1}'.format( particle, region )
    if ecaltrk: plotdir += '_ECALTRK'


    ntup_file = 'Ntup_Jul22_fullpt_testing_sample.root'
    tree_name = particle.capitalize() + 'Tree'

    pline()
    print 'Summary of input data for Fit.py:'
    print '    WS file:   ' + ws_file
    print '    particle:  ' + particle
    print '    region:    ' + region
    print '    ecaltrk:   ' + str(ecaltrk)
    print '    plotdir:   ' + plotdir
    print '    ntuple:    ' + ntup_file
    print '    ntup tree: ' + tree_name


    ########################################
    # FITTING PROCEDURE
    ########################################

    # ======================================
    # Get the workspace and set the variables

    pline()
    print 'Getting workspace'

    LWS = ROOT.LoadWorkspace( physpath_ws(ws_file), dobarrel )
    tgtvar     = LWS.tgtvar
    sigpdf     = LWS.sigpdf
    sigmeanlim = LWS.sigmeanlim
    meantgt    = LWS.meantgt


    scRawEnergy       = ROOT.RooRealVar( "scRawEnergy", "scRawEnergy", 0.)
    scPreshowerEnergy = ROOT.RooRealVar( "scPreshowerEnergy", "scPreshowerEnergy", 0.)
    r9                = ROOT.RooRealVar( "r9", "r9", 0.)
    nVtx              = ROOT.RooRealVar( "nVtx", "nVtx", 0.)
    pt                = ROOT.RooRealVar( "pt", "pt", 0.)
    genEta            = ROOT.RooRealVar( "genEta", "genEta", 0.)
    genE              = ROOT.RooRealVar( "genEnergy", "genEnergy", 0.)
    genPt             = ROOT.RooRealVar( "genPt", "genPt", 0.)

    cor74E            = ROOT.RooRealVar( "corrEnergy74X",      "corrEnergy74X", 0. )
    cor74Eerror       = ROOT.RooRealVar( "corrEnergy74XError", "corrEnergy74XError", 0. )

    # Only add to ArgList if TRK variables were included in the training
    trkMom            = ROOT.RooRealVar( "trkMomentum", "trkMomentum", 0.)
    trkMomE           = ROOT.RooRealVar( "trkMomentumError", "trkMomentumError", 0.)
    trkEta            = ROOT.RooRealVar( "trkEta", "trkEta", 0.)
    trkPhi            = ROOT.RooRealVar( "trkPhi", "trkPhi", 0.)
    fbrem             = ROOT.RooRealVar( "fbrem", "fbrem", 0.)
    ECALweight        = ROOT.RooRealVar( "ECALweight", "ECALweight", 0. )
    TRKweight         = ROOT.RooRealVar( "TRKweight",  "TRKweight", 0. )


    # ======================================
    # Set ranges where reasonably possible

    r9.setRange(    0., 1.2 );
    pt.setRange(    0., 10000. );
    genE.setRange(  0., 10000. );
    genPt.setRange( 0., 10000. );

    if dobarrel:
        genEta.setRange( -1.5, 1.5 )
    else:
        genEta.setRange( -3, 3 )


    # ======================================
    # Define which vars to use

    Vars = [
        tgtvar,
        meantgt.FuncVars(),
        scRawEnergy,
        scPreshowerEnergy,
        r9,
        nVtx,
        pt,
        genEta,
        genE,
        genPt,
        cor74E,
        cor74Eerror,
        ]

    if ecaltrk:
        Vars.extend([
            trkMom,
            trkMomE,
            trkEta,
            trkPhi,
            fbrem,
            ECALweight,
            TRKweight,
            ])

    VarsArgList = ROOT.RooArgList()
    for Var in Vars: VarsArgList.add(Var)


    # ======================================
    # Create the dataset

    eventcut = ''
    if args.testrun: eventcut = "eventNumber%20==1||eventNumber%20==0"

    print 'Getting dataset (using the macro)'
    hdata = ROOT.LoadDataset( eventcut, dobarrel, physpath_ntup(ntup_file), 'een_analyzer', tree_name, VarsArgList )
    print '  Using {0} entries'.format( hdata.numEntries() )


    ########################################
    # Add columns to dataset for E_raw,cor,cor74 over E_true
    ########################################

    # NOTE: BRACKETS AROUND THE FORMULA ARE EXTREMELY IMPORTANT
    #       There is no error message, but the results are interpreted totally different without the brackets!
    #       Or it is the RooArgLists that can't be passed in the defition of the RooFormula directly

    rawArgList = ROOT.RooArgList( scRawEnergy, scPreshowerEnergy, genE )
    rawformula = ROOT.RooFormulaVar( 'rawformula', 'raw', '((@0+@1)/@2)', rawArgList )
    rawvar = hdata.addColumn(rawformula)
    rawvar.setRange( 0., 2. )
    rawvar.setBins(800)

    ecor74ArgList = ROOT.RooArgList( cor74E, genE )
    ecor74formula = ROOT.RooFormulaVar( 'ecor74formula', 'corr. (74X)', '(@0/@1)', ecor74ArgList )
    ecor74var = hdata.addColumn(ecor74formula)
    ecor74var.setRange( 0., 2. )
    ecor74var.setBins(800)


    if not ecaltrk:
        ecorArgList = ROOT.RooArgList( sigmeanlim, tgtvar )
        ecorformula = ROOT.RooFormulaVar(
            'ecorformula', 'corr.',
            '(@0/@1)',
            ecorArgList
            )
    else:
        ecorArgList = ROOT.RooArgList( sigmeanlim, tgtvar )
        ecorformula = ROOT.RooFormulaVar(
            'ecorformula', 'corr.',
            '(@0/@1)',
            ecorArgList
            )

    # ecorArgList = ROOT.RooArgList( sigmeanlim, tgtvar )
    # ecorformula = ROOT.RooFormulaVar( 'ecorformula', 'corr.', '(@0/@1)', ecorArgList )

    ecorvar = hdata.addColumn(ecorformula)
    ecorvar.setRange( 0., 2. )
    ecorvar.setBins(800)




    ########################################
    # Make the fits
    ########################################

    pline()
    print 'Start fitting\n'

    globalPt_bounds = [
        0.,
        100.,
        500.,
        2500.,
        6500.,
        ]

    allPt_bounds = [
        0.,    5.,    10.,   15.,   20.,   25.,  30.,   40.,   50., 60.,   80.,   100.,
        150.,  200.,  250.,  300.,  400.,  500.,
        750.,  1000., 1250., 1500., 2000., 2500.,
        3000., 3500., 4000., 5000., 6500.
        ]


    for i_globalPtBin in xrange(len(globalPt_bounds)-1):

        min_globalPt = globalPt_bounds[i_globalPtBin]
        max_globalPt = globalPt_bounds[i_globalPtBin+1]

        print '  Reducing total dataset to genPt between {0} and {1}'.format( min_globalPt, max_globalPt )
        hdata_globalPtBin = hdata.reduce( 'genPt>{0}&&genPt<{1}'.format( min_globalPt, max_globalPt ) )
        print '    Number of entries in this genPt selection: ' + str(hdata_globalPtBin.numEntries())

        # Get the finer genPt bounds inside this global bin
        localPt_bounds = allPt_bounds[ allPt_bounds.index(min_globalPt) : allPt_bounds.index(max_globalPt) + 1 ]

        genPt_name = 'GENPT{0}-{1}'.format( int(min_globalPt), int(max_globalPt) )
        genPt_sliceplot = SlicePlot(
            name     = genPt_name,
            longname = particle + region + ecaltrkstr + '_' + genPt_name,
            plotdir  = plotdir
            )
        genPt_sliceplot.SetDataset( hdata_globalPtBin )
        genPt_sliceplot.SetHistVars([
            rawvar,
            ecor74var,
            ecorvar,
            ])
        genPt_sliceplot.SetSliceVar(
            genPt,
            localPt_bounds,
            )
        genPt_sliceplot.FitSlices()



########################################
# Functions
########################################

def pline(s='='):
    print '\n' + s*70


########################################
# End of Main
########################################
if __name__ == "__main__":
    Fit()