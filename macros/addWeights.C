/*************************************************
  This will add a branch to the specified TTree
  in the specified files.  Useful for adding
  event weights, cross-sections, etc...

  Michael B. Anderson
  Feb 20, 2009
*************************************************/

#include <vector>
#include <cmath>
#include <iostream>

// #include "Math/VectorUtil.h"
// #include "Math/GenVector/LorentzVector.h"
#include "TMath.h"
#include "TFile.h"
#include "TString.h"
#include "TBranch.h"
#include "TTree.h"
#include "TMatrixD.h"
#include "TVectorD.h"
#include "TF1.h"

using namespace std;
using namespace ROOT;

// typedef ROOT::Math::LorentzVector< ROOT::Math::PxPyPzE4D<float> > LorentzVector;

int main() {
  
  //************************************************************
  //                      Variables                           //
  vector<TString> fileName;

  fileName.push_back("/data/userdata/rclsa/ElectronTrees/Jul22/Ntup_Jul22_fullpt_testing_sample.root");
  fileName.push_back("/data/userdata/rclsa/ElectronTrees/Jul22/Ntup_Jul22_fullpt_testing.root");
  fileName.push_back("/data/userdata/rclsa/ElectronTrees/Jul22/Ntup_Jul22_fullpt_training.root");

  float trkMomentum, trkEta, scRawEnergy;
  int scIsEB;

  float ECALweight, TRKweight;  
  TString dirName = "een_analyzer";
  TString treeName = "ElectronTree";

  //                  END of Variables                        //
  //************************************************************


  // Get resolution file

  
  // Loop over all the Files
  for (int i=0; i < fileName.size(); i++) {

    cout << "Opening " << fileName[i].Data() << endl;

    TFile* currentFile = new TFile(fileName[i],"update");
    TDirectoryFile* directory = (TDirectoryFile*) currentFile->Get(dirName);
    TTree *tree = (TTree*) directory->Get(treeName);

    tree->SetBranchStatus("trkMomentum", 1);
    tree->SetBranchAddress("trkMomentum", &trkMomentum);
    tree->SetBranchStatus("trkEta", 1);
    tree->SetBranchAddress("trkEta", &trkEta);
    tree->SetBranchStatus("scRawEnergy", 1);
    tree->SetBranchAddress("scRawEnergy", &scRawEnergy);
    tree->SetBranchStatus("scIsEB", 1);
    tree->SetBranchAddress("scIsEB", &scIsEB);

    TBranch* br1 = tree->Branch("ECALweight", &ECALweight, "ECALweight/F");
    TBranch* br2 = tree->Branch("TRKweight", &TRKweight, "TRKweight/F");
    			   
    // Loop over all the entries, and add the new branch
    Int_t numEntries = (Int_t)tree->GetEntries();
    for (Int_t j=0; j<numEntries; j++) {

      tree->GetEntry(j);

      if (scIsEB) {
	ECALweight = 1./( 0.05*scRawEnergy+0.35 );
	TRKweight = 1./( 0.002*trkMomentum*trkMomentum*TMath::Sqrt(trkMomentum/TMath::CosH(trkEta)) +
			 0.00007*trkMomentum*trkMomentum*trkMomentum/TMath::CosH(trkEta) +
			 0.001*trkMomentum*trkMomentum*TMath::Log(0.002*trkMomentum/TMath::CosH(trkEta)) );
      } else {
	ECALweight = 1./( 0.03*scRawEnergy*scRawEnergy/(1+0.07*scRawEnergy) + 0.05*scRawEnergy*scRawEnergy*TMath::Exp(-0.04*scRawEnergy) );
	TRKweight = 1./( 0.02*trkMomentum*trkMomentum*TMath::Sqrt(trkMomentum/TMath::CosH(trkEta)) +
			 0.00006*trkMomentum*trkMomentum*trkMomentum*TMath::Log(0.0000003*trkMomentum/TMath::CosH(trkEta))/TMath::CosH(trkEta) );
      }
      
      br1->Fill();
      br2->Fill();
      

    }

    directory->cd();
    tree->Write("", TObject::kOverwrite); // save new version only
    currentFile->Close();
    cout << "...closed file." << endl;
  }
}
