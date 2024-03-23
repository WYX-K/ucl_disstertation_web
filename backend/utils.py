import pickle
import sys

import numpy as np
import pandas as pd


def filepath(file_name: str):
    return sys.path[0]+file_name


def read_data(file_name: str):
    data = pd.read_csv(filepath(file_name))
    all_patients = data[data['AreaSequence'] == 1]['SpellID_Anon'].values
    data = data[data['SpellID_Anon'].isin(all_patients)]
    data['StartTime'] = pd.to_datetime(
        data['StartTime'], format='%d/%m/%Y %H:%M')
    data['EndTime'] = pd.to_datetime(data['EndTime'], format='%d/%m/%Y %H:%M')
    return data
