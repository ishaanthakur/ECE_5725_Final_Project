
'''
ECE 5725 Final Project
Name - Ishaan Thakur (it233), Shreyas Patil (sp2544)

Curl_Counter_mod.py
'''

import cv2
import mediapipe as mp
import numpy as np

from util import calculate_angle

def Curl_Counter() -> list:
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

    left_counter, right_counter = 0, 0
    left_stage, right_stage = None, None
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
                left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

                right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

                # Calculate angle
                left_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
                right_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)

                # Visualize angle
                cv2.putText(image, str(left_angle),
                            tuple(np.multiply(left_elbow, [640, 360]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                    )

                cv2.putText(image, str(right_angle),
                            tuple(np.multiply(right_elbow, [640, 360]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                    )

                # Curl counter logic
                if left_angle > 160:
                    left_stage = "down"
                if left_angle < 30 and left_stage =='down':
                    left_stage="up"
                    left_counter +=1
                    

                if right_angle > 160:
                    right_stage = "down"
                if right_angle < 30 and right_stage =='down':
                    right_stage="up"
                    right_counter +=1
                    
                print(left_counter, right_counter)
            except:
                pass

            # Render curl counter
            # Setup status box
            
            
            cv2.rectangle(image, (0,0), (225,73), (204, 0, 153), -1)
            cv2.rectangle(image, (640,0), (415,73), (204, 0, 153), -1)

            # Rep data
            cv2.putText(image, 'REPS', (15,12),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, str(left_counter),
                        (10,60),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)

            cv2.putText(image, 'REPS', (440,12),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, str(right_counter),
                        (440,60),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)

            # Stage data
            cv2.putText(image, 'STAGE', (65,12),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, left_stage,
                        (60,60),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)

            cv2.putText(image, 'STAGE', (485,12),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, right_stage,
                        (485,60),
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

            cv2.imshow('Curl_Window', image)
            cv2.setMouseCallback('Curl_Window', WindowCloseCallback)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if flag_exit:
                break
        cap.release()
        cv2.destroyWindow('Curl_Window')
    return [left_counter, right_counter]
