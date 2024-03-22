import numpy as np
import sys
import os
from os.path import join, exists
from os import makedirs, mkdir
import h5py
import copy
import pickle

import argparse

parser = argparse.ArgumentParser()

parser.add_argument('mode', type=str,
            help="train val test")

args = parser.parse_args()

print(" ### START convert {} ### ".format(args.mode))

def make_empty_dict_of_file(filepath):
    fgroup, h5f = get_atlas_h5group(filepath)
    ed = {k : np.empty(tuple([0] + list(v.shape[1:]))) for k,v in fgroup.items()}
    ed["y"] = np.empty((0,))
    h5f.close()
    return ed

def get_data_dict_from_h5group(h5group):
    d = {}
    for k,v in h5group.items():
        d[k] = v[:]
    return d


def get_atlas_h5group(filepath, key="all_events"):
    h5f = h5py.File(filepath)
    fgroup = h5f[key]
    return fgroup, h5f

def concat_two_dicts(base,addition):
    for k,v in addition.items():
        if len(v.shape) == 1:
            base[k] = np.hstack((base[k], addition[k]))
        else:
            base[k] = np.vstack((base[k], addition[k]))
    return base

def make_new_file(dic, new_fpath):
    newf = h5py.File(new_fpath)
    newg = newf.create_group("all_events")
    for k,v in dic.items():
        newg.create_dataset(name=k, data=v, compression="gzip", compression_opts=9)
    newf.close()


def merge_files(dirpath, new_fpath):
    files = [join(dirpath,f) for f in os.listdir(dirpath)]
    base = make_empty_dict_of_file(files[0])
    for fpath in files:
        print(fpath)
        fgroup, h5f = get_atlas_h5group(fpath)
        d = get_data_dict_from_h5group(fgroup)
        base = concat_two_dicts(base,d)
        h5f.close()
    print("making new file...")
    make_new_file(base, new_fpath)
    #return base

## Set train, val or test
source_dir = 'pre_' + args.mode
dest_dir = 'dest_' + args.mode

## Set train, val or test
merged_fpath = join(dest_dir, args.mode + ".h5" )
merge_files(source_dir,merged_fpath)
