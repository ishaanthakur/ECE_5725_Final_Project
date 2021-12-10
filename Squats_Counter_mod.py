'''
ECE 5725 Final Project
Name - Ishaan Thakur (it233), Shreyas Patil (sp2544)

Squats_Counter_mod.py
'''
import cv2
import mediapipe as mp
import numpy as np

from util import calculate_angle


mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


def Squats_Counter():

    flag_exit = False

    def WindowCloseCallback(action, x, y, flags, *userdata):
        nonlocal flag_exit
        if action == cv2.EVENT_LBUTTONUP:
            
            if ((x >500 and x<640) and (y>300 and y<360 )):
                print('QUIT')
                flag_exit = True

    cap = cv2.VideoCapture(0)

    counter = 0
    stage = None
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
                # shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                # elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                # wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

                left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                # Calculate angle
                
                angle_squat_left = calculate_angle(left_hip, left_knee, left_ankle)
                

                cv2.putText(image, str(angle_squat_left),
                            tuple(np.multiply(left_knee, [640, 360]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                    )


                if angle_squat_left > 130:
                    stage = "squat"
                if angle_squat_left < 120 and stage =='squat':
                    stage="straight"
                    counter +=1
                    

            except:
                pass

            # Render squats counter
            
            cv2.rectangle(image, (0,0), (225,73), (204, 0, 153), -1)

            # Rep data
            cv2.putText(image, 'SQUATS', (15,14),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, str(counter),
                        (10,60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)

            # Stage data
            cv2.putText(image, 'STAGE', (85,14),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)

            disp_stage = 'straight'
            if stage == 'straight':
                disp_stage = 'squat'
            cv2.putText(image, disp_stage,
                        (60,60),
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

            cv2.imshow('Squats_Window', image)
            cv2.setMouseCallback('Squats_Window', WindowCloseCallback)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if flag_exit:
                break
        cap.release()
        cv2.destroyWindow('Squats_Window')
    return counter
