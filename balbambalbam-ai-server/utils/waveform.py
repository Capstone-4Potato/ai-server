import base64
import wave
import numpy as np
import matplotlib.pyplot as plt
import io
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.file_conversion import base64_to_wav, file_to_base64


def draw_waveform(base64_audio, color):    
    # Convert base64 audio to a WAV file
    wav_file_path = base64_to_wav(base64_audio)
    
    # Read audio file and extract parameters
    with wave.open(wav_file_path, 'r') as wave_file:
        params = wave_file.getparams()
        num_channels, sample_width, frame_rate, num_frames = params[:4]
        audio_frames = wave_file.readframes(num_frames)
    
    # Convert audio frames to numpy array
    audio_samples = np.frombuffer(audio_frames, dtype=np.int16)
    
    # Detect non-silent parts of the audio
    threshold = 2500
    non_silent_indices = np.where(np.abs(audio_samples) > threshold)[0]
    start_index = non_silent_indices[0] if non_silent_indices.size > 0 else 0
    end_index = non_silent_indices[-1] if non_silent_indices.size > 0 else len(audio_samples)
    non_silent_samples = audio_samples[start_index:end_index]
    
    # Calculate time array for plotting
    start_time = start_index / frame_rate
    end_time = end_index / frame_rate
    duration = end_time - start_time
    time_array = np.linspace(start_time, end_time, len(non_silent_samples))
    
    # Create waveform plot
    plt.figure(figsize=(10, 4), facecolor='white')
    plt.plot(time_array, non_silent_samples, color=color)
    plt.axis('off')
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])
    plt.ylim(0, np.max(35000))
    plt.tight_layout()
    
    # Save plot to a BytesIO object
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', transparent=True)
    buffer.seek(0)
    plt.close()
    
    # Encode image to base64
    base64_image = file_to_base64(buffer)
    
    return duration, base64_image