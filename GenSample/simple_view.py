import h5py
import numpy as np

data=h5py.File("test_output.h5")



print("#### Numbered Event branches #####")
print(list(data["event_9"].keys()))
numjet      = data["event_9"]["numJet"]
numbjet     = data["event_9"]["numbJet"]
scalarHT    = data["event_9"]["scalarHT"]
sumFatJetM  = data["event_9"]["sumFatJetM"]

print(numjet)
print(numbjet   )
print(scalarHT  )
print(sumFatJetM)

print(" ")
print(" ")
print("#### all_event branches #####")
print(list(data["all_events"].keys()))

