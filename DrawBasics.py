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

"""
Begin by creating basic, necessary, variables
"""
sample_freq = 44100
#Length of file in seconds
fileLength = 1

#Inclduing just in case necessary in later aspects of program
dirac_delta_pulse = [0] + ([1000] * int(sample_freq * 0.0001))

"""
Create functions for basics of spectrogram creation and graphing
"""
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


"""
Functions for basic spectrogram shapes:
    Horizontal Line
    Vertical Line
    Arc/Angle
    Blank Space
"""
#make horizontal lines in the spectrogram
#input is a list of lists
#inner lists will be frequency values of the horizontal lines
def create_horizontal_line(biasValuesList, length):
    #create the horizontal lines with the amount based on the passed values
    #each will last for a full second

    #begin by adding signals together
    y = [[] for x in range(len(biasValuesList))]
    i = 0
    #create individual frequency sine waves
    for bias in biasValuesList:
        y[i] = 20*(np.sin(2*np.pi*np.arange(sample_freq*length)*bias/sample_freq)).astype(np.float32)
        i+=1
    z = 0
    #add sine waves to overall signal
    for j in y:
        z = z + j
    return z

def create_vertical_line(biasValuesList, length):
    #instead of making a vertical line, make the illusion
    #Stack multiple horizontal lines at low frequency differences
    #begin by finding how many sections of lines exist
    returnVal = 0
    for verts in biasValuesList:
        #variable 'verts' will be a list of two values, lower and upper bound, in that order
        newList = range(verts[0],verts[1],50)
        y = create_horizontal_line(newList, length)
        returnVal += y
    return returnVal


def create_arc_line(biasValuesList, length, resolution):
    #arc will be illusion by creating multiple vertical lines
    #number of vertical segments will be the resolution
    #length of vertical segments will be the integer value of length/resolution
    vertLength = length/resolution
    #values used to control arc dimensions
    delta = (biasValuesList[1] - biasValuesList[0]) // resolution
    A = biasValuesList[0]
    B = biasValuesList[0] + delta

    y = [[] for x in range(resolution)]

    for i in range(resolution):
        if A < B:
            y[i] = create_vertical_line([[A,B]], vertLength)
        else:
            y[i] = create_vertical_line([[B,A]], vertLength)
        A = B
        B = B + int(delta)

    returnSignal = []
    for j in y:
        for q in j:
            returnSignal.append(q)
    return returnSignal


def blank_space(length):
    y = []
    for i in range(length*sample_freq):
        y.append(0)
    return y


"""
Now we look at making full shapes within the spectrum

issue at this point is the width parameter does not affect the end spectrogram
"""
def circle(top, bottom, leftGap, width):
    #calculated using circles made with Delta_freq = 18k, 9k result in width of w = 2.5s, 1.25s
    widthBias = 7200
    length = (top-bottom)/(7200 * 5)    #'5' comes from number of lines which make the half circle

    middle = int((top+bottom)//2)
    freqBias = (top-bottom)//5

    print(middle)
    print(freqBias)
    print(middle-freqBias)
    print(middle+freqBias)
    print(middle+(2*freqBias))
    print(middle-(2*freqBias))

    biasValues = [[['b', leftGap],['v', 0.01, [middle-freqBias, middle+freqBias]],['a', length, 300, middle+freqBias, middle+(2*freqBias)],['a', length, 300, middle+(2*freqBias), top],['h',length,top],['a',length,300,top,middle+(2*freqBias)],['a',length,300,middle+(2*freqBias),middle+freqBias],['v',0.01, [middle-freqBias,middle+freqBias]]],
    [['b', leftGap],['a', length, 300, middle-freqBias, middle-(2*freqBias)],['a', length, 300, middle-(2*freqBias), bottom],['h',length,bottom],['a',length,300,bottom,middle-(2*freqBias)],['a',length,300,middle-(2*freqBias),middle-freqBias],['b', 1]]]
    return biasValues


"""
Finally, we want to interface with the above functions
"""
def create_spectrogram_image(biasValuesList):
    #Generate Waves
    #Making your own .wav files of varying frequencies
    #PCM-16 -> values range [-32767, 32767]
    #create wav file
    newFile = wave.open('newWavFile.wav', 'w')
    newFile.setparams((1, 2, sample_freq, sample_freq*fileLength, 'NONE', 'not compressed'))

    #create a number of lists equivalent to number of layers
    finalSignal = [[] for x in range(len(biasValuesList))]
    layerNum = 0
    #create the horizontal lines with the amount based on the passed values
    #each will last for a full second

    #issue at this point is that we create a single continuous signal
    #we want to separate each value such that 'finalSignal' is a series of 'y' signals
    for layers in biasValuesList:
        for biasValues in layers:
            #vertical line
            if biasValues[0] == 'v':
                y = create_vertical_line(biasValues[2:], biasValues[1])
                #horizontal line
            elif biasValues[0] == 'h':
                y = create_horizontal_line(biasValues[2:], biasValues[1])
                #arc
                #biasValues[2] will be the resolution of the arc
            elif biasValues[0] == 'a':
                y = create_arc_line(biasValues[3:], biasValues[1], biasValues[2])
                #blank section
            elif biasValues[0] == 'b':
                y = blank_space(biasValues[1])

            for j in y:
                finalSignal[layerNum].append(j)
        layerNum += 1
    #grab corresponding array which applies to given time slice
    #apply to finalSignal
    maxSignalLength = max(map(len,finalSignal))
    signalPrime = [0 for x in range(maxSignalLength)]

    for z in finalSignal:
        i = 0
        for j in z:
            signalPrime[i] += j
            i += 1

    for i in range(len(signalPrime)):
        data = struct.pack('<h', int(signalPrime[i]))
        newFile.writeframesraw(data)

    newFile.close()
    #create spectrogram
    get_spectrogram(r'newWavFile.wav')

#top, bottom, leftGap, width
#create_spectrogram_image(circle(20000,2000,1, 5))

