#! /usr/bin/python3
# file: audio.py
# created: 20201220
# author: roch schanen
# comment: > chmod u+x audio_dev.py
# comment: > ./audio_dev.py
# comment: > aplay sound.wav

# __DEBUG__ = True
# from numpy import array
# from numpy import append
# from numpy import empty
# from numpy import iinfo
# from numpy import finfo
# from numpy import uint8
# from numpy import int16
# from numpy import int32
# from numpy import int64
# from numpy import float32
# from numpy import float64
# from numpy import frombuffer

# to do: automate some convertion
#      : keep data in float format
#      : at the moment we need getData/setData()
#      : to update format changes.

from audio import wave

if __name__ == "__main__":

    __DEVSTEP__ = 5

    # ------------------
    if __DEVSTEP__ == 5:

        # build two waves and export data in .wav (WAVE) file

        from numpy import linspace
        from numpy import sin
        from numpy import pi
        from numpy import array
        from numpy import append

        R = array([], float)
        L = array([], float)

        r  = 44100  # rate (sample/s)
        d  = 1.0    # duration
        
        # compute time interval
        t = linspace(0.0, d, int(d*r))

        # compute wave parts

        for part in [
                [440.0, 1.0, 0.0*pi, 440.0, 1.0, 0.0*pi],
                [440.0, 1.0, 0.0*pi, 440.0, 1.0, 0.0*pi],
            ]:

            fR, aR, pR, fL, aL, pL = part       

            R = append(R, aR*sin(2.0*pi*fR*t+pR)) # left  channel
            L = append(L, aL*sin(2.0*pi*fL*t+pL)) # right channel

        mywave = wave()

        mywave.setData([L,R])
        mywave.setSampleRate(r)

        # mywave.displayMeta()
        # mywave.displayData()

        mywave.exportFile('./sound.wav')

        # > aplay sound.wav
        # should show the correct parameters
        # should sound like a pure 'A' note

    # ------------------
    if __DEVSTEP__ == 4:

        # load float 32 bits wav file
        # convert
        # save integer 16 bits wav file
        mywave = wave()
        mywave.importFile('./soundcopy.wav')

        mywave.displayMeta()

        X, Y = mywave.getData()
        mywave.set('af', 1)
        mywave.set('sw', 16)
        mywave.setData([X, Y])

        mywave.displayMeta()

        mywave.exportFile('./soundcopy2.wav')

        # > aplay soundcopy.wav
        # > aplay soundcopy2.wav
        # should show the correct parameters
        # should sound exactly the same

    # ------------------
    if __DEVSTEP__ == 3:

        # load integer 16 bits wav file
        # convert
        # save float 32 bits wav file
        mywave = wave()
        mywave.importFile('./sound.wav')
        # mywave.displayMeta()
        X, Y = mywave.getData()
        # print(min(X), max(X))
        # print(min(Y), max(Y))
        mywave.set('af', 3)
        mywave.set('sw', 32)
        mywave.setData([X, Y])
        mywave.exportFile('./soundcopy.wav')

        # > aplay soundcopy.wav
        # > aplay sound.wav
        # should show the correct parameters
        # should sound exactly the same

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

        # > aplay soundcopy.wav
        # > aplay sound.wav
        # should show the correct parameters
        # should sound exactly the same

    # ------------------
    if __DEVSTEP__ == 1:

        # build two waves and export data in .wav (WAVE) file

        from numpy import linspace
        from numpy import sin
        from numpy import pi

        f1 = 440.0  # left frequency
        f2 = 440.0  # right frequency
        r  = 44100  # rate (sample/s)
        d  = 1.0    # duration

        # compute sound waves
        t = linspace(0.0, d, int(d*r))
        x = sin(2.0*pi*f1*t) # compute left  channel
        y = sin(2.0*pi*f2*t) # compute right channel

        mywave = wave()
        mywave.setData([x,y])
        mywave.setSampleRate(r)

        # mywave.displayMeta()
        # mywave.displayData()

        mywave.exportFile('./sound.wav')

        # > aplay sound.wav
        # should show the correct parameters
        # should sound like a pure 'A' note

