import h5py
import numpy as np

samplename=''
data=h5py.File(samplename)
print(list(data["all_events"].keys()))

