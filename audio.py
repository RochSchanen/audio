#! /usr/bin/python3
# file: audio.py
# created: 20201220
# author: roch schanen
# comment: > chmod u+x audio.py
# comment: > ./audio.py
# comment: > aplay sound.wav

# source: https://wavefilegem.com/how_wave_files_work.html

# valid formats (so far):
# RIFF-WAVE-  PCM  integer data 8-16-32 bits
# RIFF-WAVE- "PCM" floating point data 32-64 bits

# todo: fix asymetry for signed integer encoding, find an accurate convertion

from numpy import empty
from numpy import ndarray
from numpy import uint8
from numpy import int16
from numpy import int32
from numpy import int64
from numpy import float32
from numpy import float64
from numpy import frombuffer

__UPPER__ = b"ABCDEFGHIJKLMNOPQRSTUVWXYZ"
__LOWER__ = b"abcdefghijklmnopqrstuvwxyz"
__NUM__   = b"0123456789"
__ALPHA__    = __UPPER__+__LOWER__
__ALPHANUM__ = __ALPHA__+__NUM__

class wave:

    def __init__(self):
        print('instanciate new wave() object')
        return

    # wave data default
    data = b''

    # meta data default
    meta = {
        'ID1': b'RIFF',                # string ID
        'CS1': b'\x24\x00\x00\x00',    # chunk size = 36 (data chunk empty)
        'ID2': b'WAVE',                # string ID 
        'ID3': b'fmt ',                # string ID
        'CS2': b'\x10\x00\x00\x00',    # chunk size = 16 (fixed)
        'af' : b'\x01\x00',            # audio format = 1 (PCM)
        'ch' : b'\x02\x00',            # channels = 2 (stereo)
        'sr' : b'\x00\x00\x00\x00',    # sample rate = 0 (samples per seconds)
        'br' : b'\x00\x00\x00\x00',    # byte rate = 0 (bytes per seconds)
        'al' : b'\x04\x00',            # block alignment size = 4 bytes
        'sw' : b'\x10\x00',            # bits per samples = 16 (sample width)
        'ID4': b'data',                # string ID
        'CS3': b'\x00\x00\x00\x00'}    # chunk size = 0 (data chunk empty)

    def displayMeta(self):
        # display meta data as a table
        for n, v in zip(self.meta.keys(), self.meta.values()):
            s = f"{n}\tb'"
            for m in v:
                s += f"\\x{m:02x}"
            if len(s) < 20:
                s += 8*' '
            s += f" 'b'"
            for m in v:
                if m in __ALPHANUM__:
                    s += f"{m:c}"
            print(f"{s}'")
        # done
        return

    def get(self, *args):
        """ The function get() returns a list of values from the header. The
        list to return is determined by the *args parameter list. Each element
        of the parameter list is a string defining the name of the value to
        return. If the parameters list contains only a single element. The
        function doesn't return a list but a single value. For example:
        - X = self.get('x') returns the value of 'x'
        - X, Y = self.get('x', 'y') returns the values of both 'x' and 'y'
        """
        values = []
        for name in args:
            # convert byte string to integer value
            values.append(int.from_bytes(self.meta[name], 'little'))
        # check for single name
        if len(values) == 1:
            return values[0]
        # done
        return  values

    def set(self, name, value):
        # preserve string length
        l = len(self.meta[name])
        # set bytes string value
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

    def setData(self, ndal):
        """ convert ndarrays into binary data
        ndal is either a single ndarray or a list of ndarrays
        ...                                                                 !!!
        """
        
        print('--- wave.setData() ---')

        # coerce data to a list of ndarrays
        if isinstance(ndal, ndarray): ndal = [ndal]

        # compute and save the number of channels
        ch = len(ndal)
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
        l = len(ndal[0])
        self.set('CS3', l*al)
        self.set('CS1', l*al+36)
        print('data length', l)
        print('data size', l*al)

        # reserve memory
        m = empty(l*ch, dtype = float)

        # inter-weave channels
        for i, d in enumerate(ndal):
            m[i::ch] = ndal[i]

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
        # done
        return

    def importFile(self, filepath):
        fh = open(filepath, 'rb')
        meta = fh.read(44)
        
        # ID1, CS1, ID2 
        err = False
        if not meta[0:4]  == b'RIFF': err = True
        if not meta[8:12] == b'WAVE': err = True
        if err:
            print('RIFF-WAVE format expected')
            print('exiting...')
            exit()
        self.meta['CS1'] = meta[4:8]

        # ID3, CS2
        err = False
        if not meta[12:16] == b'fmt ': err = True
        if err:
            print('"fmt " identifier expected')
            print('exiting...')
            exit()
        self.meta['CS2'] = meta[16:20]
        
        # check header length
        err = False
        if not self.get('CS2') == 16: err =True
        if err:
            print('expected fmt header length of 16 bytes')
            print('exiting...')
            exit()

        # af
        err = True
        # WAVE_FORMAT_PCM
        if meta[20:22] == b'\x01\x00': err = False
        # WAVE_FORMAT_IEEE_FLOAT
        # (accept WAVE_FORMAT_IEEE_FLOAT when header length = 16)
        if meta[20:22] == b'\x03\x00': err = False
        if err:
            print('PCM format expected')
            print('exiting...')
            exit()
        self.meta['af']  = meta[20:22]

        # ch, sr, br, al, sw
        self.meta['ch']  = meta[22:24]
        self.meta['sr']  = meta[24:28]
        self.meta['br']  = meta[28:32]
        self.meta['al']  = meta[32:34]
        self.meta['sw']  = meta[34:36]

        # display
        print(f'channels \t= {self.get("ch")}')
        print(f'sample rate \t= {self.get("sr")}S/s')
        print(f'data width \t= {self.get("sw")}bits')
        if self.get('af') == 1: print('data type \t= integer')
        if self.get('af') == 3: print('data type \t= float')

        # ID4
        err = False
        if not meta[36:40] == b'data': err = True
        if err:
            print('"data" identifier expected')
            print('exiting...')
            exit()
        self.meta['CS3'] = meta[40:44]

        # display
        samples = self.get('CS3') / self.get('al')
        print(f"samples \t= {samples:.0f}")
        print(f"duration \t= {samples/self.get('sr'):.3f}s")

        # data
        self.data = fh.read(self.get('CS3'))

        # done
        fh.close()
        return

    def getData(self):
        # define type convertion table
        typeTable = {
            (1, 8)  : uint8,
            (1, 16) : int16,
            (1, 32) : int32,
            (3, 32) : float32,
            (3, 64) : float64,
        }
        # get data format from header
        af, sw, ch = self.get('af', 'sw', 'ch')
        dataType = typeTable[(af, sw)]
        # get ndarray from binary data
        nda = frombuffer(self.data, dataType)
        # unweave data channels
        data = []
        for i in range(ch):
            data.append(nda[i::ch])
        # done
        return data

if __name__ == "__main__":

    __DEVSTEP__ = 3

    # ------------------
    if __DEVSTEP__ == 3:

        # load float 32 bits wav file
        # convert
        # save integer 16 bits wav file
        mywave = wave()
        mywave.importFile('./violin.wav')
        # mywave.displayMeta()
        X, Y = mywave.getData()
        # print(min(X), max(X))
        # print(min(Y), max(Y))
        mywave.set('af', 1)
        mywave.set('sw', 16)
        mywave.setData([X, Y])
        mywave.exportFile('./soundcopy.wav')

    # ------------------
    if __DEVSTEP__ == 2:

        # import, export test
        print()
        mywave = wave()
        print()
        mywave.importFile('./sound.wav')
        print()
        mywave.displayMeta()
        print()
        mywave.exportFile('./soundcopy.wav')

    # ------------------
    if __DEVSTEP__ == 1:

        # build two waves and export data in .wav (WAVE) file

        from numpy import linspace
        from numpy import sin
        from numpy import pi

        f1 = 440.0  # left frequency
        f2 = 440.0  # right frequency
        r  = 44100  # rate (sample/s)
        d  = 0.50   # duration

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
