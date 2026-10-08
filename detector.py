import librosa
import numpy as np
import requests
import time

def check_siren(audio_file):
    # 1. Load the audio file
    y, sr = librosa.load(audio_file, duration=5)
    
    # 2. Extract pitch/frequencies using Fast Fourier Transform (FFT)
    frequencies = np.abs(librosa.stft(y))
    fft_freqs = librosa.fft_frequencies(sr=sr)
    
    # 3. Find the average dominant frequency
    mean_freq = np.mean(fft_freqs[np.argmax(frequencies, axis=0)])
    print(f"Detected Sound Frequency: {mean_freq:.1f} Hz")
    
    # 4. Ambulance sirens sweep continuously between 700 Hz and 1500 Hz
    if 700 <= mean_freq <= 1500:
        print("🚨 SIREN DETECTED! Sending alert to server...")
        # Send alert to backend server
        try:
            requests.post("http://localhost:3000/trigger-siren", json={
                "vehicle_id": "AMB-101",
                "direction": "NORTH",
                "status": "EMERGENCY"
            })
        except Exception as e:
            print("Server not running yet! Start server.js first.")
    else:
        print("Normal traffic noise / No siren detected.")

# Test with an audio file
check_siren("ambulance_siren.wav")