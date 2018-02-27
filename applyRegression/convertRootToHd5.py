import os
import numpy as np
import pandas as pd
import root_pandas as rpd

df = rpd.read_root('ntuples_NN/Ntup_10Nov_Photon_total.root')

df.head()

df.to_hdf('ntuples_NN/Ntup_10Nov_Photon_total_2.hd5','photonTree',compression=9,complib='bzip2',mode='w',format='table',data_columns=['NtupID'])
