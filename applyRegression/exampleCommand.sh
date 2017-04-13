# TRAINING_NTUP="/afs/cern.ch/work/t/tklijnsm/public/CMSSW_8_0_4/src/NTuples/Ntup_Jul22_fullpt_training.root"
# TESTING_NTUP="/afs/cern.ch/work/t/tklijnsm/public/CMSSW_8_0_4/src/NTuples/Ntup_Jul22_fullpt_testing.root"
# TESTING_SAMPLE_NTUP="/afs/cern.ch/work/t/tklijnsm/public/CMSSW_8_0_4/src/NTuples/Ntup_Jul22_fullpt_testing_sample.root"

# RESULT="../savedResults/UsedForOct28Talk/Config_Oct20_electron_EE_ECALonly_results.root"

# python applyRegressionWrapper.py \
#     --config ../python/Config_Oct20_electron_EE_ECALonly.config \
#     --result "$RESULT" \
#     --ntup   "$TESTING_SAMPLE_NTUP" \
#     --batch

# python applyRegressionWrapper.py \
#     --config ../python/Config_Oct20_electron_EE_ECALonly.config \
#     --result "$RESULT" \
#     --ntup   "$TRAINING_NTUP" \
#     --keep \
#     --batch

# python applyRegressionWrapper.py \
#     --config ../python/Config_Oct20_electron_EE_ECALonly.config \
#     --result "$RESULT" \
#     --ntup   "$TESTING_NTUP" \
#     --keep \
#     --batch


# Remade with run and lumi numers included

# TRAINING_NTUP="/afs/cern.ch/work/t/tklijnsm/public/CMSSW_8_0_4/src/NTuples/Ntup_Jul22_fullpt_training.root"
# TESTING_NTUP="/afs/cern.ch/work/t/tklijnsm/public/CMSSW_8_0_4/src/NTuples/Ntup_Jul22_fullpt_testing.root"
# TESTING_SAMPLE_NTUP="/afs/cern.ch/work/t/tklijnsm/public/CMSSW_8_0_4/src/NTuples/Ntup_Jul22_fullpt_testing_sample.root"

# RESULT="../savedResults/UsedForOct28Talk/Config_Oct20_electron_EB_ECALonly_results.root"

# python applyRegressionWrapper.py \
#     --config ../savedResults/UsedForOct28Talk/Configs/Config_Oct20_electron_EB_ECALonly.config \
#     --result "$RESULT" \
#     --ntup   "$TESTING_SAMPLE_NTUP" \
#     --out "Ntup_Nov04_runLumi.root"
#     # --batch

#     


# End of november trkMomResolved run

python applyRegressionWrapper.py \
    --config ../savedResults/trkMomIssueResolved/usedConfigs/Config_Nov25_electron_EB.config \
    --result ../savedResults/trkMomIssueResolved/Config_Nov25_electron_EB_results.root \
    --ntup /afs/cern.ch/work/r/rcoelhol/public/CMSSW_8_0_12/src/NTuples/Ntup_10Nov_ElectronPhoton.root \
    --batch

python applyRegressionWrapper.py \
    --config ../savedResults/trkMomIssueResolved/usedConfigs/Config_Nov25_electron_EE.config \
    --result ../savedResults/trkMomIssueResolved/Config_Nov25_electron_EE_results.root \
    --ntup /afs/cern.ch/work/r/rcoelhol/public/CMSSW_8_0_12/src/NTuples/Ntup_10Nov_ElectronPhoton.root \
    --keep \
    --batch