import joblib
import os
import pickle
import config

from scipy.fft import fft

import numpy as np
import mne


save_dir = config.MODEL_DIR
edf_file_name = config.EDF_FILE_NAME

def read_data(file_path):
    datax=mne.io.read_raw_edf(file_path, preload=True)
    datax.resample(100)
    datax.set_eeg_reference()
    datax.filter(l_freq=1, h_freq=45)
    datax.notch_filter(freqs=45)
    if (datax.info['bads']):
        datax.info['bads'] = ['MEG 2443']
        ch_names = datax.info['ch_names'].copy()
        ch_names.remove('MEG 2443')
        datax.reorder_channels(['MEG 2443'] + ch_names)
    else:
        pass
    ica = mne.preprocessing.ICA(n_components=14, random_state=42)
    ica.fit(datax.filter(5,15))
    epochs=mne.make_fixed_length_epochs(datax,duration=25,overlap=0)
    epochs=epochs.get_data()
    return epochs #trials,channel,length

def apply_fft(data_array):
    for i in range(data_array.shape[0]):
        for j in range(data_array.shape[1]):
            data_array[i, j, :] = fft(data_array[i, j, :])
    return data_array

# Load the FeatureExtractor and MinMaxScaler objects
def load_preprocessing_objects(save_dir):
    with open(save_dir + '/fe.pkl', 'rb') as f:
        fe = pickle.load(f)
    with open(save_dir + '/scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    return fe, scaler


def main_predictor(file_path=edf_file_name):
	data = read_data(file_path)
	
	# applying fft
	data = fft(data)

	# feature reduction and scaling
	fe, scaler = load_preprocessing_objects(save_dir)

	data = fe.transform(data.real.astype(np.float32))
	data = scaler.transform(data)

	# Load the saved model
	model = joblib.load(os.path.join(save_dir, 'model.pkl'))
	    
	predictions = model.predict(data)

	# get the major vote
	pred = np.median(predictions)

	return pred

