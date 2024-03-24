
import datetime

import joblib
import numpy as np
import torch

from utils import *
from model import LSTM

import json
from django.http import HttpResponse

import pickle
import pandas as pd
from collections import defaultdict


def sankey(request):

    data = read_data('AE_Visit_example5k.csv')

    # Find all patients that have appeared
    all_patients = data[data['AreaSequence'] == 1]['SpellID_Anon'].values

    # Determine the maximum time node
    max_time_point = max(data[data['SpellID_Anon'].isin(
        all_patients)].groupby('SpellID_Anon').size()) + 2

    # Generate an initial status for each patient at each time point
    patient_time_status = {patient: {i: str(
        i) + " Not Admitted" for i in range(1, max_time_point + 1)} for patient in all_patients}

    patient_data = {patient: data[data['SpellID_Anon'] == patient].sort_values(
        by='StartTime') for patient in all_patients}
    # Iterate through all patients
    for patient, records in patient_data.items():
        for i, record in enumerate(records.iterrows(), start=1):
            if i == 1:
                patient_time_status[patient][i] = str(
                    i) + " " + record[1]['Pathway']
                patient_time_status[patient][i +
                                             1] = str(i+1) + " " + record[1]['CurrentArea']
            else:
                patient_time_status[patient][i +
                                             1] = str(i+1) + " " + record[1]['CurrentArea']
            if i == len(records):
                final_status = "DC" if "Discharge" in record[1]['TransferStatus'] else "UCH"
                for j in range(i+2, max_time_point + 1):
                    patient_time_status[patient][j] = str(
                        j) + " " + final_status

    nodes = set()
    links = []

    # Iterate through patients and time points where there are records
    for patient, statuses in patient_time_status.items():
        for i in range(1, max_time_point):
            # Get the current time point's status and the next time point's status
            status_current_time = statuses[i]
            status_next_time = statuses[i+1]
            # If these statuses have not been added as nodes yet, add them
            nodes.add(status_current_time)
            nodes.add(status_next_time)
            # Add a link from the current time point's status to the next time point's status
            links.append((status_current_time, status_next_time))

    # Create link counts, each link's value is the number of its occurrences
    link_counts = defaultdict(int)
    for source, target in links:
        link_counts[(source, target)] += 1

    # Generate the final list of links
    final_links = [{'source': source, 'target': target, 'value': value}
                   for (source, target), value in link_counts.items()]

    all_areas = set(' '.join(status.split(' ')[
                    1:]) for statuses in patient_time_status.values() for status in statuses.values())
    area_colors = {area: f"hsl({i * (360 // len(all_areas))
                                }, 50%, 60%)" for i, area in enumerate(all_areas)}

    temp_data = {
        'data': [{'name': node, 'itemStyle': {'color': area_colors[' '.join(node.split(' ')[1:])]}} for node in nodes],
        'links': final_links
    }

    return HttpResponse(json.dumps({"res": temp_data}, ensure_ascii=False), status=200)


def maxPatientArea(request):
    data = read_data('AE_Visit_example5k.csv')
    timeline = pd.DataFrame(columns=['Time', 'Area', 'Change'])

    def create_events(row):
        start_event = pd.DataFrame({'Time': [row['StartTime']], 'Area': [
                                   row['CurrentArea']], 'Change': [1]})
        end_event = pd.DataFrame({'Time': [row['EndTime']], 'Area': [
                                 row['CurrentArea']], 'Change': [-1]})
        return pd.concat([start_event, end_event])

    events = data.apply(create_events, axis=1).tolist()
    timeline = pd.concat(events, ignore_index=True)

    # Convert the data type of the 'Change' column to int
    timeline['Change'] = timeline['Change'].astype(int)

    # Sort by time and area, then calculate the cumulative sum for each area to get the count of people at each time point
    timeline = timeline.sort_values(by=['Time', 'Area'])
    timeline['Count'] = timeline.groupby('Area')['Change'].cumsum()

    # Find all areas
    areas = timeline['Area'].unique()

    temp_list = []

    # temp sort by count
    each_size = 50

    color_interval = 360 // len(areas)
    temp_list = sorted(
        [
            {
                'area_name': area,
                'height': 300,
                'width': timeline[timeline['Area'] == area]['Count'].max() * (each_size**2) / 300,
                'count': str(timeline[timeline['Area'] == area]['Count'].max())
            }
            for area in areas if area != 'OTF'
        ],
        key=lambda x: int(x['count']),
        reverse=True
    )

    temp_width = 0
    for i, temp in enumerate(temp_list):
        temp['color'] = f"hsl({i * color_interval}, 50%, 60%)"
        temp['id'] = []
        if int(temp['count']) >= 10:
            temp['row'] = 1
            temp_width += temp['width'] + 8
        else:
            temp['row'] = 2
            temp['height'] = each_size-13
            temp['width'] = temp_width
        temp['width'] = str(temp['width'])

    return HttpResponse(json.dumps({"res": temp_list}, ensure_ascii=False), status=200)


