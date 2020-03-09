#!/usr/bin/env python3
import subprocess
import picamera
import time

YOUTUBE = "rtmp://a.rtmp.youtube.com/live2/"
KEY = 'p5kf-tfwm-1r8t-5g1z'
stream_cmd = 'ffmpeg -thread_queue_size 16 -re -ar 44100 -ac 2 -acodec pcm_s16le -f s16le -ac 2 -i /dev/zero -f h264 -i - -vcodec copy -acodec aac -ab 128k -g 50 -strict experimental -f flv ' + YOUTUBE + KEY
stream = subprocess.Popen(stream_cmd, shell=True, stdin=subprocess.PIPE)

camera = picamera.PiCamera(resolution=(640, 480), framerate=25)
try:
    now = time.strftime("%Y-%m-%d-%H:%M:%S")
    camera.framerate = 25
    camera.vflip = False
    camera.hflip = False
    camera.start_recording(stream.stdin, format='h264', bitrate=2000000)
    while True:
        camera.wait_recording(1)
except KeyboardInterrupt:
    camera.stop_recording()
finally:
    camera.close()
    stream.stdin.close()
    stream.wait()
    print("Camera safely shut down")
    print("Good bye")
