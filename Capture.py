import cv2
import threading
from Calibrate import Calibrate

class Capture():
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.calibrate = Calibrate()

    def start(self):
        self.updateFrame()
        while(True):
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()

    def updateFrame(self):
        while(True):
            ret, self.img = self.cap.read()
            if ret: 
                self.img = self.calibrate.getChessboard(self.img)
                cv2.imshow('img', self.img)
                break
        threading.Timer(0.03333, self.updateFrame).start()

           


if __name__ == "__main__":
    capture = Capture()
    capture.start()