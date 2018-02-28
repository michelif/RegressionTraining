import os
import numpy as np
import pandas as pd
import root_pandas as rpd

df = rpd.read_root('ntuples_NN/Ntup_10Nov_Photon_test_1_EB.root','een_analyzer/correction',stop=1500000)

df.head()

df.to_hdf('ntuples_NN/Ntup_10Nov_Photon_test_1_EB.hd5','photonTree',compression=9,complib='bzip2',mode='w',format='table',data_columns=['NtupID'])
