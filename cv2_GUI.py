
'''
ECE 5725 Final Project
Name - Ishaan Thakur (it233), Shreyas Patil (sp2544)

cv2_GUI.py

Main program for starting our application and running different exercise functionalities
'''

import cv2
import os
import math
from ChestFly_Counter_mod import ChestFly_Counter
from Crunches_Counter_mod import Crunches_Counter
from Curl_Counter_mod import Curl_Counter

from Lat_Counter_mod import Lat_Counter
from Squats_Counter_mod import Squats_Counter
from util import euclidean_dist
from email_send import email_function


from collections import defaultdict
# Lists to store the bounding box coordinates
abs_pos, arms_pos, chest_pos, shoulder_pos, legs_pos = (278,192), (405,110), (300,131),(261,105), (312,330)

counter_dict = defaultdict(lambda: 0)

code_run = True
top_left_corner=[]
bottom_right_corner=[]
click_pos = []
os.environ['DISPLAY']=':0'
email_recv = 'timcook@apple.com' ## change to send it to specified email address

flag_exercise = [False for i in range(5)]

## Callback function when a mouse event is detected
def EventCallback(action, x, y, flags, *userdata):
  
  ## Global variable declaration
  global top_left_corner, bottom_right_corner, counter_dict, code_run, flag_exercise

    ## LEFT mouse button lifted up; used for detecting touch events on screen
  if action == cv2.EVENT_LBUTTONUP:
    click_pos = [(x,y)]

    if (x>0 and x<90) and (y> 300 and y<360): ## Send Email Option Selected
        str_email = ""
        if len(counter_dict) >= 1:
            for k,v in counter_dict.items():
                str_email += str(k) + " : " + str(v)+ '\n'
            email_function(email_recv, str_email) 
            counter_dict = defaultdict(lambda: 0)
            
    elif (x>550 and x<640) and (y> 300 and y<360): ## QUIT option selected
        code_run = False
        return
    

    else:
        if euclidean_dist(*click_pos[0], *chest_pos) < 20: # Chest selected
            print("DO CHEST")        
            if True not in flag_exercise:
                flag_exercise[0] = True
            
        elif euclidean_dist(*click_pos[0], *abs_pos) < 20: # Abs selected
            print("DO ABS")
            if True not in flag_exercise:
                flag_exercise[1] = True
            
        elif euclidean_dist(*click_pos[0], *shoulder_pos) < 20: #Shoulder selected
            print("DO SHOULDER")
            if True not in flag_exercise:
                flag_exercise[2] = True

        elif euclidean_dist(*click_pos[0], *arms_pos) < 20: # Arms selected
            print("DO ARMS")
            if True not in flag_exercise:
                flag_exercise[3] = True
            
        elif euclidean_dist(*click_pos[0], *legs_pos) < 20: # Legs selected
            print("DO LEGS")
            if True not in flag_exercise:
                flag_exercise[4] = True
            
        else:
            pass
    

image = cv2.imread("human.jpg") # Displaying Arnold's image
image = cv2.resize(image, (640, 480))

radius, thickness = 2, 3

color_drawn = (0,255,0)
image = cv2.circle(image, abs_pos, radius, color_drawn, thickness)
image = cv2.circle(image, arms_pos, radius, color_drawn, thickness)
image = cv2.circle(image, shoulder_pos, radius, color_drawn, thickness)
image = cv2.circle(image, chest_pos, radius, color_drawn, thickness)
image = cv2.circle(image, legs_pos, radius, color_drawn, thickness)
# Make a temporary image, will be useful to clear the drawing
temp = image.copy()
# Create a named window
cv2.namedWindow("Window")

cv2.setMouseCallback("Window", EventCallback)

k=0
cv2.namedWindow('Window')
cv2.moveWindow("Window", 100,-75)

'''
Send Email
'''
cv2.rectangle(image, (0,360), (90,300), (245,117,16), -1)
cv2.putText(image, "EMAIL",(5,345), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)

'''
Quit Button
'''
cv2.rectangle(image, (640,360), (550,300),(0,0,255) , -1)
cv2.putText(image, "QUIT",(560,345), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)

while True :
    if flag_exercise[0]:
        counter_dict['CHEST'] += ChestFly_Counter()
        flag_exercise[0] = False
        
    elif flag_exercise[1]:
        counter_dict['ABS'] += Crunches_Counter()
        flag_exercise[1] = False

    elif flag_exercise[2]:
        if counter_dict['SHOULDER'] == 0:
            counter_dict['SHOULDER'] = Lat_Counter()
        else:
            ls_cnter = Lat_Counter()
            counter_dict['SHOULDER'][0] += ls_cnter[0]
            counter_dict['SHOULDER'][1] += ls_cnter[1]
        flag_exercise[2] = False

    elif flag_exercise[3]:
        if counter_dict['ARMS'] == 0:
            counter_dict['ARMS'] = Curl_Counter()
        else:
            ls_cnter = Curl_Counter()
            counter_dict['ARMS'][0] += ls_cnter[0]
            counter_dict['ARMS'][1] += ls_cnter[1]
        flag_exercise[3] = False

    elif flag_exercise[4]:
        counter_dict['LEGS'] += Squats_Counter()
        flag_exercise[4] = False

    else:
        pass
    

    
    k = cv2.waitKey(1) & 0XFF == ord('q') # Needed for displaying every instance of image frame
    
    cv2.imshow("Window", image)
    if not code_run:
        
        break

cv2.destroyAllWindows() # close all cv2 Window instances


