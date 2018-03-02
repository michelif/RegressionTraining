To apply regression to ntuples and create a root file:

./applyRegression.exe -p /mnt/t3nfs01/data01/shome/tklijnsm/EGMregression/Config_Oct26_photon_EB_ECALonly_NI3000.config -b /mnt/t3nfs01/data01/shome/tklijnsm/EGMregression/Config_Oct26_photon_EB_ECALonly_NI3000_results.root -e /mnt/t3nfs01/data01/shome/tklijnsm/EGMregression/Config_Oct27_photon_EE_ECALonly_NI3000_results.root  -t root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/tklijnsm/oldRegressionNtuples/Ntup_10Nov_Photon_1.root  -o ntuples_NN/Ntup_10Nov_Photon_test_1_EB_training.root -i 1

-i 1 if you want to create the training file

-i 0 if you want to create the testing file

The output trees have two additional branches:
"correction" and "resolution" which are the result of e/gamma regression

-----------------

To convert the root output file into hd5:

python convertRootToHd5.py

------------------


Full list of variables used:

List of variables:
EB variables
  scRawEnergy
  scEtaWidth
  scPhiWidth
  full5x5_e5x5/scRawEnergy
  hadronicOverEm
  rhoValue
  delEtaSeed
  delPhiSeed
  full5x5_r9
  full5x5_sigmaIetaIeta
  full5x5_sigmaIetaIphi
  full5x5_sigmaIphiIphi
  full5x5_eMax/full5x5_e5x5
  full5x5_e2nd/full5x5_e5x5
  full5x5_eTop/full5x5_e5x5
  full5x5_eBottom/full5x5_e5x5
  full5x5_eLeft/full5x5_e5x5
  full5x5_eRight/full5x5_e5x5
  full5x5_e2x5Max/full5x5_e5x5
  full5x5_e2x5Left/full5x5_e5x5
  full5x5_e2x5Right/full5x5_e5x5
  full5x5_e2x5Top/full5x5_e5x5
  full5x5_e2x5Bottom/full5x5_e5x5
  N_SATURATEDXTALS
  N_ECALClusters
  clusterRawEnergy[0]/scRawEnergy
  clusterRawEnergy[1]/scRawEnergy
  clusterRawEnergy[2]/scRawEnergy
  clusterDPhiToSeed[0]
  clusterDPhiToSeed[1]
  clusterDPhiToSeed[2]
  clusterDEtaToSeed[0]
  clusterDEtaToSeed[1]
  clusterDEtaToSeed[2]
  iEtaCoordinate
  iPhiCoordinate
  iEtaMod5
  iPhiMod2
  iEtaMod20
  iPhiMod20
EE variables
  scRawEnergy
  scEtaWidth
  scPhiWidth
  full5x5_e5x5/scRawEnergy
  hadronicOverEm
  rhoValue
  delEtaSeed
  delPhiSeed
  full5x5_r9
  full5x5_sigmaIetaIeta
  full5x5_sigmaIetaIphi
  full5x5_sigmaIphiIphi
  full5x5_eMax/full5x5_e5x5
  full5x5_e2nd/full5x5_e5x5
  full5x5_eTop/full5x5_e5x5
  full5x5_eBottom/full5x5_e5x5
  full5x5_eLeft/full5x5_e5x5
  full5x5_eRight/full5x5_e5x5
  full5x5_e2x5Max/full5x5_e5x5
  full5x5_e2x5Left/full5x5_e5x5
  full5x5_e2x5Right/full5x5_e5x5
  full5x5_e2x5Top/full5x5_e5x5
  full5x5_e2x5Bottom/full5x5_e5x5
  N_SATURATEDXTALS
  N_ECALClusters
  clusterRawEnergy[0]/scRawEnergy
  clusterRawEnergy[1]/scRawEnergy
  clusterRawEnergy[2]/scRawEnergy
  clusterDPhiToSeed[0]
  clusterDPhiToSeed[1]
  clusterDPhiToSeed[2]
  clusterDEtaToSeed[0]
  clusterDEtaToSeed[1]
  clusterDEtaToSeed[2]
  iXCoordinate
  iYCoordinate
  scPreshowerEnergy/scRawEnergy
  preshowerEnergyPlane1/scRawEnergy
  preshowerEnergyPlane2/scRawEnergy

