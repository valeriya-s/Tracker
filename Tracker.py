import cv2
import mediapipe as mp
import time
import numpy as mafs
import math

#######################################
#socket stuff:
import socket
UDP_IP = "10.0.0.140"
UDP_PORT = 5065

print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
##########################################

def calculateAngle(landmark1, landmark2, landmark3):
    '''
    This function calculates angle between three different landmarks.
    Args:
        landmark1: The first landmark containing the x,y and z coordinates.
        landmark2: The second landmark containing the x,y and z coordinates.
        landmark3: The third landmark containing the x,y and z coordinates.
    Returns:
        angle: The calculated angle between the three landmarks.

    '''

    # Get the required landmarks coordinates.
    x1 = landmark1.x
    y1 = landmark1.y
    x2 = landmark2.x
    y2 = landmark2.y
    x3 = landmark3.x
    y3 = landmark3.y
    # x2, y2, _, _ = landmark2
    # x3, y3, _, _ = landmark3

    # Calculate the angle between the three points
    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
    
    # Check if the angle is less than zero.
    if angle < 0:

        # Add 360 to the found angle.
        angle += 360
    
    # Return the calculated angle.
    return angle


mp_drawing=mp.solutions.drawing_utils
mp_drawing_styles=mp.solutions.drawing_styles
mppose=mp.solutions.pose


cap=cv2.VideoCapture(0)
poses=mppose.Pose()

# Timer So Everything doesn't fly at a million miles an hour  
start = time.time()

while True:
    data,image=cap.read()
    image=cv2.cvtColor(cv2.flip(image,1),cv2.COLOR_BGR2RGB)

    results=poses.process(image)
    image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)

    if results.pose_landmarks:
        # for landmarks in results.pose_landmarks:
        mp_drawing.draw_landmarks(image,results.pose_landmarks,mppose.POSE_CONNECTIONS)
        
        # print(results.pose_landmarks.landmark[mppose.PoseLandmark.LEFT_WRIST.value]) 
        left_elbow_angle = calculateAngle(results.pose_landmarks.landmark[mppose.PoseLandmark.LEFT_SHOULDER.value],
                                        results.pose_landmarks.landmark[mppose.PoseLandmark.LEFT_ELBOW.value],
                                        results.pose_landmarks.landmark[mppose.PoseLandmark.LEFT_WRIST.value])

        # Get the angle between the right shoulder, elbow and wrist points. 
        right_elbow_angle = calculateAngle(results.pose_landmarks.landmark[mppose.PoseLandmark.RIGHT_SHOULDER.value],
                                        results.pose_landmarks.landmark[mppose.PoseLandmark.RIGHT_ELBOW.value],
                                        results.pose_landmarks.landmark[mppose.PoseLandmark.RIGHT_WRIST.value])   
        
        # Get the angle between the left elbow, shoulder and hip points. 
        left_shoulder_angle = calculateAngle(results.pose_landmarks.landmark[mppose.PoseLandmark.LEFT_ELBOW.value],
                                        results.pose_landmarks.landmark[mppose.PoseLandmark.LEFT_SHOULDER.value],
                                        results.pose_landmarks.landmark[mppose.PoseLandmark.LEFT_HIP.value])

        # Get the angle between the right hip, shoulder and elbow points. 
        right_shoulder_angle = calculateAngle(results.pose_landmarks.landmark[mppose.PoseLandmark.RIGHT_HIP.value],
                                        results.pose_landmarks.landmark[mppose.PoseLandmark.RIGHT_SHOULDER.value],
                                        results.pose_landmarks.landmark[mppose.PoseLandmark.RIGHT_ELBOW.value])

        # Get the angle between the left shoulder, hip, and knee points. 
        left_hip_angle = calculateAngle(results.pose_landmarks.landmark[mppose.PoseLandmark.LEFT_SHOULDER.value],
                                        results.pose_landmarks.landmark[mppose.PoseLandmark.LEFT_HIP.value],
                                        results.pose_landmarks.landmark[mppose.PoseLandmark.LEFT_KNEE.value])

        # Get the angle between the right shoulder, hip, and knee points. 
        right_hip_angle = calculateAngle(results.pose_landmarks.landmark[mppose.PoseLandmark.RIGHT_SHOULDER.value],
                                        results.pose_landmarks.landmark[mppose.PoseLandmark.RIGHT_HIP.value],
                                        results.pose_landmarks.landmark[mppose.PoseLandmark.RIGHT_KNEE.value])
        
        # Get the angle between the left hip, knee and ankle points. 
        left_knee_angle = calculateAngle(results.pose_landmarks.landmark[mppose.PoseLandmark.LEFT_HIP.value],
                                        results.pose_landmarks.landmark[mppose.PoseLandmark.LEFT_KNEE.value],
                                        results.pose_landmarks.landmark[mppose.PoseLandmark.LEFT_ANKLE.value])

        # Get the angle between the right hip, knee and ankle points 
        right_knee_angle = calculateAngle(results.pose_landmarks.landmark[mppose.PoseLandmark.RIGHT_HIP.value],
                                        results.pose_landmarks.landmark[mppose.PoseLandmark.RIGHT_KNEE.value],
                                        results.pose_landmarks.landmark[mppose.PoseLandmark.RIGHT_ANKLE.value])


    end = time.time()
    if (end - start > 0.05):
        
        start = time.time()
        end = time.time()

        # for num1 in xList:
        #     print(str(num1))

        k = 0
        print(left_hip_angle)
        print(right_hip_angle)

        #test socket:
        b1= bytes(str(left_elbow_angle),'utf-8')
        b2= bytes(str(right_elbow_angle),'utf-8')
        b3= bytes(str(left_shoulder_angle),'utf-8')
        b4= bytes(str(right_shoulder_angle),'utf-8')
        b5= bytes(str(left_hip_angle),'utf-8')
        b6= bytes(str(right_hip_angle),'utf-8')
        b7= bytes(str(left_knee_angle),'utf-8')
        b8= bytes(str(right_knee_angle),'utf-8')

        sock.sendto(b1,(UDP_IP,UDP_PORT))
        sock.sendto(b3,(UDP_IP,UDP_PORT))
        sock.sendto(b5,(UDP_IP,UDP_PORT))
        sock.sendto(b7,(UDP_IP,UDP_PORT))
        sock.sendto(b2,(UDP_IP,UDP_PORT))
        sock.sendto(b4,(UDP_IP,UDP_PORT))
        sock.sendto(b6,(UDP_IP,UDP_PORT))
        sock.sendto(b8,(UDP_IP,UDP_PORT))


    cv2.imshow('Posetracker',image)
    cv2.waitKey(1)
