
import cv2
import numpy as np
import matplotlib as mplot
import threading
import PyQt5

cap = cv2.VideoCapture(0)

def cap_frame():
    threading.Timer(5.0, cap_frame).start()
    print("Hello, world!")

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points
objp = np.zeros((4*6, 3), np.float32)
objp[:, :2] = np.mgrid[0:6, 0:4].T.reshape(-1, 2)

# Arrays to store object points and image points from all the images
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d point in image plane
print("Hello, world!")

cap_frame()

count = 0

while (count < 10):
    ret, frame = cap.read()
    
    # Our operations on the frame come 
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# Display the resulting frame
    cv2.imshow('frame', gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