def dateRange(request):
    data = read_data('AE_Visit_example5k.csv')
    # Get the date range of the data
    date_range = [data['StartTime'].min().strftime(
        '%Y-%m-%d %H:%M:%S'), data['EndTime'].max().strftime('%Y-%m-%d %H:%M:%S')]
    return HttpResponse(json.dumps({"res": date_range}, ensure_ascii=False), status=200)


def patientByTime(request):
    n = int(request.GET.get('n'))

    data = read_data('AE_Visit_example5k.csv')
    time = request.GET.get('start_time')

    time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
    data = data[~((data['CurrentArea'] == 'OTF')
                  & (data['AreaSequence'] == 1))]
    patients = data[(data['StartTime'] <= time+datetime.timedelta(minutes=5*n))
                    & (data['EndTime'] >= time+datetime.timedelta(minutes=5*n))]
    if len(patients) == 0:
        return HttpResponse(json.dumps({"res": []}, ensure_ascii=False), status=200)
    temp_list = []
    patients.apply(lambda x: temp_list.append(
        {
            'id': x['SpellID_Anon'],
            'area_name': x['CurrentArea']
            if x['CurrentArea'] != 'OTF'
            else data[(data['SpellID_Anon'] == x['SpellID_Anon']) & (data['AreaSequence'] == x['AreaSequence']-1)]['CurrentArea'].values[0]
        }), axis=1)
    return HttpResponse(json.dumps({"res": temp_list}, ensure_ascii=False), status=200)


def patientAdmittedProb(request):

    time = pd.to_datetime(request.GET.get('run_time_now'))
    SpellID_Anon = int(request.GET.get('id'))

    data = read_data('AE_Visit_example5k.csv')
    data = data[(data['StartTime'] <= time) & (
        data['SpellID_Anon'] == SpellID_Anon)]

    data['Pathway'] = (data['Pathway'] != 'Walkin').astype('category')

    with open(filepath('dict_area.pkl'), 'rb') as f:
        dict_area = pickle.load(f)
    data['CurrentArea'] = data['CurrentArea'].map(dict_area) - 1

    data = data.sort_values(by='AreaSequence')

    now_area_sequence = data[(data['StartTime'] <= time) & (
        data['EndTime'] >= time)]['AreaSequence'].values[0]
    now_area = data[(data['StartTime'] <= time) & (
        data['EndTime'] >= time)]['CurrentArea'].values[0]

    Pathway = data['Pathway'].values[0]
    FirstTimetoED = pd.Timestamp(
        data[data['AreaSequence'] == 1]['StartTime'].values[0])
    FirstTimetoED_cal = FirstTimetoED.hour + FirstTimetoED.minute/60

    patient = [Pathway, FirstTimetoED_cal]

    current_areas = data['CurrentArea'].values
    start_times = data['StartTime'].values
    total_mins = data['TotalMins'].values

    for i in range(1, now_area_sequence*2+1):
        if i % 2 == 1:
            patient.append(current_areas[i//2])
        else:
            if current_areas[i//2 - 1] == now_area:
                timedelta = time - pd.to_datetime(start_times[i//2-1])
                minutes = timedelta.total_seconds() / 60
                patient.append(minutes)
            else:
                patient.append(total_mins[i//2-1])

    for i in range(4, len(patient), 2):
        if i < len(patient):
            if patient[i] == 0:
                patient[i-1] += patient[i+1]
                del patient[i]
                del patient[i]
        else:
            break

    temp = {
        'id': str(SpellID_Anon),
        'Pathway': 'Walkin' if patient[0] == 0 else 'Ambulance',
        'FirstTimetoED': FirstTimetoED.strftime("%d/%m/%Y %H:%M"),
        'areas': [],
    }
    for i in range(2, len(patient), 2):
        temp['areas'].append({
            'area_name': list(dict_area.keys())[list(dict_area.values()).index(patient[i]+1)],
            'time': str(patient[i+1])
        })
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    patient = np.array(patient)
    region_sequences = torch.IntTensor(patient[2:-1:2]).to(device)
    time_sequences = torch.FloatTensor(
        patient[3::2]/patient[3::2].max() if patient[3::2].max() != 0 else patient[3::2]).to(device)
    other_features = patient[:2]

    extractor = LSTM().to(device)
    extractor.load_state_dict(torch.load(filepath('models/lstm_lgb/lstm.pth')))
    extractor.eval()
    with torch.no_grad():
        region_embed = extractor.region_embedding(region_sequences)
        time_embed = extractor.time_embedding(
            region_sequences) * time_sequences.unsqueeze(-1)
        combined_embed = torch.cat([region_embed, time_embed], dim=-1)
        _, (hidden, _) = extractor.lstm(combined_embed.float())
        extracted_features = hidden.squeeze(0).cpu().numpy()
    extracted_features = np.concatenate(
        [other_features, extracted_features])
    extracted_features = extracted_features.reshape(1, -1)
    classifier = joblib.load(filepath('models/lstm_lgb/lgb.dta'))
    predict_proba = classifier.predict_proba(
        extracted_features)[:, 1][0]
    temp['prob'] = str(predict_proba)
    return HttpResponse(json.dumps({"res": temp}, ensure_ascii=False), status=200)
