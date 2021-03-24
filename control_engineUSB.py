import pygame
import sys
import os
import time
os.environ["SDL_VIDEODRIVER"] = "dummy"
pygame.init()

#gpio init motor 1
in1 = 36
in2 = 38
ena = 40
GPIO.setmode(GPIO.BOARD)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(ena, GPIO.OUT)
GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
pwm1 = GPIO.PWM(ena, 100)
pwm1.start(0)


import RPi.GPIO as GPIO
#gpio init motor 2
in3 = 11
in4 = 13
enb = 15


GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)
GPIO.setup(enb, GPIO.OUT)
GPIO.output(in3, GPIO.LOW)
GPIO.output(in4, GPIO.LOW)
pwm2 = GPIO.PWM(enb, 100)
pwm2.start(0)
#enable pygame
pygame.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()


def split_axis(x_axis):
    x_axis = x_axis*100
    left_motor_speed = 0
    right_motor_speed = 0
    #change axis here to change motors place
    if x_axis < 0:
        left_motor_speed = abs(x_axis)
       
    if x_axis > 0:
        right_motor_speed = abs(x_axis)
    if left_motor_speed == 100: left_motor_speed = 99


   
        
    if left_motor_speed !=0 or right_motor_speed != 0:
        if left_motor_speed == 0: left_motor_speed = 100 - right_motor_speed
        if right_motor_speed == 0: right_motor_speed = 100 - left_motor_speed
    return left_motor_speed, right_motor_speed


def get_direction(motor_speed):
    direction = 0
    if motor_speed < 0: direction = -1
    if motor_speed > 0: direction = 1
    return direction

def change_pwm_motors(left_motor_speed,right_motor_speed):
   
    left_motor_speed = int(abs(left_motor_speed))
    right_motor_speed = int(abs(right_motor_speed))

    pwm1.ChangeDutyCycle(left_motor_speed)
    pwm2.ChangeDutyCycle(right_motor_speed)

# Main loop.
while True:
   
    #get events from the queue
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            pygame.quit()
   #read joystick axis 
    x_axis = joystick.get_axis(0)
    y_axis = joystick.get_axis(1) * -1
    print(f"axisX:{x_axis}, axisY: {y_axis}")
    speed = y_axis
    left_motor_speed, right_motor_speed = split_axis(x_axis)
    # speed on y axis influence speed of motors
    
    left_motor_speed = left_motor_speed * speed
    right_motor_speed = right_motor_speed * speed
    
    if x_axis == 0:
        left_motor_speed  =  100 * speed
        right_motor_speed =  100 * speed


    change_pwm_motors(left_motor_speed,right_motor_speed)
    right_motor_direction = get_direction(right_motor_speed)
    left_motor_direction = get_direction(left_motor_speed)
        
    print(f"right_motor_speed: {right_motor_speed}")
    print(f"left_motor_speed: {left_motor_speed}")
      
    print(f"right_motor_direction: {right_motor_direction}")
    print(f"left_motor_direction: {left_motor_direction}")
    # turn on left motor when user want to move right
    if left_motor_speed > 0:
         GPIO.output(in1,GPIO.HIGH)
         GPIO.output(in2,GPIO.LOW)
        
  
    if left_motor_speed < 0:
         GPIO.output(in1,GPIO.LOW)
         GPIO.output(in2,GPIO.HIGH)
    
    # turn on right motor when user want to move left
    if right_motor_speed > 0:
         GPIO.output(in3,GPIO.LOW)
         GPIO.output(in4,GPIO.HIGH)
    if right_motor_speed < 0:
         GPIO.output(in4,GPIO.LOW)
         GPIO.output(in3,GPIO.HIGH)
    #clear pins when speed = 0      
    if right_motor_direction == 0:
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
    if left_motor_direction == 0:
        GPIO.output(in3, GPIO.LOW)
        GPIO.output(in4, GPIO.LOW)
        
    # Pause for half a second.
    time.sleep(0.5)