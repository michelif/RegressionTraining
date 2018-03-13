import os
import numpy as np
import pandas as pd
import root_pandas as rpd

name='Ntup_10Nov_Photon_training_allvars.root'

df = rpd.read_root('ntuples_NN/'+name,'een_analyzer/correction')

df.head()

df.to_hdf('ntuples_NN/'+name.replace('.root','.hd5'),'photonTree',compression=9,complib='bzip2',mode='w',format='table',data_columns=['NtupID'])
