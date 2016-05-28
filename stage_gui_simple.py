#!/usr/bin/env python

import time
import picamera
import fractions

camera = picamera.PiCamera()
camera.led = False

def init_camera(w,h):
    #camera.resolution = (1920,1080)
    #camera.resolution = (1296, 972)
    camera.resolution = (w, h)
    camera.start_preview()
    #camera.window = (200, 0, 1296, 972)
    camera.annotate_text = 'Hello world! (%s,%s)'%(w,h)
    # picamera example setting fixed awb
    time.sleep(2)
    # Now fix the values
    #camera.shutter_speed = camera.exposure_speed
    #camera.exposure_mode = 'off'
    g = camera.awb_gains
    print(g)
    #g = (fractions.Fraction(203,128), fractions.Fraction(275, 256))
    camera.awb_mode = 'off'
    camera.awb_gains = g
print("start!")


import serial
import os, sys, pygame

pygame.joystick.init()

WHITE = 255,255,255
GREEN = 0,255,0
BLACK = 0,0,0
BLUE  = 0,0,255
RED   = 255,0,0

#size = width, height = 340, 410
#size= width,height = 800,600
#size = width, height = 1920, 1080
#size = width, height = 

#size = pygame.display.get_mode()
#screen = pygame.display.set_mode(size)
#pygame.display.init()
print("set mode")
screen = pygame.display.set_mode((0,0)) # use current resolution
print("info")
info = pygame.display.Info()
print info

print screen
pygame.display.set_caption("pygame.draw functions ~ examples")
pygame.init()

init_camera(info.current_w, info.current_h)

#draw a few rectangles
#rect2 = pygame.draw.rect(screen, WHITE, (100,20,60,60),3) # not filled

"""
#draw a few circles
circ1 = pygame.draw.circle(screen, WHITE, (50,180), 30, 0) #filled
circ2 = pygame.draw.circle(screen, WHITE, (130,180), 30, 3) #filled

#draw an ellipse
ellipse1 = pygame.draw.ellipse(screen, WHITE, (20,220,140,60), 3)

#draw a few arcs
arc1 = pygame.draw.arc(screen, WHITE, (20,290,60,60),deg(0), deg(90), 3)
arc2 = pygame.draw.arc(screen, WHITE, (100,290,60,60),deg(90), deg(270), 3)

#draw a few lines
for n in range(5):
    pygame.draw.line(screen, WHITE, (20,350+(10*n)), (100,350), 2)
    pygame.draw.line(screen, GREEN, (20,390), (100,350+(10*n)), 2)

#draw a few anti aliased lines
for n in range(5):
    pygame.draw.aaline(screen, WHITE, (120,390), (250,350+(10*n)), 1)

#draw a few aaline sequences
CLOSED = 1
OPEN = 0
points=[]
points.append((180,100))
points.append((240,100))
points.append((240,160))
points.append((180,160))
pygame.draw.aalines(screen, GREEN, OPEN, points, 1)    
points.append((260,100))
points.append((320,100))
points.append((320,160))
points.append((260,160))
pygame.draw.aalines(screen, GREEN, CLOSED, points, 1)    
"""

#Lets create some text. We could use a loop, but lets keep it simple
font = pygame.font.Font(None, 20)

def draw_text(text="default",xy=(0,0),color=WHITE,size=1):
    fontimg1 = font.render(text,size,color)
    screen.blit(fontimg1, xy)

import serial
ser = None
for n in range(3):
    try:
        c = "COM4"
        c = "/dev/serial/by-id/usb-Teensyduino_USB_Serial_267660-if00"
        ser = serial.Serial(c, timeout = 0)  # open first serial port
        print (ser.name)          # check which port was really used
        #ser.write(b"hello")      # write a string
        break
    except Exception, e:
        print e
        time.sleep(1)

pygame.key.set_repeat(500,1) # lazy

def clamp(v,l,h):
    if v<l: return l
    if v > h: return h
    return v

