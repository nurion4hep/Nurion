import h5py
import numpy as np

data=h5py.File("test_output.h5")

print("#### all_event branches #####")
print(list(data["all_events"].keys()))

