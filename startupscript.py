# importing socket module
from ast import And
from asyncio import QueueFull, tasks
from pickle import TRUE
from pydoc import resolve
from signal import alarm
import socket
import subprocess
import json
import os
from unicodedata import numeric
from xmlrpc.client import DateTime
#import modules.mysqlconnector as db
import modules.raspberrypi as pi
#import modules.stringdata as qdata
#import modules.socketcomms as sock
import uuid
import calendar
import time
import functools
from queue import Queue
import threading
from threading import Thread, Lock
import sys
import logging
import asyncio
import queue
from PIL import Image

# import modules.ledcontrol as led
# from rpi_ws281x import PixelStrip, Color

q = queue.Queue(1)
def getRuntimeData(filename="/home/pi/config.json"):
    file = open(filename, "r")
    data = json.load(file)
    file.close()
    return data

    
def updateConfig(dataset, key, value, file="/home/pi/config.json"):
    new_data = {key: value}
    dataset.update(new_data)
    file = open(file, "w")
    json.dump(dataset, file)
    file.close()

def piSetup(filename="/home/pi/config.json"):
    # logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
    ## getting hostname by socket.gethostname method
    data = getRuntimeData()
    return data    

        
def playvideo(video):
    subprocess.run(["cvlc", "-f", "--play-and-exit", "--no-video-title-show", video])
    q.get()

def processtrigger(channel):
    inputindex = 0
    current = -1
    for i in range (0, len(pi_inputs)):
        if(channel == pi_inputs[i]):
            inputindex = i
            break

    if(videoplayingindex != channel):
        output = q.put_nowait(channel)
        if(output != QueueFull):
            argstring = []
            argcount = 1
            argstring.append(videos[inputindex])
            videothread = threading.Thread(target=playvideo, args=argstring)
            videothread.start()
            

    print("button push")
    # pidevice.alarmstate(True) # turn off relay
    

def flashing():
    while True:
        for i in range(0, len(pi_outputs)):
            print("i = ", i)
            pidevice.control_light(pi_outputs[i], True)
            time.sleep(5)
            pidevice.control_light(pi_outputs[i], False)
        

def backgroundscreen():
    time.sleep(30)
    # turn on background screen
    #subprocess.run(["cvlc", "-f",  "/home/pi/Pictures/Microsoft-Logo.jpg"])
    # DISPLAY=:0 /usr/bin/feh  -Y -x -q -D 5 -B black -F -Z -z -r /home/pi/Pictures
    #subprocess.run(["cvlc", "-f", "--play-and-exit", "--no-video-title-show", picfilefolder])
    subprocess.run(["/usr/bin/feh", "-Y", "-x", "-q", "-D 5", "-B black", "-F", "-Z", "-z", "-r", picfilefolder])
    #subprocess.run(["gpicview", "--display=:0", "/home/pi/Pictures/"])
    #subprocess.run(["sudo systemctl restart backgroundscreensvc.service"])


async def main():
    global videoplayingindex
    videoplayingindex = -1
    DEBOUNCE_TIME = 5 #minimum seconds between button pushes
    LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
                '-35s %(lineno) -5d: %(message)s')
    LOGGER = logging.getLogger(__name__)
        
        
    # LED strip configuration:
    LED_COUNT = 16        # Number of LED pixels.
    LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
    # LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
    LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA = 10          # DMA channel to use for generating signal (try 10)
    LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
    LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
    LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

    global LEDdevice
    # LEDdevice = led.ledcontroller(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_BRIGHTNESS, LED_INVERT, LED_CHANNEL)
    
   
    data = piSetup()
    global pi_inputs, pi_outputs
    pi_inputs = data["piinputs"]
    pi_outputs = data["pioutputs"]
    videolist = data["videolist"]
    global picfilefolder
    picfilefolder = "/home/pi/Pictures"

    global backgroundscreenactive
    backgroundscreenactive = False
    inputs = list(pi_inputs)
    outputs = list(pi_outputs)
    global pidevice
    pidevice = pi.raspberrypi(pi_inputs, pi_outputs)
    global videos
    videos = list(videolist)

    pidevice.setcallback(pi_inputs[0], processtrigger)
    pidevice.setcallback(pi_inputs[1], processtrigger)
    pidevice.setcallback(pi_inputs[2], processtrigger)
    
    # start outputs thread
    setbackground = threading.Thread(target=backgroundscreen)
    setbackground.start()
    # infinite look to wait for button pushes
    try:
        while True:
            # print(".")
            time.sleep(5)
    except KeyboardInterrupt:
        pidevice.GPIO_cleanup(pi_inputs, pi_outputs)
    # startconnect = asyncio.create_task(startprocess())
    # startconnect

    

asyncio.run(main())
