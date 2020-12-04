import sys
from pandas_profiling import ProfileReport
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import f1_score
import tensorflow as tf
import os
from sherlock import helpers
from sherlock.features.preprocessing import extract_features, convert_string_lists_to_lists, prepare_feature_extraction
from sherlock.deploy.train_sherlock import train_sherlock
from sherlock.deploy.predict_sherlock import predict_sherlock

import numbers
import json
#'pip install git+git://github.com/clintval/gender_predictor.git'
from gender_predictor import GenderPredictor
import itertools

# Check whether these is a header
def identify_header(path, n=5, th=0.9):
    df1 = pd.read_csv(path, header='infer', nrows=n)
    df2 = pd.read_csv(path, header=None, nrows=n)
    sim = (df1.dtypes.values == df2.dtypes.values).mean()
    return True if sim < th else False

# If no header, generate header
def generate_header(path):
    tmp_samples = pd.read_csv(path)
    # Convert input dataset to the required form
    index_range = range(len(tmp_samples.columns))
    df_value = pd.DataFrame(columns = ['value'],index = index_range)
    df_label = pd.DataFrame(columns = ['label'],index = index_range)
    idx = 0
    for i in tmp_samples.columns:
        unique_val = list(tmp_samples[i].unique())
        val_no_nan = [x for x in unique_val if str(x) != 'nan']
        if len(val_no_nan) == 0:
            # No value in any cell of this attribute
            val_no_nan = [i]
        df_value.at[idx,'value'] = str(val_no_nan)
        df_label.at[idx,'label'] = i
        idx += 1
    # Load Sherlock architecture and weights from files
    file = open('../models/sherlock_model.json', 'r')
    sherlock_file = file.read()
    sherlock = tf.keras.models.model_from_json(sherlock_file)
    file.close()
    sherlock.load_weights('../models/sherlock_weights.h5')
    sherlock.compile(optimizer='adam',
                loss='categorical_crossentropy',
                metrics=['categorical_accuracy'])
    test_samples_converted, y_test = convert_string_lists_to_lists(df_value, df_label,'value','label')
    X_test = extract_features(test_samples_converted)
    predicted_labels = predict_sherlock(X_test, nn_id='sherlock')
    return predicted_labels

def summary_age(x):
    age = {'<16':0,'16-24':0,'25-34':0,
          '35-44':0,'45-54':0,'55-64':0,'>64':0}
    for i in x:
        if i < 16:
            age['<16'] += 1
        elif i <= 24:
            age['16-24'] += 1
        elif i <= 34:
            age['25-34'] += 1
        elif i <= 44:
            age['35-44'] += 1
        elif i <= 54:
            age['45-54'] += 1
        elif i <= 64:
            age['55-64'] += 1
        else:
            age['>64'] += 1
    return age

def trans_age(x):
    i = int(x)
    if i < 16:
        return('<16')
    elif i <= 24:
        return('16-24')
    elif i <= 34:
        return('25-34')
    elif i <= 44:
        return('35-44')
    elif i <= 54:
        return('45-54')
    elif i <= 64:
        return('55-64')
    else:
        return('>64')

def get_var_category(series):
    unique_count = series.nunique(dropna=False)
    total_count = len(series)
    if pd.api.types.is_numeric_dtype(series):
        return 'Numerical'
    elif pd.api.types.is_datetime64_dtype(series):
        return 'Date'
    elif unique_count==total_count:
        return 'Text (Unique)'
    else:
        return 'Categorical'    

def filter_categories(df,column_name):
    if get_var_category(df[column_name]) == 'Categorical':
        return True
    else:
        return False

def predict_gender(x):
    gp = GenderPredictor()
    gp.train_and_test()
    return gp.classify(x)

def preprocess_before_count(tmp,name,gender,age):
    # Preprocess dataframe
    # name = gender = age = country = race = ethnicity = False
    if age:
        # If current not categorical, then convert to category
        if filter_categories(tmp, age):
            tmp[age] = tmp[age].apply(lambda x: trans_age(x))
    if name and (gender == False):
        gender = 'Pred'
        # Name attribute exists, but gender attribute not exists
        pred_gender = []
        for i in tmp[name]:
            pred_gender.append(predict_gender(i))
        tmp['Gender'] = pred_gender
    
    return tmp, gender

def process_df(tmp,cand):
    mup = []
    uncover = set()
    for i in range(1,len(cand)+1):
        att_comb = itertools.combinations(cand, i)
        for att in att_comb:
            count = tmp[list(att)].value_counts()
            value = tmp[list(att)].drop_duplicates().values
            for j in value:
                MUP = True
                idx = 0
                c = count.copy()
                while idx < i:
                    c = c[j[idx]]
                    idx += 1
                if int(c) <= 25:
                    for z in att:
                        uncover.add(z)
                    # No enough case, determine whether MUP
                    for ele in mup:
                        if ele in j:
                            MUP = False
                    if MUP:
                        mup.append(list(j))
    return mup, uncover

def generate_df(dataset_ID,age,gender,race,ethnicity,country,mup,uncover):
    tmp_info = pd.DataFrame(columns = ['Dataset_ID','Age','Gender','Race','Ethnicity','Country','MUP','Uncovered Attributes','Report'])
    tmp_info.at[0,'Dataset_ID'] = dataset_ID
    if age:
        tmp_info.at[0,'Age'] = 'Exist'
    else:
        tmp_info.at[0,'Age'] = 'Not Exist' 
    if gender == 'Pred':
        tmp_info.at[0,'Gender'] = 'Not exist, predict by sherlock'
    elif gender:
        tmp_info.at[0,'Gender'] = 'Exist'
    else:
        tmp_info.at[0,'Gender'] = 'Not Exist' 
    if race:
        tmp_info.at[0,'Race'] = 'Exist'
    else:
        tmp_info.at[0,'Race'] = 'Not Exist' 
    if ethnicity:
        tmp_info.at[0,'Ethnicity'] = 'Exist'
    else:
        tmp_info.at[0,'Ethnicity'] = 'Not Exist'  
    if country:
        tmp_info.at[0,'Country'] = 'Exist'
    else:
        tmp_info.at[0,'Country'] = 'Not Exist'
    #tmp_info.at[0,'Maximal Uncovered Pattern'] = mup
    tmp_info.at[0,'Uncovered Attributes'] = uncover
    tmp_info.at[0,'Report'] = 'report/'+dataset_ID+'.html'
    return tmp_info
    
def make_clickable(url):
    name= os.path.basename(url)
    return '<a href="{}">{}</a>'.format(url,name)

def read_info(path):
    info = pd.read_excel(path, index_col=None)
    info = info.style.format({'Report': make_clickable})
    return info

if __name__ == "__main__":
    tmp_samples = pd.read_csv()