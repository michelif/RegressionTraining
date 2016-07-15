# =====================================
# Manage input

if [ $# -eq 0 ] || [ $# -eq 1 ] ; then
    echo "No arguments supplied"
    echo "  argument 1 should be 'photon' or 'electron'"
    echo "  argument 2 should be 'EB' or 'EE'"
    return 1
fi
export PARTICLE="$1"
export REGION="$2"


export TESTRUN="Y"
# export TESTRUN="N"

# =====================================
# Set correct paths to Ntuples

NTUPLEPATH="${CMSSW_BASE}/src/NTuples/"


# =====================================
#### LOW PT RUNS

# export HIGHPT="N"

# ELECTRONNTUP="Ntup_01June_DoubleElectron.root"
# PHOTONNTUP="Ntup_01June_DoublePhoton.root"

# # Small sample for quick iterations (comment out for full set of plots)
# # ELECTRONNTUP="SampleNtup_01June_electrons.root"
# PHOTONNTUP="SampleNtup_15June_photons_lowpt_mediumsized.root"

# PHOTONTRAINING="before05Jun_photonConfig_results.root"
# ELECTRONTRAINING="before05Jun_electronConfig_results.root"


# =====================================
#### HIGH PT RUNS

# export HIGHPT="Y"

# ELECTRONNTUP="Ntup_05June_electrons_LowHighPt.root"

# # New photon sample, contains the old energy variable
# # PHOTONNTUP="Ntup_05June_photons_LowHighPt.root"
# PHOTONNTUP="Ntup_12June_photons_lowhighpt.root"

# # Medium sized samples, full pt spectrum
# # ELECTRONNTUP="SampleNtup_11June_electrons.root"
# # PHOTONNTUP="SampleNtup_11June_photons.root"


# #### Trained up to genPt <= 2 TeV
# ELECTRONTRAINING="pt2TeV_electronConfig_results.root"
# PHOTONTRAININGOUTPUT="pt2TeV_photonConfig_results.root"
# export USE2TEVCUT="Y"

# #### Full pt spectrum
# # ELECTRONTRAINING="FullPt_electronConfig_results.root"
# # PHOTONTRAININGOUTPUT="FullPt_photonConfig_results.root"


# =====================================
#### 25 June runs

# ------------------------------
# Low pt spectrum

# export HIGHPT="N"

# export FLATNTUPLE=$NTUPLEPATH/Ntup_Jun22_lowpt_testing_sample.root

# PHOTONTRAINING="Config_photon_lowpt_Jun25_results.root"
# ELECTRONTRAINING="Config_electron_lowpt_Jun25_results.root"

# Old vars
# PHOTONTRAINING="Config_photon_lowpt_Jun25_OLDVARS_results.root"
# ELECTRONTRAINING="Config_electron_lowpt_Jun25_OLDVARS_results.root"


# ------------------------------
# Full pt spectrum

# If "Y", 1 set of plots is made for 0 - 6500 GeV
export HIGHPT="Y"

# If "Y", a set of plots is made for several pt ranges, up to 6500 GeV
# export USEGLOBALPTBINS="Y"

export FLATNTUPLE=$NTUPLEPATH/Ntup_Jun22_fullpt_testing_sample.root

# PHOTONTRAINING="Config_photon_fullpt_Jun25_results.root"
# ELECTRONTRAINING="Config_electron_fullpt_Jun25_results.root"

# # Old vars
# PHOTONTRAINING="Config_photon_fullpt_Jun25_OLDVARS_results.root"
# ELECTRONTRAINING="Config_electron_fullpt_Jun25_OLDVARS_results.root"

# Training sets by Rafael
# PHOTONTRAINING="Config_photon_Jun30_results.root"
# ELECTRONTRAINING="Config_electron_Jun30_results.root"

# Redone training sets by Rafael
# PHOTONTRAINING="Config_photon_Jul13_results.root"
# ELECTRONTRAINING="Config_electron_Jul13_results.root"

ELECTRONTRAINING="Config_electron_Jul15_results.root"



# =====================================
# Prepare the run

if [ "$PARTICLE" = "electron" ]; then
    # export FLATNTUPLE=$NTUPLEPATH/$ELECTRONNTUP
    export NTUPLETREE="ElectronTree"
    export TRAININGOUTPUT=$ELECTRONTRAINING
elif [ "$PARTICLE" = "photon" ]; then
    # export FLATNTUPLE=$NTUPLEPATH/$PHOTONNTUP
    export NTUPLETREE="PhotonTree"
    export TRAININGOUTPUT=$PHOTONTRAINING
fi


# Make a working directory for the test plots - copy training output in there as well
PLOTDIR="plots_${PARTICLE}_${REGION}"
cd ${CMSSW_BASE}/src/RegressionTrainingCopy
mkdir -p $PLOTDIR
cp $TRAININGOUTPUT $PLOTDIR
export PLOTDIR_FULLPATH=$CMSSW_BASE/src/RegressionTrainingCopy/$PLOTDIR

# TESTMACRO="$CMSSW_BASE/src/HiggsAnalysis/GBRLikelihood/macros/eregtestThomas.C"
# TESTMACRO="$CMSSW_BASE/src/HiggsAnalysis/GBRLikelihood/macros/eregtest_inputbins.C"
# TESTMACRO="$CMSSW_BASE/src/HiggsAnalysis/GBRLikelihood/macros/scale_fitMean_RawCor.C"
TESTMACRO="$CMSSW_BASE/src/HiggsAnalysis/GBRLikelihood/macros/DrawBinPlots.C"


# =====================================
# Execute

echo "Running test macro $TESTMACRO"
echo "  FLATNTUPLE     = $FLATNTUPLE"
echo "  NTUPLETREE     = $NTUPLETREE"
echo "  TRAININGOUTPUT = $TRAININGOUTPUT"
echo "  PLOTDIR        = $PLOTDIR"
echo

pushd $CMSSW_BASE/src/HiggsAnalysis/GBRLikelihood/macros/
root -b -l -q $TESTMACRO
popd
# mkdir -p plots
# mv *.eps plots/
# mv *.png plots/