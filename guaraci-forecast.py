#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Guaraci Forecast 0.2

This script deploys space weather forecast models designed by the Guaraci framework: https://github.com/tiagocinto/guaraci-toolkit. It's optimized for Python 2.7 and unix-based operating systems.

Author: Tiago Cinto
Version: 0.2
Email: tiago.cinto@pos.ft.unicamp.br
"""
from __future__ import division

def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

from datetime import datetime
from urllib2 import urlopen #, URLError, HTTPError

import traceback
import schedule
import time
import pandas as pd
import numpy as np
import xml.etree.ElementTree as et
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from sklearn.ensemble import (AdaBoostClassifier, RandomForestClassifier, GradientBoostingClassifier)

from imblearn.over_sampling import (RandomOverSampler, ADASYN, SMOTE)

from imblearn.under_sampling import (AllKNN, 
                                    EditedNearestNeighbours,
                                    RepeatedEditedNearestNeighbours,
                                    OneSidedSelection, 
                                    ClusterCentroids,
                                    RandomUnderSampler,
                                    NeighbourhoodCleaningRule,
                                    CondensedNearestNeighbour,
                                    NearMiss,
                                    InstanceHardnessThreshold)

from imblearn.combine import (SMOTEENN, SMOTETomek)

def send_mail(e):
    """
    This function sends an email for notifying a system crash.
    """
    msg = MIMEMultipart()
    msg['From'] = CRASH_LOG_FROM_ADDRESS
    msg['To'] = CRASH_LOG_TO_ADDRESS
    msg['Subject'] = "sw-forecast crash!"
    message = e
    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP(SMTP_SERVER)
    password = SMTP_PASSWORD
    server.starttls()
    server.login(msg['From'], password)
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()


def print_log_msg(msg):
    """
    This function formats and prints on screen and file any log message.
    """
    print(msg)
    msg = format_log_message(msg)
    append_text_to_file(file_name=LOG_PATH, text=msg + "\n")


def append_text_to_file(file_name, text):
    """
    This function opens an archive file and appends some content.
    """
    f = open(file_name,'a')
    f.write(text)
    f.close()


def format_log_message(msg):
    """
    This function formats a log msg. This is done to represent time the log entry was created.
    """
    return str('%s | %s' % (datetime.now(), msg))


def safe_division(n, d):
    """
    This function prevents a division by zero exception.
    """
    return n / d if d else 0


def z_score_calculation(x, mu, sigma):
    """
    This function computes the standard z-score of an input feature.
    """
    return safe_division(x - mu, sigma)


def download_file(url, save_path):
    """
    This function downloads a specified file. Used to download DSD and SRS from SWPC's repositories.
    """
    print_log_msg('Downloading: ' + url + '...')
    f = urlopen(url)
    with open(save_path, 'wb') as local_file:
        local_file.write(f.read())
        print_log_msg('Done: ' + url + '.')


def compute_xray_background_flux(label):
    """
    This function computes the xray background flux based on the SWPC xray peak flux scale.
    """
    class_name = label[:1]
    intensity = label[1:4]
    if class_name == 'A':
        if intensity != '0.0' and intensity != '0.00': xray_background_flux = float(intensity) * A_CLASS_PEAK_FLUX
        else: xray_background_flux = A_CLASS_PEAK_FLUX
    elif class_name == 'B': xray_background_flux = float(intensity) * B_CLASS_PEAK_FLUX
    elif class_name == 'C': xray_background_flux = float(intensity) * C_CLASS_PEAK_FLUX
    elif class_name == 'M': xray_background_flux = float(intensity) * M_CLASS_PEAK_FLUX
    elif class_name == 'X': xray_background_flux = float(intensity) * X_CLASS_PEAK_FLUX
    else: xray_background_flux = A_CLASS_PEAK_FLUX
    return xray_background_flux
    


def count_file_length(file_name):
    """
    This function counts the number of lines in a file. Used for selecting only the last 5 entries of daily solar data.
    """
    i = 0
    f = open(file_name, 'r')
    for x in f:
        i = i + 1
    f.close()
    return i


def contains(file_name, string):
    """
    This function opens an SRS file and explores its content to look for a specific magnetic class.
    """
    f = open(file_name, 'r')
    for line in f:
        df_line = line.split()
        for elem in df_line:
            if elem.lower() == string.lower():
                f.close()
                return 1
    f.close()
    return 0
    
    
def count_class(file_name, string):
    """
    This function opens an SRS file and explores its content to count specific classes.
    """
    i = 0
    f = open(file_name, 'r')
    for line in f:
        df_line = line.split()
        for elem in df_line:
            if elem.lower() == string.lower():
                i = i + 1
    f.close()
    return i
            

def is_number(string):
    """
    Check if string is a number.
    """
    try:
        float(string)
        return 1
    except ValueError:
        return 0


def extract_attribute(line, atr_idx):
    pd_line = pd.DataFrame([line.split()])
    return pd_line.iloc[0, atr_idx]


def assemble_dataset():
    """
    This function assembles the dataset to be used for forecasting flares based on data collected from DSD and SRS.
    Will compose a data frame with the following features:
    1- year
    2- month
    3- day
    4- radio flux
    5- sunspot number
    6- sunspot area
    7- xray background flux
    8- daily mag type wmfr
    9- daily z component wmfr
    10- daily p component wmfr
    11- daily c component wmfr
    """
    try:
        dsd_path = TEMP_PATH + DSD_FILE_NAME
        download_file(url=DSD_URL, save_path=TEMP_PATH + DSD_FILE_NAME)
        df = np.zeros(shape=[5, 11])
        df = pd.DataFrame(df, columns=COL_NAMES_DATAFRAME)
        i = j = 0
        file_length = count_file_length(dsd_path)
        dsd_file = open(dsd_path, 'r')
        for line in dsd_file:
            i = i + 1
            if i > file_length - 5:
                z_component_wmfr = p_component_wmfr = c_component_wmfr = mag_type_wmfr = 0
                for atr, idx, tp, sigma, mu in iter(INPUT_ATTRS):
                    if tp == 'id':
                        var = extract_attribute(line, idx)
                        df.loc[j, atr] = var   
                srs_file_name = str('%s%s%sSRS.txt' % (df.loc[j, 'year'], df.loc[j, 'month'], df.loc[j, 'day']))
                download_file(url=SRS_URL + srs_file_name, save_path=TEMP_PATH + srs_file_name)
                for atr, idx, tp, mu, sigma in iter(INPUT_ATTRS):
                    if tp == 'reg':
                        if atr == 'xray_background_flux':
                            var = extract_attribute(line, idx)
                            var = round(z_score_calculation(compute_xray_background_flux(var), mu, sigma), 6)
                            df.loc[j, atr] = var
                        elif atr == 'mag_type_wmfr':
                            for cl, wmfr in iter(MAG_TYPES): 
                                 qt = count_class(file_name=TEMP_PATH + srs_file_name, string=cl)
                                 mag_type_wmfr = mag_type_wmfr + qt * wmfr                        
                            df.loc[j, atr] = round(z_score_calculation(mag_type_wmfr, mu, sigma), 6)
                        elif atr == 'z_component_wmfr':
                            for cl in ZPC_CLASSES:
                                qt = count_class(file_name=TEMP_PATH + srs_file_name, string=cl)
                                if qt != 0:
                                    cl_split = list(cl)
                                    for cnt, wmfr in iter(Z_COMPONENTS): 
                                        if cnt == cl_split[0].lower():
                                            z_component_wmfr = z_component_wmfr + qt * wmfr
                                            break
                            df.loc[j, atr] = round(z_score_calculation(z_component_wmfr, mu, sigma), 6)
                        elif atr == 'p_component_wmfr':
                            for cl in ZPC_CLASSES:
                                qt = count_class(file_name=TEMP_PATH + srs_file_name, string=cl)
                                if qt != 0:
                                    cl_split = list(cl)
                                    for cnt, wmfr in iter(P_COMPONENTS): 
                                        if cnt == cl_split[1].lower():
                                            p_component_wmfr = p_component_wmfr + qt * wmfr
                                            break
                            df.loc[j, atr] = round(z_score_calculation(p_component_wmfr, mu, sigma), 6)
                        elif atr == 'c_component_wmfr':
                            for cl in ZPC_CLASSES:
                                qt = count_class(file_name=TEMP_PATH + srs_file_name, string=cl)
                                if qt != 0:
                                    cl_split = list(cl)
                                    for cnt, wmfr in iter(C_COMPONENTS): 
                                        if cnt == cl_split[2].lower():
                                            c_component_wmfr = c_component_wmfr + qt * wmfr
                                            break
                            df.loc[j, atr] = round(z_score_calculation(c_component_wmfr, mu, sigma), 6)
                        else: 
                            var = extract_attribute(line, idx)
                            var = round(z_score_calculation(float(var), mu, sigma), 6)
                            df.loc[j, atr] = var
                j = j + 1
        dsd_file.close()
        model_input = reframe_data(df, col_names=COL_NAMES_MODEL_INPUT)
        model_input.to_csv(WORK_PATH + 'model_input.csv')
        df_view = df.copy()
        df_view.columns = COL_NAMES_DATAFRAME_VIEW
        df_view.to_csv(WORK_PATH + 'dataframe.csv')     
        return model_input, df
    except Exception, e:
        print_log_msg('%s' % e)
        if SEND_CRASH_LOG: send_mail('%s' % traceback.format_exc()) 
        return pd.DataFrame([]), pd.DataFrame([])


def reframe_data(data_in, col_names):
    """
    This function reframes data so that it will be adjusted in the format expected by the predictor model.
    Will only work for a delta t of 5 days. It is flexible regarding the number of input features only, not the length of the sliding time window.
    """
    rows_data_in, cols_data_in = data_in.shape
    np_data = np.empty(shape=[1, cols_data_in * 5])
    df = pd.DataFrame(np_data)
    df_n_col = 0
    for j_data_in in range(0, cols_data_in):
        for i_data_in in range(0, rows_data_in):
            df.iloc[0, df_n_col] = data_in.iloc[i_data_in, j_data_in]
            df_n_col = df_n_col + 1
    df.columns = col_names
    return df


def resample_data(predictors, target, df_data, method):
    """
    This function resamples training datasets prior to training models.
    """
    if method=='adasyn':
        util = ADASYN()
    elif method=='random-over-sampler':
        util = RandomOverSampler()
    elif method=='smote':
        util = SMOTE(kind='borderline2')
    elif method=='smote-tomek':
        util = SMOTETomek()
    elif method=='smote-enn':
        util = SMOTEENN()
    elif method=='edited-nn':
        util = EditedNearestNeighbours()
    elif method=='repeated-edited-nn':
        util = RepeatedEditedNearestNeighbours()
    elif method=='all-knn':
        util = AllKNN()
    elif method=='one-sided-selection':
        util = OneSidedSelection()
    elif method=='cluster-centroids':
        util = ClusterCentroids()
    elif method=='random-under-sampler':
        util = RandomUnderSampler()
    elif method=='neighbourhood-cleaning-rule':
        util = NeighbourhoodCleaningRule()
    elif method=='condensed-nearest-neighbour':
        util = CondensedNearestNeighbour()
    elif method=='near-miss':
        util = NearMiss(version=1)
    elif method=='instance-hardness-threshold':
        util = InstanceHardnessThreshold()
    
    x_resampled, y_resampled = util.fit_sample(df_data[predictors], df_data[target])
    x_resampled = pd.DataFrame(x_resampled, columns=predictors)
    y_resampled = pd.DataFrame(y_resampled, columns=[target])
    return x_resampled, y_resampled


def predict_proba(alg, input_data):
    """
    This function calculates the forecasting probabilities of a learning algorithm
    """
    probabilities = alg.predict_proba(input_data)
    return probabilities[:,0], probabilities[:,1]


def fit_alg(alg, x_data, y_data):
    """
    This function fits a learning algorithm.
    """
    alg.fit(x_data, y_data)


def load_training_data(training_data_files):
    """
    This function loads training data of a model for different time horizons.
    """
    dfs = [pd.read_csv(DATA_PATH + file_name, sep=';', decimal=',') for file_name in training_data_files]
    for df, nam in zip(dfs, training_data_files):
        df['ft'] = nam[len(nam)-7:len(nam)-4]
    return dfs



def threshold_predict(y_score, t):
    """
    This function adjusts class predictions based on the prediction threshold (t).
    Will only work for binary classification problems.
    """
    return 'Yes' if y_score >= t else 'No'


def reset_module_view(modules):
    """
    This function resets module's view data.
    """
    view_data = pd.DataFrame([])
    for module in modules:
        view_data[module + '_data_processing_time'] = ['NA']
        view_data[module + '_t1d_no_proba'] = ['NA']
        view_data[module + '_t1d_yes_proba'] = ['NA']
        view_data[module + '_t2d_no_proba'] = ['NA']
        view_data[module + '_t2d_yes_proba'] = ['NA']
        view_data[module + '_t3d_no_proba'] = ['NA']
        view_data[module + '_t3d_yes_proba'] = ['NA']
        view_data[module + '_t1d_prediction'] = ['NA']
        view_data[module + '_t2d_prediction'] = ['NA']
        view_data[module + '_t3d_prediction'] = ['NA']
    return view_data


def write_view_data(view_data):
    """
    This function writes to disk a view data object.
    """
    xml_root_node = et.Element("sw-forecast")
    xml_view_node = et.SubElement(xml_root_node, "view")
    for column in view_data:
        et.SubElement(xml_view_node, column).text = view_data.loc[0, column]
    tree = et.ElementTree(xml_root_node)
    tree.write(WORK_PATH + VIEW_FILE_NAME)


def fit_model(df, ft, nmbr, features, model):
    """
    This function pre-process and fits a model
    """
    print_log_msg('Fitting mod%s/%s...' % (nmbr, ft))
    df[features['%s_target_feature' % ft]] = df[features['%s_target_feature' % ft]].map(lambda x: '%.0f' % float(x))
    fit_alg(alg=model['%s_model' % ft], x_data=df[features['%s_features_set' % ft]], y_data=df[features['%s_target_feature' % ft]])
    print_log_msg('mod%s/%s fit sucessfully.' % (nmbr, ft))


def predict_probabilities(df, ft, nmbr, features, model, input_data):
    """
    This function calculates the forecasting probabilities of a model over the assembled input data.
    """
    print_log_msg('Calculating flare probabilities with mod%s/%s...' % (nmbr, ft))
    no_proba, yes_proba = predict_proba(alg=model['%s_model' % ft], input_data=input_data[features['%s_features_set' % ft]])
    print_log_msg('mod%s/%s: 0/%.2f x 1/%.2f' % (nmbr, ft, no_proba, yes_proba))
    return no_proba, yes_proba


def forecast(yes_proba, nmbr, ft, model):
    """
    This function makes predictions based on the yes probability and the provided cutt-off point
    """
    print_log_msg('Forecasting with mod%s/%s...' % (nmbr, ft))
    forecast = '%s' % threshold_predict(float(yes_proba), model['%s_model_t' % ft])
    print_log_msg('mod%s/%s: %s' % (nmbr, ft, forecast))
    return forecast


def exec_module(nmbr, training_data_files, graphical_input_file, features, model, input_data):
    """
    This function sets up a forecasting module and executes it.
    """
    try:
        view = pd.DataFrame([])
        data_processing_time = str(datetime.now().strftime("%Y-%m-%d %H:%M"))
        view['mod%d_data_processing_time' % nmbr] = [data_processing_time]
        probabilities = pd.DataFrame([])
        forecasts = pd.DataFrame([])
        print_log_msg('Loading dataset to train models of mod%d...' % nmbr)
        dfs = load_training_data(training_data_files)
        for df in dfs:
            if df[df.ft == 't1d'].empty != True: ft = 't1d'
            elif df[df.ft == 't2d'].empty != True: ft = 't2d'
            elif df[df.ft == 't3d'].empty != True: ft = 't3d'
            if model['%s_model_resampling_method' % ft] != None:
                x_resampled, y_resampled = resample_data(
                                                features['%s_features_set' % ft], 
                                                features['%s_target_feature' % ft], 
                                                df, 
                                                model['%s_model_resampling_method' % ft]
                                            )
                df = pd.concat([x_resampled, y_resampled], axis=1)
            fit_model(df, ft, nmbr, features, model)
            no_proba, yes_proba = predict_probabilities(df, ft, nmbr, features, model, input_data)
            probabilities['mod%d_%s' % (nmbr, ft)] = ['%.2f' % no_proba, '%.2f' % yes_proba]
            forecasts['mod%d_%s' % (nmbr, ft)] = [forecast(yes_proba, nmbr, ft, model)]
            view[('mod%d_%s_no_proba' % (nmbr, ft))] = [probabilities.loc[0, ('mod%d_%s' % (nmbr, ft))]]
            view[('mod%d_%s_yes_proba' % (nmbr, ft))] = [probabilities.loc[1, ('mod%d_%s' % (nmbr, ft))]]            
            view[('mod%d_%s_prediction' % (nmbr, ft))] = [forecasts.loc[0, ('mod%d_%s' % (nmbr, ft))]]
            if ft == 't1d': append_text_to_file(WORK_PATH + graphical_input_file, '%s,%.2f\n' % (data_processing_time, yes_proba))
        return view
    except Exception, e:
        print_log_msg('%s' % e)
        if SEND_CRASH_LOG: send_mail('%s' % traceback.format_exc()) 
        return reset_module_view(['mod%d' % nmbr])

def main():
    """
    Main controller.
    """
    try:
        view1 = pd.DataFrame([])
        print_log_msg('Initializing new execution.')
        print_log_msg('Assembling input data...')
        input_data, dataframe = assemble_dataset()
        view1['t_instant'] = ['%s-%s-%s' % (dataframe.loc[4,'year'], dataframe.loc[4,'month'], dataframe.loc[4,'day'])]
        view2 = exec_module(1, MOD1_TRAINING_DATA_FILES, MOD1_GRAPHICAL_INPUT_FILE, MOD1_FEATURES, MOD1, input_data)
        view3 = exec_module(2, MOD2_TRAINING_DATA_FILES, MOD2_GRAPHICAL_INPUT_FILE, MOD2_FEATURES, MOD2, input_data)
        view_data = pd.concat([view1, view2, view3], axis=1)
        write_view_data(view_data)
    except Exception, e:
        print_log_msg('%s' % e)
        if SEND_CRASH_LOG: send_mail('%s' % traceback.format_exc()) 
    
    
"""
ARs' Zpc classes
"""
ZPC_CLASSES = [
    'AXX', 'BXO', 'BXI', 'HRX', 'CRO',
    'CRI', 'HAX', 'CAO', 'CAI', 'HSX',
    'CSO', 'CSI', 'DRO', 'ERO', 'FRO',
    'DRI', 'ERI', 'FRI', 'DAO', 'EAO',
    'FAO', 'DAI', 'EAI', 'FAI', 'DSO',
    'ESO', 'FSO', 'DSI', 'ESI', 'FSI',
    'DAC', 'EAC', 'FAC', 'DSC', 'ESC',
    'FSC', 'HKX', 'CKO', 'CKI', 'HHX',
    'CHO', 'CHI', 'DKO', 'EKO', 'FKO',
    'DKI', 'EKI', 'FKI', 'DHO', 'EHO',
    'FHO', 'DHI', 'EHI', 'FHI', 'DKC',
    'EKC', 'FKC', 'DHC', 'EHC', 'FHC'
]
		    

"""
ARs' magnetic types and their corresponding weighted mean flare rates
"""
MAG_TYPES = [
    ['Alpha', 5.755425],
    ['Beta', 6.114663],
    ['Beta-Gamma', 7.184164],
    ['Beta-Gamma-Delta', 16.932790],
    ['Beta-Delta', 10.962962],
    ['Gamma-Delta', 17],
    ['Gamma', 8.5],
]
    

"""
ARs' z components and their corresponding weighted mean flare rates
"""
Z_COMPONENTS = [
    ['a', 5.281121],
    ['b', 5.538421],
    ['c', 6.050772],
    ['d', 6.642577],
    ['e', 8.180760],
    ['f', 12.24156],
    ['h', 5.969069],
]


"""
ARs' p components and their corresponding weighted mean flare rates
"""
P_COMPONENTS = [
    ['a', 6.542995],
    ['h', 5.566455],
    ['k', 11.02844],
    ['r', 5.946721],
    ['s', 6.018621],
    ['x', 5.421434],
]


"""
ARs' c components and their corresponding weighted mean flare rates
"""
C_COMPONENTS = [
    ['c', 12.44513],
    ['i', 7.070465],
    ['o', 6.191639],
    ['x', 5.749823],  
]


"""
Parameters for converting xray backgound flux data
"""
A_CLASS_PEAK_FLUX = 0.00000001
B_CLASS_PEAK_FLUX = 0.0000001
C_CLASS_PEAK_FLUX = 0.000001
M_CLASS_PEAK_FLUX = 0.00001
X_CLASS_PEAK_FLUX = 0.0001


"""
Input features: feature, idx, type, mu, sigma
"""
INPUT_ATTRS = [
    ['year', 0, 'id', -1, -1],
    ['month', 1, 'id', -1, -1],
    ['day', 2, 'id', -1, -1],
    ['radio_flux', 3, 'reg', 114.97, 42.04],
    ['sunspot_number', 4, 'reg', 78.04, 66.45],
    ['sunspot_area', 5, 'reg', 530.42, 581.80],
    ['xray_background_flux', 8, 'reg', 0.000000422486, 0.0000006999466],
    ['z_component_wmfr', -1, 'reg', 28.875546, 23.376342],
    ['p_component_wmfr', -1, 'reg', 28.875546, 23.320936],
    ['c_component_wmfr', -1, 'reg', 28.875546, 22.963968],
    ['mag_type_wmfr', -1, 'reg', 28.866666, 23.217382]
]


"""
Parameters for configuring system's paths
"""
WORK_PATH = '//home//ubuntu//www//guaraci-forecast//'
TEMP_PATH = WORK_PATH + 'temp//'
DATA_PATH = WORK_PATH + 'data//'
LOG_PATH = WORK_PATH + 'log'
VIEW_FILE_NAME = 'view.xml'

MOD1_GRAPHICAL_INPUT_FILE = 'c-m-x-flare-forecasts-graphical-input.csv'
MOD2_GRAPHICAL_INPUT_FILE = 'm-x-flare-forecasts-graphical-input.csv'


"""
URLs for downloading data files
"""
DSD_FILE_NAME = 'DSD.txt'
DSD_URL = 'ftp://ftp.swpc.noaa.gov/pub/indices/' + DSD_FILE_NAME
SRS_URL = 'ftp://ftp.swpc.noaa.gov/pub/warehouse/2020/SRS/'


"""
Parameters for setting up system crash log
"""
SMTP_PASSWORD = "QcWtIBkZgdxyLvaq"
CRASH_LOG_FROM_ADDRESS = "tiago.cinto@gmail.com"
CRASH_LOG_TO_ADDRESS = "tiago.cinto@gmail.com"
SMTP_SERVER = 'smtp-relay.sendinblue.com:587'
SEND_CRASH_LOG = True

"""
Parameters for scheduling system execution
"""
SCHEDULED_EXECUTION = True
EXECUTION_HOUR = '01:00'


"""
Models' training data files. Files must be of csv type and have their forecasting horizons specified prior to the csv extension.
"""
# MOD1
MOD1_TRAINING_DATA_FILES = [
    'mod1.data.t1d.csv',
    'mod1.data.t2d.csv',
    'mod1.data.t3d.csv'
]
# MOD2
MOD2_TRAINING_DATA_FILES = [
    'mod2.data.t1d.csv',
    'mod2.data.t2d.csv',
    'mod2.data.t3d.csv'
]


"""
Dict containing models' learning algorithms and their cut-off points for each time horizon
"""
# MOD1
MOD1 = {
    't1d_model': RandomForestClassifier(
                    n_estimators=300,
                    min_samples_split=100,
                    min_samples_leaf=40,
                    max_depth=15,
                    max_features=4,
                    min_impurity_split=0.001,
                    class_weight={'0':1,'1':0.78},
                    random_state=10
                ),
    't1d_model_t':0.45,
    't1d_model_resampling_method': None,
    't2d_model': RandomForestClassifier(
                    n_estimators=300,
                    min_samples_split=50,
                    min_samples_leaf=90,
                    max_depth=8,
                    max_features=4,
                    min_impurity_split=1e-07,
                    class_weight={'0':1,'1':0.55},
                    random_state=10
                ),
    't2d_model_t': 0.40,
    't2d_model_resampling_method': None,
    't3d_model': AdaBoostClassifier(DecisionTreeClassifier(
                                        min_samples_split=800,
                                        min_samples_leaf=75,
                                        max_depth=13,
                                        max_features=2,
                                        class_weight={'0':1,'1':0.45},
                                        random_state=10
                                    ),
                    n_estimators=350,
                    learning_rate=0.01,
                    random_state=10
                ),
    't3d_model_t': 0.48,
    't3d_model_resampling_method': None
}
# MOD2
MOD2 = {
    't1d_model': GradientBoostingClassifier(
                    n_estimators=250,
                    learning_rate=0.01,
                    min_samples_split=200,
                    min_samples_leaf=40,
                    max_depth=9,
                    max_features=8,
                    subsample=0.8,
                    random_state=10
                ),
    't1d_model_t':0.43,
    't1d_model_resampling_method': 'smote-tomek',
    't2d_model': GradientBoostingClassifier(
                    n_estimators=200,
                    learning_rate=0.05,
                    min_samples_split=350,
                    min_samples_leaf=5,
                    max_depth=13,
                    max_features=9,
                    subsample=0.85,
                    random_state=10
                ),
    't2d_model_t': 0.38,
    't2d_model_resampling_method': 'smote',
    't3d_model': GradientBoostingClassifier(
                    n_estimators=500,
                    learning_rate=0.01,
                    min_samples_split=350,
                    min_samples_leaf=25,
                    max_depth=11,
                    max_features=10,
                    subsample=0.85,
                    random_state=10
                ),
    't3d_model_t': 0.45,
    't3d_model_resampling_method': 'smote-tomek',
}

"""
Dict containing models' input features and targets for each time horizon
"""
# MOD1
MOD1_FEATURES = {
    't1d_features_set': [
        'radio_flux_10.7cm_t3', 'radio_flux_10.7cm_t2', 'radio_flux_10.7cm_t1', 
        'sesc_sunspot_number_t1', 
        'c_component_wmfr_t1'
    ],
    't1d_target_feature': 'flare_t1do',
    't2d_features_set': [
        'radio_flux_10.7cm_t2', 'radio_flux_10.7cm_t1',
        'sesc_sunspot_number_t1',
        'mag_type_wmfr_t1',
        'c_component_wmfr_t1'
    ],
    't2d_target_feature': 'flare_t2do',
    't3d_features_set': [
        'radio_flux_10.7cm_t1',
        'mag_type_wmfr_t1',
        'c_component_wmfr_t1'
    ],
    't3d_target_feature': 'flare_t3do'
}
# MOD2
MOD2_FEATURES = {
    't1d_features_set': [
        'radio_flux_10.7cm_t5', 'radio_flux_10.7cm_t4', 'radio_flux_10.7cm_t3',  'radio_flux_10.7cm_t2', 'radio_flux_10.7cm_t1',
        'sesc_sunspot_number_t5', 'sesc_sunspot_number_t4', 'sesc_sunspot_number_t3', 'sesc_sunspot_number_t2', 'sesc_sunspot_number_t1', 
        'sunspot_area_t5', 'sunspot_area_t4', 'sunspot_area_t3', 'sunspot_area_t2', 'sunspot_area_t1',
        'goes15_xray_bkgd_flux_t1',
        'z_component_wmfr_t5', 'z_component_wmfr_t4', 'z_component_wmfr_t3', 'z_component_wmfr_t2', 'z_component_wmfr_t1',
        'p_component_wmfr_t5', 'p_component_wmfr_t4', 'p_component_wmfr_t3', 'p_component_wmfr_t2', 'p_component_wmfr_t1',
        'c_component_wmfr_t5', 'c_component_wmfr_t4', 'c_component_wmfr_t3', 'c_component_wmfr_t2', 'c_component_wmfr_t1',
        'mag_type_wmfr_t5', 'mag_type_wmfr_t4', 'mag_type_wmfr_t3', 'mag_type_wmfr_t2', 'mag_type_wmfr_t1'
    ],
    't1d_target_feature': 'flare_t1do',
    't2d_features_set': [
         'radio_flux_10.7cm_t5', 'radio_flux_10.7cm_t4', 'radio_flux_10.7cm_t3',  'radio_flux_10.7cm_t2', 'radio_flux_10.7cm_t1',
         'sesc_sunspot_number_t5', 'sesc_sunspot_number_t4', 'sesc_sunspot_number_t3', 'sesc_sunspot_number_t2', 'sesc_sunspot_number_t1', 
         'sunspot_area_t5', 'sunspot_area_t4', 'sunspot_area_t3', 'sunspot_area_t2', 'sunspot_area_t1',
         'goes15_xray_bkgd_flux_t3', 'goes15_xray_bkgd_flux_t1',
         'z_component_wmfr_t5', 'z_component_wmfr_t4', 'z_component_wmfr_t3', 'z_component_wmfr_t2', 'z_component_wmfr_t1',
         'p_component_wmfr_t5', 'p_component_wmfr_t4', 'p_component_wmfr_t3', 'p_component_wmfr_t2', 'p_component_wmfr_t1',
         'c_component_wmfr_t5', 'c_component_wmfr_t4', 'c_component_wmfr_t3', 'c_component_wmfr_t2', 'c_component_wmfr_t1',
         'mag_type_wmfr_t5', 'mag_type_wmfr_t4', 'mag_type_wmfr_t3', 'mag_type_wmfr_t2', 'mag_type_wmfr_t1'
    ],
    't2d_target_feature': 'flare_t2do',
    't3d_features_set': [
        'radio_flux_10.7cm_t5', 'radio_flux_10.7cm_t4', 'radio_flux_10.7cm_t3',  'radio_flux_10.7cm_t2', 'radio_flux_10.7cm_t1',
        'sesc_sunspot_number_t5', 'sesc_sunspot_number_t4', 'sesc_sunspot_number_t3', 'sesc_sunspot_number_t2', 'sesc_sunspot_number_t1', 
        'sunspot_area_t5', 'sunspot_area_t4', 'sunspot_area_t3', 'sunspot_area_t2', 'sunspot_area_t1',
        'goes15_xray_bkgd_flux_t2', 'goes15_xray_bkgd_flux_t1',
        'z_component_wmfr_t5', 'z_component_wmfr_t4', 'z_component_wmfr_t3', 'z_component_wmfr_t2', 'z_component_wmfr_t1',
        'p_component_wmfr_t5', 'p_component_wmfr_t4', 'p_component_wmfr_t3', 'p_component_wmfr_t2', 'p_component_wmfr_t1',
        'c_component_wmfr_t5', 'c_component_wmfr_t4', 'c_component_wmfr_t3', 'c_component_wmfr_t2', 'c_component_wmfr_t1',
        'mag_type_wmfr_t5', 'mag_type_wmfr_t4', 'mag_type_wmfr_t3', 'mag_type_wmfr_t2', 'mag_type_wmfr_t1'
    ],
    't3d_target_feature': 'flare_t3do'
}


"""
Column names for model_input
"""
COL_NAMES_MODEL_INPUT = [
    "year_t5", "year_t4", "year_t3", "year_t2", "year_t1",
    "month_t5", "month_t4", "month_t3", "month_t2", "month_t1",
    "day_t5", "day_t4", "day_t3", "day_t2", "day_t1",
    'radio_flux_10.7cm_t5', 'radio_flux_10.7cm_t4', 'radio_flux_10.7cm_t3', 'radio_flux_10.7cm_t2', 'radio_flux_10.7cm_t1',
    'sesc_sunspot_number_t5', 'sesc_sunspot_number_t4', 'sesc_sunspot_number_t3', 'sesc_sunspot_number_t2', 'sesc_sunspot_number_t1',
    'sunspot_area_t5', 'sunspot_area_t4', 'sunspot_area_t3', 'sunspot_area_t2', 'sunspot_area_t1',
    'goes15_xray_bkgd_flux_t5', 'goes15_xray_bkgd_flux_t4', 'goes15_xray_bkgd_flux_t3', 'goes15_xray_bkgd_flux_t2', 'goes15_xray_bkgd_flux_t1',
    'z_component_wmfr_t5', 'z_component_wmfr_t4', 'z_component_wmfr_t3', 'z_component_wmfr_t2', 'z_component_wmfr_t1',
    'p_component_wmfr_t5', 'p_component_wmfr_t4', 'p_component_wmfr_t3', 'p_component_wmfr_t2', 'p_component_wmfr_t1',
    'c_component_wmfr_t5', 'c_component_wmfr_t4', 'c_component_wmfr_t3', 'c_component_wmfr_t2', 'c_component_wmfr_t1',
    'mag_type_wmfr_t5', 'mag_type_wmfr_t4', 'mag_type_wmfr_t3', 'mag_type_wmfr_t2', 'mag_type_wmfr_t1'
]


"""
Column names for dataframe (for inner processing)
"""
COL_NAMES_DATAFRAME = [
    'year',
    'month',
    'day',
    'radio_flux',
    'sunspot_number',
    'sunspot_area',
    'xray_background_flux',
    'z_component_wmfr',
    'p_component_wmfr',
    'c_component_wmfr',
    'mag_type_wmfr'
]

"""
Column names for dataframe (for presenting view data)
"""
COL_NAMES_DATAFRAME_VIEW = [
    'Year',
    'Month',
    'Day',
    'Radio flux',
    'Sunspot number',
    'Sunspot area',
    'X-ray background flux',
    'Z component WMFR',
    'p component WMFR',
    'c component WMFR',
    'Mag type WMFR'
]

main()

if SCHEDULED_EXECUTION:
    schedule.every().day.at(EXECUTION_HOUR).do(main)
    #schedule.every().hour.do(main)
    #schedule.every(20).minutes.do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)
        
        

