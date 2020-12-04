import sys
from pandas_profiling import ProfileReport
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import f1_score
import tensorflow as tf

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
    tmp_samples = pd.read_csv(i)
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


if __name__ == "__main__":
    tmp_samples = pd.read_csv()