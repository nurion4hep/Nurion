import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
from ROOT import *
from root_numpy import root2array, tree2array
from root_numpy import testdata
from IPython.display import display
import h5py
import numpy as np

## --Conver Ntuple to Pandas Dataframe
infile      = TFile.Open('cms_hepcnn_test.root')
file_tree   = infile.Get('Events')
data_arr    = tree2array(file_tree)
data_df     = pd.DataFrame(data_arr)

brNames = ["run", "event", "weight",
           "MET_pt",
           "hTrck_pt", "hEcal_pt", "hHcal_pt",
           "hTrck_n", "hEcal_n", "hHcal_n"]

display(data_df)

with h5py.File('out.h5', 'w') as fout:
    dt = h5py.special_dtype(vlen=np.float32)
    g = fout.create_group("Events")
    for brName in brNames:
        g.create_dataset(brName, dtype=dt,data=data_arr[brName],chunks=True,compression='gzip', compression_opts=9)