class Stage(object):
    xd,yd,zd = 0,0,0
    mult = 1
    def clamp_move(self):
        self.xd = clamp(self.xd,0,33*256*6)
        self.yd = clamp(self.yd,0,33*256*6)
    def move_rel(self, rel):
        self.xd+=rel[0]*self.mult
        self.yd+=rel[1]*self.mult
        if len(rel) >= 3:
            self.zd+=rel[2]*self.mult
        if len(rel) >= 4:
            self.mult*=rel[3]
            self.mult = int(self.mult)
            if self.mult < 1: self.mult = 1
        self.clamp_move()
    
    def move_abs(self, rel):
        self.xd=rel[0]*self.mult
        self.yd=rel[1]*self.mult
        if len(rel)>=3:
            self.zd=rel[2]*self.mult
        if len(rel) >= 4:
            self.mult=rel[3]
        self.clamp_move()
    last_t = 0

    def info_str(self):
        return "%s,%s,%s *%s"%(self.xd,self.yd,self.zd,self.mult)

    def draw(self):
        if 0:
            rect1 = pygame.draw.rect(screen, BLACK, (0,0,260,260),0) #filled = 0
            
            draw_text("Place: %s,%s,%s "%(self.xd,self.yd,self.zd), (20,20))
        t=pygame.time.get_ticks()
        dt = self.last_t-t
        self.last_t = t

        camera.annotate_text = self.info_str()
        
        if (0):
            self.xd+=1
            if self.xd>100:
                self.xd = 0
                self.yd+=1
        ttl = 0
        data = " "

        full_read_size = 1024*8
        count = 0
        while ser != None: #while
            try:
                data = ser.read(full_read_size)
            except serial.serialutil.SerialException, e:
                print e
                #break
                # device reports readiness to read but returned no data (device disconnected?)
                break
            ttl+=len(data)
            if len(data)<full_read_size:
                break
            count+=1
            if count > 4:
                print "too much data"
                break
            #print(data)
        #print(ttl)
        
        if ser != None: ser.write(str.encode("ag%s bg%s cg%s E9500 "%(self.xd,self.yd,self.zd)))

# optionally flip x,y
dx = -1
dy = -1
key_move = {pygame.K_KP4:(-dx,0), pygame.K_KP6:(dx,0), pygame.K_KP2:(0,-dy), pygame.K_KP8:(0,dy), pygame.K_KP_PLUS:(0,0,1), pygame.K_KP_MINUS:(0,0,-1)
    , pygame.K_KP_MULTIPLY:(0,0,0,2), pygame.K_KP_DIVIDE:(0,0,0,0.5)}
main_stage = Stage()

import datetime
import math
import random

def dither(value):
    i = math.floor(value)
    f = value-i
    if random.random()>f:
        return i
    else:
        return i+1
    return value,i,f

def do_joystick():
    joystick_count = pygame.joystick.get_count()
    #print ("joystick_count %s"%(joystick_count))
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        #print(joystick.get_name())
        axes = joystick.get_numaxes()
        #print("axes = %s"%(axes))
        for i in range( axes ):
            axis = joystick.get_axis( i )
        buttons = joystick.get_numbuttons()
        #print("buttons = %s"%(buttons))
        for i in range( buttons ):
            #print(i)
            button = joystick.get_button( i )
        if joystick.get_button( 5 ):	#rb
            mult = 256
            zmult = 4
            x = joystick.get_axis( 0 )*mult
            y = -joystick.get_axis( 1 )*mult
            z = joystick.get_axis( 4 )*zmult
            #print((x,y,z))
            main_stage.move_rel((dither(x),dither(y),dither(z)))


def capture_image(vp = True):
    desc = "VideoFrame"
    if not vp: desc = "Still"
    date_time = datetime.datetime.now()
    fn = "Capture-%s-%s-%s.jpg"%(date_time, main_stage.info_str(), desc)
    print(fn)
    camera.annotate_text = ""
    camera.capture(fn, use_video_port=vp)

try:
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                sys.exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #print("mouse %s %s"%(event.pos,event.button))
                main_stage.move_abs(event.pos)
            elif event.type == pygame.MOUSEMOTION:
                #print("mouse move %s %s"%(event.pos,event.buttons))
                if event.buttons[0]:
                    main_stage.move_abs(event.pos)
                if event.buttons[2]:
                    main_stage.move_abs((main_stage.xd,main_stage.yd,event.pos[1]))
            elif event.type == pygame.KEYDOWN:
                #print ("key:%s"%event.key)
                if event.key in key_move.keys():
                    main_stage.move_rel(key_move[event.key])
                
                if event.key == pygame.K_KP7:
                    capture_image(True) # fast/video port image capture
                if event.key == pygame.K_KP1:
                    capture_image(False)

                if event.key == pygame.K_ESCAPE:
                    pygame.display.quit()
                    sys.exit(0)
        
        do_joystick()
        main_stage.draw()
        #pygame.display.update()
        main_stage.move_rel((0,0))
        #pygame.time.delay(1)

finally:
    ser.close()             # close port
    camera.close()
    
