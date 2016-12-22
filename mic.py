import pyaudio
import numpy as np
import urllib.request
import threading
    
def light(FLG):
    urllib.request.urlopen( "http://192.168.10.200/light.php?num="+str(FLG) )

CHUNK=2048
RATE=44100
LIGHT_FLG = 3
p=pyaudio.PyAudio()

stream=p.open(  format = pyaudio.paInt16,
    channels = 1,
    rate = RATE,
    frames_per_buffer = CHUNK,
    input = True,
    output = True)

while stream.is_active():
    input = stream.read(CHUNK)
    data = np.frombuffer(input, dtype="int16")
    if len(data[data>30000])>0 :
        print(data[data>30000])
        th_me = threading.Thread(target=light, name="th_me", args=(LIGHT_FLG,)) 
        th_me.start()
        print(str(LIGHT_FLG)+" is on!")
        if LIGHT_FLG==3:
            LIGHT_FLG = 4
        elif LIGHT_FLG==4:
            LIGHT_FLG = 3

stream.stop_stream()
stream.close()
p.terminate()

