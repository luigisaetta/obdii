import sys
import time
from subprocess import call

# only if using Googe Voice
sys.path.append('/home/pi/AIY-voice-kit-python/src')
import aiy.voicehat

def on_button_press():
            button.on_press(None)
            print('The button is pressed!')
            time.sleep(3)
            print('Shutting down...')
            call("sudo shutdown -h now", shell=True)

#
# main
# 

button = aiy.voicehat.get_button()
button.on_press(on_button_press)

while True:
    print('Another loop...')
    time.sleep(5)