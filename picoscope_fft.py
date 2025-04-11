# %%

import glob
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#df = pd.read_parquet('aquisition_2025-04-11_13-35-48.parquet')
files = glob.glob('try/*.parquet')
print(files)

path_fft = 'ffts'
os.makedirs(f'{path_fft}', exist_ok = True)
for file in files[-1:]:
    df = pd.read_parquet(file)
    fftA = np.fft.fft(df.adc2mVChAMax[:])
    fftB = np.fft.fft(df.adc2mVChBMax[:])
    fftC = np.fft.fft(df.adc2mVChCMax[:])
    fftD = np.fft.fft(df.adc2mVChDMax[:])

    labels = ['Channel A', 'Channel B', 'Channel C', 'Channel D']
    plt.figure(figsize = (7,5), dpi = 300)
    freqs = np.linspace(0, np.unique(df.sampling_rate), len(abs(fftA)))
    for i, fft in enumerate([fftA, fftB, fftC, fftD]):
        plt.plot(freqs, abs(fft)/len(abs(fft))*2, label = f'{labels[i]}')
        plt.ylim(0, 10)
        plt.xlim(0,1000)
        plt.title(f'{np.unique(df.timestamp)[0]} time, {np.unique(round(df.sampling_rate/1e6, 2))[0]} MS/s', size = 20)
        plt.xlabel('Frequency [Hz]', size = 16)
        plt.ylabel('Amplitude [mV]', size = 16)
        plt.legend()
        plt.grid()
    plt.savefig(f'{path_fft}/fft_{np.unique(df.timestamp)[0]}.png')



# %%
for file in files[-1:]:
    df = pd.read_parquet(file)
    signalA = df.adc2mVChAMax
    signalB = df.adc2mVChBMax
    signalC = df.adc2mVChCMax
    signalD = df.adc2mVChDMax

    labels = ['Channel A', 'Channel B', 'Channel C', 'Channel D']
    plt.figure(figsize = (7,5), dpi = 300)
    for i, signal in enumerate([signalA, signalB, signalC, signalD]):
        plt.plot(df.time/1e9, signal, label = f'{labels[i]}', lw = 0.3)
        #plt.ylim(0, 10)
        #plt.xlim(0,1000)
        plt.title(f'{np.unique(df.timestamp)[0]} time, {np.unique(round(df.sampling_rate/1e6, 2))[0]} MS/s', size = 20)
        plt.xlabel('Frequency [Hz]', size = 16)
        plt.ylabel('Amplitude [mV]', size = 16)
        plt.legend()
        plt.grid()
    #plt.savefig(f'{path_fft}/fft_{np.unique(df.timestamp)[0]}.png')


# %%
