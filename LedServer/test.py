import simpleaudio as sa
from subprocess import call

import time

filename = 'sample.wav'
wave_obj = sa.WaveObject.from_wave_file(filename)
play_obj = wave_obj.play()
for i in range(0,100):
    call(["amixer", "-D", "pulse", "sset", "Master", str(i) + "%"])
    time.sleep(0.0)
play_obj.wait_done()  # Wait until sound has finished playing
