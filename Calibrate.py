import cv2
import threading
import numpy as np
import matplotlib

class Calibrate():
    def __init__(self):
        self.img = None;
        # termination criteria
        self.criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        # prepare object points
        self.objp = np.zeros((4*6, 3), np.float32)
        self.objp[:, :2] = np.mgrid[0:4, 0:6].T.reshape(-1, 2)
        # Arrays to store object points and image points from all the images
        self.objpoints = [] # 3d point in real world space
        self.imgpoints = [] # 2d point in image plane

    def getChessboard(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, (4,6), None)
        if ret == True:
            self.objpoints.append(self.objp)
            corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1, -1), self.criteria)
            self.imgpoints.append(corners)
            cv2.drawChessboardCorners(img, (4,6), corners2, ret)
        return img
    

def getFrame(cap):
    threading.Timer(100, self.getFrame, cap).start()
    ret, img = cap.read()
    cv2.imshow('img', img)
    return img

if __name__ == "__main__":
    app = Calibrate()
    cap = cv2.VideoCapture(0)
    while (True):
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()