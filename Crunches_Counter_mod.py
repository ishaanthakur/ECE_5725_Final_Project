
'''
ECE 5725 Final Project
Name - Ishaan Thakur (it233), Shreyas Patil (sp2544)

Crunches_Counter_mod.py
'''

import cv2
import mediapipe as mp
import numpy as np
import time

from util import calculate_angle
def Crunches_Counter() -> int:
    flag_exit = False

    def WindowCloseCallback(action, x, y, flags, *userdata):
        nonlocal flag_exit
        if action == cv2.EVENT_LBUTTONUP:
            if ((x >500 and x<640) and (y>300 and y<360 )):
                print('QUIT')
                flag_exit = True


    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    cap = cv2.VideoCapture(0)

    counter = 0
    stage = None
    currTime = 0
    ## Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            frame = cv2.resize(frame, (640, 360))
            frame_rate = time.time() - currTime
            
            currTime = time.time()
            # Recolor image to RGB
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
                left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]

                # Calculate angle
                angle = calculate_angle(left_knee, left_hip, left_shoulder)

                # Visualize angle
                cv2.putText(image, str(angle),
                            tuple(np.multiply(left_hip, [640, 360]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                    )

                # Crunches counter logic
                if angle > 90:
                    stage = "down"
                if angle < 80 and stage =='down':
                    stage="up"
                    counter +=1
                    

            except:
                pass

            # Render crunches counter
            # Setup status box
            cv2.rectangle(image, (0,0), (225,73), (204, 0, 153), -1)

            # Rep data
            cv2.putText(image, 'REPS', (15,14),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, str(counter),
                        (10,60),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)

            # Stage data
            cv2.putText(image, 'STAGE', (65,14),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, stage,
                        (65,60),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)

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

            cv2.imshow('Crunches_Window', image)
            cv2.setMouseCallback('Crunches_Window', WindowCloseCallback)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if flag_exit:
                break
        cap.release()
        cv2.destroyWindow('Crunches_Window')
    return counter
