import ROOT, sys
from array import array

response   = array( 'f', [ 0. ] )
resolution = array( 'f', [ 0. ] )

outputFile = ROOT.TFile.Open(sys.argv[1]+"_withRegression.root", "RECREATE")
inputFile1 = ROOT.TFile.Open(sys.argv[1]+".root")
inputFile2 = ROOT.TFile.Open(sys.argv[1]+"_application.root")

inputTree1 = inputFile1.Get('een_analyzer/ElectronTree')
inputTree2 = inputFile2.Get('een_analyzer/correction')

outputFile.mkdir('een_analyzer')
outputFile.cd('een_analyzer')
outputTree = inputTree1.CloneTree(0)
outputTree.Branch('response', response, 'response/F')
outputTree.Branch('resolution', resolution, 'resolution/F')

for ievent in xrange(inputTree1.GetEntries()):
    inputTree1.GetEntry(ievent)
    inputTree2.GetEntry(ievent)

    response[0]   = inputTree2.response
    resolution[0] = inputTree2.resolution

    outputTree.Fill()

outputTree.Write()
outputFile.Close()
