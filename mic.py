import numpy as np
import pyaudio
import threading
from subprocess import Popen, PIPE

def action(STAT):
    scpt = b'set volume with output muted'
    if STAT == True:
        scpt = b'set volume without output muted'
    p = Popen(['osascript', '-'] , stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout,stderr = p.communicate(scpt)
    #print(p.returncode, stdout, stderr)

CHUNK=4096
RATE=44100
STATUS = False
p=pyaudio.PyAudio()

print('waiting finger snap ...')
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
        th_me = threading.Thread(target=action, name="th_me", args=(STATUS,))
        th_me.start()
        if STATUS==False:
            STATUS = True
        elif STATUS==True:
            STATUS = False

stream.stop_stream()
stream.close()
p.terminate()
