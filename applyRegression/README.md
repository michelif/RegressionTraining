To apply regression to ntuples and create a root file:

./applyRegression.exe -p /mnt/t3nfs01/data01/shome/tklijnsm/EGMregression/Config_Oct26_photon_EB_ECALonly_NI3000.config -b /mnt/t3nfs01/data01/shome/tklijnsm/EGMregression/Config_Oct26_photon_EB_ECALonly_NI3000_results.root -e /mnt/t3nfs01/data01/shome/tklijnsm/EGMregression/Config_Oct27_photon_EE_ECALonly_NI3000_results.root  -t root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/tklijnsm/oldRegressionNtuples/Ntup_10Nov_Photon_1.root  -o ntuples_NN/Ntup_10Nov_Photon_test_1_EB_training.root -i 1

-i 1 if you want to create the training file

-i 0 if you want to create the testing file


-----------------

To convert the root output file into hd5:

python convertRootToHd5.py