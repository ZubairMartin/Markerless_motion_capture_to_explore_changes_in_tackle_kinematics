import os
import numpy as np
import pandas as pd
from pathlib import Path
import re


def merge_dfs(df1, fname1, df2, fname2, new_fname):
    rename_dataset_dir_for_df(fname1, new_fname, df1)
    rename_dataset_dir_for_df(fname2, new_fname, df2)
    df_new = df1.combine_first(df2)
    return df_new

def rename_dataset_dir_for_df(old_fname, new_fname, df):
    idx = list(df.index)
    for i in range(len(idx)):
        idx[i] = idx[i].replace(old_fname, new_fname)
    df.index = pd.Index(idx)

def replace_dataset_backslash_with_forward(df):
    idx = list(df.index)
    for i in range(len(idx)):
        idx[i] = idx[i].replace("\\", "/")
    df.index = pd.Index(idx)

def get_collected_data_df(dir):
    h5_paths = [os.path.join(dir,f) for f in os.listdir(dir) if f.endswith(".h5") and f.startswith("CollectedData")]
    return pd.read_hdf(h5_paths[0])

def save(df, dir):
    df = df.sort_index()
    df.to_hdf(os.path.join(dir,'CollectedData_UCT.h5'), key='df_with_missing', mode='w')
    df.to_csv(os.path.join(dir,'CollectedData_UCT.csv'))
    print("Saved " + dir)

def merge_datasets(dir1, dir2, dir_new):
    df1 = get_collected_data_df(dir1)
    df2 = get_collected_data_df(dir2)
    fname1 = os.path.basename(dir1)
    fname2 = os.path.basename(dir2)
    fname_new = os.path.basename(dir_new)
    df_new = merge_dfs(df1, fname1, df2, fname2, fname_new)
    return df_new

def delete_dupes(directory, folders):
    """
    Deletes the duplicate frames in a given dataframe. Keeps the first index
    ---
    Parameters:
    ---
        directory: String
            String of the absolute filepath of the labeled-data folder to be altered
        folders: List
            List of Strings containing the names of the folders to be changed
    """
    for folder in folders:
        dir = os.path.join(directory,folder)
        df = get_collected_data_df(dir)
        df = df.sort_index()
        df = df[~df.index.duplicated(keep='first')]
        save(df, dir)

def set_collected_df_folder(df, folder_name):
    idx = list(df.index)
    for i in range(len(idx)):
        old_fname = re.search('labeled-data/(.*)/', idx[i])
        idx[i] = idx[i].replace(old_fname.group(1), folder_name)
    df.index = pd.Index(idx)

if __name__ == "__main__":
    topdir = '/home/zubair/Session8_Set2_tackle1-UCT-2019-11-27/labeled-data/'
    
    """
    for f in fnames:
        if os.path.isdir(os.path.join(dir, f)):
            df = get_collected_data_df(dir)
            df.sort_index()
            print(df)
            save(df, os.path.join(dir, f))
    
    for fname in sorted(os.listdir('./Cheetah-UCT-2019-10-14/labeled-data/')):
        folder = os.path.join('./Cheetah-UCT-2019-10-14/labeled-data/',fname)
        if os.path.isdir(folder):
            df = get_collected_data_df(folder)
            replace_dataset_backslash_with_forward(df)
            save(df, folder)

    for fname in sorted(os.listdir('./Cheetah-UCT-2019-10-14/labeled-data')):
    """
    fname = "10_12_2017JulesFlick11CAM1"
    folder = os.path.join('./Cheetah-UCT-2019-10-14/labeled-data',fname)
    new_fname = "10_12_2017JulesFlick11CAM1"
    new_folder = os.path.join('./Cheetah-UCT-2019-10-14/labeled-data', new_fname)
    if os.path.isdir(folder):
        df = get_collected_data_df(folder)
        set_collected_df_folder(df, new_fname)
        save(df, folder)
        os.rename(folder, new_folder)
    

#README!!

# Typical bugs are:
#1. backslashes instead of forward slashes in paths in CollectedData file
#2. Spaces in names of files - these are autorenamed during creation of dataset and then everything breaks :(
#3. Dots in file names - DLC ignore these and again things break... :'(
