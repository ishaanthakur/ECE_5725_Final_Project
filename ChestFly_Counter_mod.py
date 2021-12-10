'''
ECE 5725 Final Project
Name - Ishaan Thakur (it233), Shreyas Patil (sp2544)

ChestFly_Counter_mod.py
'''

import cv2
import mediapipe as mp
import numpy as np

from util import euclidean_dist_exercise

def ChestFly_Counter() -> int:
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
    stage_left = ""
    ## Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            frame = cv2.resize(frame, (640, 360))
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

                left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                right_wrist =  [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                
                # Calculate distance
                dist = euclidean_dist_exercise(left_wrist, right_wrist)

                # # Visualize angle

                cv2.putText(image, str(dist),
                            tuple(np.multiply(left_wrist, [640, 360]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                    )


                # Lat raise counter logic

                if dist > 250:
                    stage_left = "WIDE"
                if dist < 100 and stage_left =='WIDE':
                    stage_left="CLOSE"
                    counter +=1

            except:
                pass

            # Render chest counter
            # Setup status box
            cv2.rectangle(image, (0,0), (225,73), (204, 0, 153), -1)

            # Rep data
            cv2.putText(image, 'CNT', (15,14),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, str(counter),
                        (10,60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)

            # Stage data
            cv2.putText(image, 'STAGE', (65,14),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)


            cv2.putText(image, stage_left,
                        (65,60),
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

            cv2.imshow('ChestFly_Window', image)
            cv2.setMouseCallback('ChestFly_Window', WindowCloseCallback)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if flag_exit:
                break
        cap.release()
        cv2.destroyWindow('ChestFly_Window')
    return counter
