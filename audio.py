#! /usr/bin/python3
# file: audio.py
# created: 20201220
# author: roch schanen
# comment: > chmod u+x audio.py
# comment: > ./audio.py
# comment: > aplay sound.wav

# todo: fix asymetry for signed integer encoding, find an accurate convertion

from numpy import empty
from numpy import int16

class wave:

    data = b''

    meta = {
        'ID1': b'RIFF',                # string ID
        'CS1': b'\x24\x00\x00\x00',    # chunk size = 36 (data chunk empty)
        'ID2': b'WAVE',                # string ID 
        'ID3': b'fmt ',                # string ID
        'CS2': b'\x10\x00\x00\x00',    # chunk size = 16 (fixed)
        'af' : b'\x01\x00',            # audio format = 1 (PCM)
        'ch' : b'\x02\x00',            # channels = 2 (stereo)
        'sr' : b'\x00\x00\x00\x00',    # sample rate = 0 (samples per seconds)
        'br' : b'\x00\x00\x00\x00',    # byte rate = 0(bytes per seconds)
        'al' : b'\x04\x00',            # block alignment size = 4 bytes
        'sw' : b'\x10\x00',            # bits per samples = 16 (sample width)
        'ID4': b'data',                # string ID
        'CS3': b'\x00\x00\x00\x00'}    # chunk size = 0 (data chunk empty)

    def displayMeta(self):
        # display meta data as a table
        for n, v in zip(self.meta.keys(), self.meta.values()):
            print(f'{n}\t{v}')
        # done
        return

    def get(self, name):
        # convert bytes string to integer value
        value = int.from_bytes(self.meta[name], 'little')
        # done
        return  value

    def set(self, name, value):
        # preserve bytes string length
        l = len(self.meta[name])
        # update bytes string value
        self.meta[name] = value.to_bytes(l, 'little')
        # done
        return

    def setSampleRate(self, sr):

        print('--- wave.setRate() ---')

        # save sample rate
        self.set('sr', sr)
        print('sample rate', sr)

        # get alignment
        al = self.get('al')
        print('alignment', al)

        # compute and save new byte rate
        br = sr * al
        self.set('br', br)
        print('byte rate', br)

        # done
        return

    def setData(self, data):
        
        print('--- wave.setData() ---')

        # coerce data to a list of ndarrays
        if not isinstance(data, list): data = [data]

        # compute and save the number of channels
        ch = len(data)
        self.set('ch', ch)
        print('channels', ch)

        # get width
        sw = self.get('sw')
        # compute and save alignment size
        al = (sw >> 3) * ch
        self.set('al', al)
        print('sample width', sw)
        print('alignment', al)

        # get sample rate
        sr = self.get('sr')
        # compute and save byte rate
        br = sr * al
        self.set('br', br)
        print('sample rate', sr)
        print('byte rate', br)

        # compute and save data length
        l = len(data[0])
        self.set('CS3', l*al)
        self.set('CS1', l*al+36)
        print('data length', l)
        print('data size', l*al)

        # reserve memory
        m = empty(l*ch, dtype = float)
        # inter-weave channels
        for i, d in enumerate(data): m[i::ch] = data[i]
        # convert floating to signed 16 bits little endian bytes
        self.data = ((32767*m).astype(int16)).tobytes()
        
        # done
        return

    def displayData(self):
        print(self.data)
        return

    def exportFile(self, filepath):
        fh = open(filepath, 'wb')
        fh.write(b''.join(self.meta.values()))
        fh.write(self.data)
        fh.close()
        return

    # def importfile(self, filepath):
    #     return

    # def getSampleRate(self):
    #     return self.get('sr')

    # def getData(self):
    #     return data



if __name__ == "__main__":

    # build two waves and export data in .wav (WAVE) file

    from numpy import linspace
    from numpy import sin
    from numpy import pi

    f1 = 440.0  # left frequency
    f2 = 440.0  # right frequency
    r  = 44100  # rate (sample/s)
    d  = 0.25    # duration

    # compute sound waves
    t = linspace(0.0, d, d*r)
    x = sin(2.0*pi*f1*t) # compute left  channel
    y = sin(2.0*pi*f2*t) # compute right channel

    mywave = wave()
    mywave.setData([x,y])
    mywave.setSampleRate(r)

    # mywave.displayMeta()
    # mywave.displayData()

    mywave.exportFile('./sound.wav')
