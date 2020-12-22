#! /usr/bin/python3
# file audio.py
# created 20201220
# author roch schanen
# comment chmod u+x audio.py

# todo create sinusoidal signal and make one channel wav file

from numpy import linspace
from numpy import append
from numpy import empty
from numpy import array
from numpy import int16
from numpy import sin
from numpy import pi


def bytestr(value):
    s = ""
    for n in value: s += f' {n:02x}'
    return s.strip()

class wave():

    def __init__(self):
        # display debug statement
        print('create "wave()" class instance')
        return

    data = None         # sample list

    def add(self, datArr):

        return

if __name__ == "__main__":


    f = 440.0  # frequency
    d = 1.0    # duration
    r = 44100  # samples per seconds
    w = 16     # data width (16 bits)
    
    r = 8

    # compute sound waves (constants)
    t = linspace(0.0, d, d*r)
    x = [+1.0]*r # compute left  channel
    y = [-1.0]*r # compute right channel
    # interweave x and y channel
    z = empty(2*r, dtype = float)
    z[0::2] = x # copy left  channel
    z[1::2] = y # copy right channel
    # convert floating arrays to 16 bits integers coded as little endian bytes
    data   = ((32767*z).astype(int16)).tobytes()

    # strings
    D1 = b'RIFF'
    D2 = b'WAVE'
    D3 = b'fmt '
    D4 = b'data'

    # length
    l3  = len(data)
    l1  = 36 + l3
    l2  = 16

    # encoding
    pcm         = 1
    channels    = 2
    samplerate  = r
    samplebits  = w
    blockalign  = channels * samplebits / 8
    bytesrate   = samplerate * blockalign

    print(bytestr(D1), bytestr(l1), bytestr(D2))
    print(bytestr(b'fmt '), bytestr(),  )

    print(bytestr(data))

    w = wave()

    # sin(2.0*pi*f*t)

# http://soundfile.sapp.org/doc/WaveFormat/
