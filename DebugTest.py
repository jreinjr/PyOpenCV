
import numpy as np
import cv2
import threading


cap = cv2.VideoCapture(0)
frame = None
capturing = True
undistorted = False

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points
objp = np.zeros((4*6, 3), np.float32)
objp[:, :2] = np.mgrid[0:6, 0:4].T.reshape(-1, 2)

# Arrays to store object points and image points from all the images
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d point in image plane

count = 0
cap_freq = 30
tick = 0

# Camera undistortion matrix
mtx = None
dist = None

print("Capturing chessboards in 10 images.")
while True:
    # Read the current frame
    ret, frame = cap.read()

    if capturing:
        # Capture chessboards in 10 images
        if count < 10:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Find the chessboard corners
            ret, corners = cv2.findChessboardCorners(gray, (4,6), None)
            if ret == True:
                tick += 1
                # Draw and display the corners
                cv2.drawChessboardCorners(frame, (4,6), corners, ret)
                # Capture a photo every cap_freq loops
                if (tick > cap_freq):
                    objpoints.append(objp)
                    cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
                    imgpoints.append(corners)
                    count += 1
                    print(count + " images captured.")
                    tick = 0
        # Once we capture 10 chessboards
        else:
            print("Capture complete. Calibrating.")
            imageSize = frame.shape[:-1]
            ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, imageSize, None, None)
            h, w = frame.shape[:2]
            newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 0, (w,h))
            capturing = False
            undistorted = True
   
    if undistorted:
        frame = cv2.undistort(frame, mtx, dist, None, newcameramtx)
        x,y,w,h = roi
        frame = frame[y:y+h, x:x+w]

	# Display the resulting frame
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    




#