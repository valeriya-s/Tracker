import cv2
import mediapipe as mp
import time
import numpy as mafs

#######################################
#socket stuff:
import socket
UDP_IP = "10.0.0.1"
UDP_PORT = 5065

print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
##########################################

mp_drawing=mp.solutions.drawing_utils
mp_drawing_styles=mp.solutions.drawing_styles
mppose=mp.solutions.pose


cap=cv2.VideoCapture(0)
poses=mppose.Pose()

# shoulders + elbows + wrist + hips + knees + ankles
# 12 zeros
xList = mafs.zeros(12)
yList = mafs.zeros(12)
zList = mafs.zeros(12)

xBytes = 0 
yBytes = 0 
zBytes = 0 

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
        
        i = 0
        for num1 in range(11,29):
            # i dont wanna include hand shit
            if num1 in range(17, 23):
                ignore = results.pose_landmarks.landmark[mppose.PoseLandmark(num1)].x
            else:
                xList[i] = results.pose_landmarks.landmark[mppose.PoseLandmark(num1)].x
                yList[i] = results.pose_landmarks.landmark[mppose.PoseLandmark(num1)].y
                zList[i] = results.pose_landmarks.landmark[mppose.PoseLandmark(num1)].z
                i=i+1

    end = time.time()
    if (end - start > 1):
        
        start = time.time()
        end = time.time()

        for num1 in xList:
            print(str(num1))

        for num1 in yList:
            print(str(num1))


        k = 0
        print("yo")
        for numy in xList:

            xBytes = bytes(str(xList[k]),'utf-8')
            yBytes = bytes(str(yList[k]),'utf-8')
            zBytes = bytes(str(zList[k]),'utf-8')

            sock.sendto(xBytes,(UDP_IP,UDP_PORT))
            sock.sendto(yBytes,(UDP_IP,UDP_PORT))
            sock.sendto(zBytes,(UDP_IP,UDP_PORT))
            k = k + 1

    #test socket:
    # b1= bytes(str(Rankle_x),'utf-8')
    # sock.sendto(b1,(UDP_IP,UDP_PORT))

    cv2.imshow('Posetracker',image)
    cv2.waitKey(1)

