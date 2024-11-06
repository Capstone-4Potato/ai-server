import librosa
import pandas as pd
import numpy as np
import base64
from scipy.ndimage import uniform_filter1d
import soundfile as sf
import os
from io import BytesIO

def process_and_save_audio_base64(encoded_input, threshold=0.1):
    input_data = base64.b64decode(encoded_input)
    
    audio_bytes = BytesIO(input_data)
    y, sr = librosa.load(audio_bytes, sr=None)

    non_silent_indices = np.where(np.abs(y) > threshold)[0]

    if non_silent_indices.size > 0:
        start_index = non_silent_indices[0]
        end_index = non_silent_indices[-1]
        preprocessed_samples = y[start_index:end_index + 1]
    else:
        preprocessed_samples = np.array([])

    if len(preprocessed_samples) > 0:
        output_audio = BytesIO()
        sf.write(output_audio, preprocessed_samples, sr, format='WAV')

        output_audio.seek(0)  
        encoded_output = base64.b64encode(output_audio.read()).decode('utf-8')

        print("Preprocessed audio ready for output.")
        return encoded_output
    else:
        print("No non-silent samples to save.")
        return None


def extract_dataframe_base64(encoded_audio1, encoded_audio2, window_size=1000, sampling_interval=0.005):
    audio_data1 = base64.b64decode(encoded_audio1)
    audio_data2 = base64.b64decode(encoded_audio2)

    audio_bytes1 = BytesIO(audio_data1)
    audio_bytes2 = BytesIO(audio_data2)

    y1, sr1 = librosa.load(audio_bytes1, sr=None)
    y2, sr2 = librosa.load(audio_bytes2, sr=None)

    if sr1 != sr2:
        sr = min(sr1, sr2)
        y1 = librosa.resample(y1, orig_sr=sr1, target_sr=sr)
        y2 = librosa.resample(y2, orig_sr=sr2, target_sr=sr)
    else:
        sr = sr1

    if len(y1) > len(y2):
        y2 = np.pad(y2, (0, len(y1) - len(y2)), 'constant', constant_values=np.nan)
    else:
        y1 = np.pad(y1, (0, len(y2) - len(y1)), 'constant', constant_values=np.nan)

    y1_mean = uniform_filter1d(np.abs(y1), size=window_size)
    y2_mean = uniform_filter1d(np.abs(y2), size=window_size)

    y1_peaks = np.where((y1 > y1_mean) & (y1 > 0), y1, np.nan)
    y2_peaks = np.where((y2 > y2_mean) & (y2 > 0), y2, np.nan)

    indices1 = np.arange(0, len(y1_peaks), int(sr * sampling_interval))
    indices2 = np.arange(0, len(y2_peaks), int(sr * sampling_interval))

    y1_samples = y1_peaks[indices1]
    y2_samples = y2_peaks[indices2]

    time_samples1 = indices1 / sr
    time_samples2 = indices2 / sr

    df1 = pd.DataFrame({'Time (s)': time_samples1[~np.isnan(y1_samples)],
                        'Amplitude': y1_samples[~np.isnan(y1_samples)]})
    df2 = pd.DataFrame({'Time (s)': time_samples2[~np.isnan(y2_samples)],
                        'Amplitude': y2_samples[~np.isnan(y2_samples)]})

    return df1, df2