'''
ECE 5725 Final Project
Name - Ishaan Thakur (it233), Shreyas Patil (sp2544)

util.py
'''

import numpy as np
import math

def calculate_angle(a,b,c): ## Angle calculation between three landmarks
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End

    rad = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angl = np.abs(rad*180.0/np.pi)
    if angl >180.0:
        angl = 360-angl

    return angl

def euclidean_dist(x1, y1, x2, y2): # euclidean distance calculation between two points 
    return math.sqrt((y1-y2)**2 + (x1-x2)**2)

def euclidean_dist_exercise(a,b): # euclidean distance calculation between 2 points in image frame
    a = np.array(a) # Left
    b = np.array(b) # Right
    a[0] = a[0] * 640
    b[0] = b[0] * 640
    a[1] = a[1] * 360
    b[1] = b[1] * 360
    dist = np.sqrt(np.power((a[1]-b[1]), 2) + np.power((a[0]-b[0]), 2))
    return dist
