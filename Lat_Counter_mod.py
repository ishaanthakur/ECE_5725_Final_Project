'''
ECE 5725 Final Project
Name - Ishaan Thakur (it233), Shreyas Patil (sp2544)

Lat_Counter_mod.py
'''

from typing import Tuple
import cv2
import mediapipe as mp
import numpy as np


import time

from util import calculate_angle


def Lat_Counter() -> list:
    flag_exit = False

    def WindowCloseCallback(action, x, y, flags, *userdata):
        nonlocal flag_exit
        if action == cv2.EVENT_LBUTTONUP:
            
            if ((x >500 and x<640) and (y>300 and y<360 )):
                print('QUIT')
                flag_exit = True

    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    init_time = time.time()
    cap = cv2.VideoCapture(0)

    counter_left, counter_right = 0, 0
    stage_left, stage_right = None, None
    ## Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():

            ret, frame = cap.read()

            # Recolor image to RGB
            frame = cv2.resize(frame, (640, 360))
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # Make detection
            results = pose.process(image)

            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark

                # Get coordinates


                left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]

                right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]

                # Calculate angle
                angle_lat_left = calculate_angle(left_hip, left_shoulder, left_elbow)
                angle_lat_right= calculate_angle(right_hip, right_shoulder, right_elbow)

                # # Visualize angle


                cv2.putText(image, str(angle_lat_left),
                            tuple(np.multiply(left_shoulder, [640, 360]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                    )

                cv2.putText(image, str(angle_lat_right),
                            tuple(np.multiply(right_shoulder, [640, 360]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                    )

                # Lat raise counter logic

                if angle_lat_left > 50:
                    stage_left = "UP"
                if angle_lat_left < 30 and stage_left =='UP':
                    stage_left="DOWN"
                    counter_left +=1



                if angle_lat_right > 50:
                    stage_right = "UP"
                if angle_lat_right < 30 and stage_right =='UP':
                    stage_right="DOWN"
                    counter_right +=1

                print(counter_left, counter_right)
            except:
                pass

            # Render lat counter
            
            cv2.rectangle(image, (0,0), (225,73), (204, 0, 153), -1)
            # Rep data
            cv2.putText(image, 'LEFT RAISE', (15,12),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, str(counter_left),
                        (10,60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)

            # Stage data
            cv2.putText(image, 'STAGE', (150,12),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)



            cv2.rectangle(image, (640,0), (415,73), (204, 0, 153), -1)



            # Rep data
            cv2.putText(image, 'RIGHT RAISE', (440,12),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, str(counter_right),
                        (440,60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)

            # Stage data
            cv2.putText(image, 'STAGE', (565,12),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)



            cv2.putText(image, stage_left,
                        (125,60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)

            cv2.putText(image, stage_right,
                        (540,60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)

            '''
            Quit Button
            '''
            cv2.rectangle(image, (640,360), (500,300), (0,0,255), -1)
            cv2.putText(image, "QUIT",(510,345), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)


            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(67,246,157), thickness=2, circle_radius=2),
                                    mp_drawing.DrawingSpec(color=(246,234,67), thickness=2, circle_radius=2)
                                    )

            cv2.namedWindow('Lat_Window')
            cv2.moveWindow('Lat_Window', 0,0)
            cv2.imshow('Lat_Window', image)

            cv2.setMouseCallback('Lat_Window', WindowCloseCallback)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if flag_exit:
                break
        cap.release()
        cv2.destroyWindow('Lat_Window')
    return [counter_left, counter_right]
