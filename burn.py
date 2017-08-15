""" 
    Tucker Shannon - 7/14/2017 
    CNC Wood burning program for RaspberryPi
    This python program converts images into an Archimedes spiral type wood burning art made by varying
    the speed of rotation of a spinning platform with a wood burning pen.

"""

import RPi.GPIO as gpio 

import numpy
from math import cos, sin, pi
from PIL import Image, ImageDraw, ImageSequence
import cv2
import time


gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
gpio.setup(23, gpio.OUT)
gpio.setup(24, gpio.OUT)
gpio.setup(22, gpio.OUT)
gpio.setup(27, gpio.OUT)
gpio.setup(18, gpio.OUT)
gpio.setup(4,gpio.OUT)
gpio.setup(5,gpio.OUT)
gpio.output(4,True)
gpio.output(5,True)
count = 0




##################################################
# Asks user for input to center the motors
##################################################
def centerMotor(*args):
    while True:
t      
        print "Type 'l' to move buner left, 'r' to move right,'s' to spin the platform or, 'q' to begin burning."
        char = raw_input('l,r,or q:')
       
    
        if char == "l":
            rot = raw_input('rotations: ')
            for x in range(0,int(rot)*200):
                step(2,1,0.001)
                step(1,1,0.001)
            
        
        if char == "r":
            rot = raw_input('rotations: ')
            for x in range(0,int(rot)*200):
                step(2,2,0.001) 
                step(1,1,0.001)
            
        if char == "s":
            for x in range(0,10000):
  
                step(1,1,0.001)

        if char == "q":
            break


##################################################
# function for driving stepper motor with a motor number,
# rotation direction, time, and a bool for moving both motors
##################################################
def step(motor,direction,t,move=False):
    
   
    if motor == 1:
        if move == True:
            gpio.output(5,False)
            gpio.output(27,False)
        gpio.output(4,False)
        if direction == 1:
            gpio.output(24,True)
        if direction == 2:
            gpio.output (24,False)
        
        
        if move == True:
            gpio.output(22,True)
        gpio.output(23,True)
        time.sleep(t)
        if move == True:
            gpio.output(22,False)
        gpio.output(23,False)



    if motor == 2:
        gpio.output(5,False)
        if direction == 1:
            gpio.output(27,True)
        if direction == 2:
            gpio.output (27,False)
        gpio.output(22,True)
        time.sleep(t)
        gpio.output(22,False)
        gpio.output(5,True)




##################################################
#   Plot the image array onto wood 
##################################################		


def plot_spiral(parray,speed):
	theta = 0 #setting initial theta to 0
	r = 1 #intital radius
        maxInt = numpy.amax(parray)+1 #finding the max integer in the photo array
	(x_limit,y_limit) = parray.shape #finding the x and y limits of the shape
	stepCount = 0 #used as a counter for each motor step
        speed = .00002/speed 
        sleeptime = speed*pi*r*(maxInt-int(parray[1,1]))

	while True: #runs until you manually stop the program (ctrl-c)
            r = r + 20.0 * float(1)/(1200*4) #incrementing the radius (1200 because 1-6 gear ratio and 200 steps per revolution on stepper)*4 because im micro stepping
            theta = theta + (2*pi)/(1200*4) #incrementing theta 
            stepCount = stepCount + 1 
            x = x_limit/2 + int(r*cos(theta))
            y = y_limit/2 + int(r*sin(theta))
            if x >0 and x < x_limit and y > 0 and y<y_limit: #check to make sure we're within the boundaries
                print maxInt-int(parray[x,y]) #print the darkness (10 being most dark)
                #set the sleep time to the integer and x , y cordinate
                #the larger the integer the slower the burn tool moves
                sleep = speed*pi*r*(maxInt-int(parray[x,y]))
                if sleeptime > sleep:
                    sleeptime = sleeptime * 0.9
                else:
                    sleeptime = sleep

                if (stepCount % 25) == 0:
                    step(1,1,sleeptime,True)
                else:
                    step(1,1,sleeptime)
            else: 
                sleep = speed*pi*r
                if (stepCount % 25) == 0:
                    step(1,1,sleeptime,True)
                else:
                    step(1,1,sleeptime)


       
##################################################
#   function to convert photo into a numppy array of of darkness scale 1-10
##################################################				
        
def get_photo_array(width,photoName):
    image = Image.open(photoName)
    ratio = float(image.size[1])/image.size[0]
    sizex = width
    sizey = int(round(ratio * sizex))
    pic = image.resize((sizex,sizey))
    r, g, b = pic.split()
    im = numpy.array(g)
    scale = 9
    im = im/(256/(scale))
    im = numpy.around(im, decimals=0, out=None)
    photoarray = numpy.zeros([sizex,sizey])
    for num in range(0,numpy.size(im,1)):
                 for num2 in range(0,numpy.size(im,0)):
                    photoarray[num][num2] = int(im[num2,num])
                                 
    return photoarray











if __name__== '__main__':

        
        print "Save image as 'burn.jpg'. Silhouettes work best"
        centerMotor()
	photoName = "burn.jpg" #name of photo to convert
        outputWidth = 2000 #how wide the output will be
         
	photoarray = get_photo_array(outputWidth,photoName)
        
        speed = 20 #setting an arbitrary rotation speed
        plot_spiral(photoarray,speed)
 
    

