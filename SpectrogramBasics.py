#Resources Used
#https://pythontic.com/visualization/signals/spectrogram
#https://docs.python.org/3/library/wave.html
#https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.windows.hann.html#scipy.signal.windows.hann
#https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.spectrogram.html
#https://zach.se/generate-audio-with-python/

#important that the files read into the get_spectrogram function are mono channel, NOT STEREO
#get_spectrogram(r'C:\Users\npose\Documents\Programming\Atom\Spectro_Images\ShiaLaBeoufSample3.wav')


# import the libraries
import matplotlib.pyplot as plt
import numpy             as np
from   scipy.io          import wavfile
from   scipy             import signal
import wave
import struct
import math
from   playsound         import playsound

#create sine look up table
#subtract values by 32768
sineTable = [16384,16617,16850,17084,17317,17550,17782,18015,
18247,18479,18710,18941,19171,19401,19630,19858,
20086,20313,20539,20765,20989,21213,21435,21657,
21877,22097,22315,22532,22747,22962,23175,23387,
23597,23806,24013,24219,24423,24626,24827,25026,
25223,25419,25613,25805,25995,26183,26369,26553,
26735,26915,27092,27268,27441,27612,27781,27948,
28112,28274,28433,28590,28744,28896,29046,29193,
29337,29478,29617,29754,29887,30018,30146,30271,
30394,30513,30630,30744,30855,30963,31068,31170,
31269,31365,31458,31548,31634,31718,31799,31876,
31951,32022,32090,32155,32216,32275,32330,32382,
32430,32476,32518,32557,32593,32625,32654,32680,
32702,32721,32737,32749,32759,32764,32767,32766,
32762,32754,32744,32729,32712,32691,32667,32640,
32609,32575,32538,32497,32454,32407,32356,32303,
32246,32186,32123,32056,31987,31914,31838,31759,
31677,31591,31503,31412,31317,31220,31119,31016,
30909,30800,30687,30572,30454,30333,30209,30082,
29953,29821,29686,29548,29408,29265,29120,28971,
28821,28668,28512,28354,28193,28030,27865,27697,
27527,27355,27180,27004,26825,26644,26461,26276,
26089,25900,25709,25516,25321,25125,24926,24726,
24525,24321,24116,23910,23702,23492,23281,23069,
22855,22640,22423,22206,21987,21767,21546,21324,
21101,20877,20652,20426,20200,19972,19744,19515,
19286,19056,18825,18594,18363,18131,17899,17666,
17433,17200,16967,16734,16500,16267,16033,15800,
15567,15334,15101,14868,14636,14404,14173,13942,
13711,13481,13252,13023,12795,12567,12341,12115,
11890,11666,11443,11221,11000,10780,10561,10344,
10127,9912,9698,9486,9275,9065,8857,8651,
8446,8242,8041,7841,7642,7446,7251,7058,
6867,6678,6491,6306,6123,5942,5763,5587,
5412,5240,5070,4902,4737,4574,4413,4255,
4099,3946,3796,3647,3502,3359,3219,3081,
2946,2814,2685,2558,2434,2313,2195,2080,
1967,1858,1751,1648,1547,1450,1355,1264,
1176,1090,1008,929,853,780,711,644,
581,521,464,411,360,313,270,229,
192,158,127,100,76,55,38,23,
13,5,1,0,3,8,18,30,
46,65,87,113,142,174,210,249,
291,337,385,437,492,551,612,677,
745,816,891,968,1049,1133,1219,1309,
1402,1498,1597,1699,1804,1912,2023,2137,
2254,2373,2496,2621,2749,2880,3013,3150,
3289,3430,3574,3721,3871,4023,4177,4334,
4493,4655,4819,4986,5155,5326,5499,5675,
5852,6032,6214,6398,6584,6772,6962,7154,
7348,7544,7741,7940,8141,8344,8548,8754,
8961,9170,9380,9592,9805,10020,10235,10452,
10670,10890,11110,11332,11554,11778,12002,12228,
12454,12681,12909,13137,13366,13596,13826,14057,
14288,14520,14752,14985,15217,15450,15683,15917,
16150,16384]

#based on sampling frequency of 44.1 kHz
freq_max = 22050
sample_freq = 44100
#Length of file in seconds
fileLength = 1
#max_amplitude for wav data
max_amplitude = 32767.0

#plot the frequency spectrum of a signal
def plot_spectrum(signal):
    N = sample_freq*fileLength
    Fs = sample_freq
    Y_k = np.fft.fft(signal)[0:int(N/2)]/N # FFT function from numpy
    Y_k[1:] = 2*Y_k[1:] # need to take the single-sided spectrum only
    Pxx = np.abs(Y_k) # be sure to get rid of imaginary part
    f = Fs*np.arange((N/2))/N; # frequency vector
    plt.plot(f,Pxx)
    plt.ylabel('Amplitude')
    plt.xlabel('Frequency [Hz]')
    plt.show()

#plot spectrogram of a signal
def get_spectrogram(path):
    #Pull data from .wav file
    sampleRate, data = wavfile.read(path)
    #Compute spectrogram
    #We use a hanning window here with width of 64 samples and non-symmetric window for spectral analysis
    frequencies, segmentTimes, Sxx = signal.spectrogram(data, sampleRate, signal.windows.hann(2048, False))
    #Plot spectrogram
    plt.pcolormesh(segmentTimes, frequencies, Sxx, shading = 'gouraud')
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [s]')
    plt.show()

#make horizontal lines in the spectrogram
#input is a list of lists
#inner lists will be frequency values of the horizontal lines
def create_horizontal_line(biasValuesList):
    #Generate Waves
    #Making your own .wav files of varying frequencies
    #PCM-16 -> values range [-32767, 32767]
    #create wav file
    newFile = wave.open('newWavFile.wav', 'w')
    newFile.setparams((1, 2, sample_freq, sample_freq*fileLength, 'NONE', 'not compressed'))

    #create the horizontal lines with the amount based on the passed values
    #each will last for a full second
    for biasValues in biasValuesList:
        #begin by adding signals together
        y = [[] for x in range(len(biasValues))]
        i = 0
        #create individual frequency sine waves
        for bias in biasValues:
            y[i] = (np.sin(2*np.pi*np.arange(sample_freq*fileLength)*bias/sample_freq)).astype(np.float32)
            i+=1
        z = 0
        #add sine waves to overall signal
        for j in y:
            z = z + j
        #convert the signal to a wav file
        for i in range(sample_freq*fileLength):
            data = struct.pack('<h', int(z[i]))
            newFile.writeframesraw(data)
    newFile.close()
    #create spectrogram
    get_spectrogram(r'newWavFile.wav')


#test values
biasValues = [[1000, 5000, 7500, 10000, 15000, 20000],[3000, 12500,17500],[5000,20000,7500,3000]]
create_horizontal_line(biasValues)
