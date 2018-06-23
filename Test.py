import cv2

class Test():
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.showFrame()

    def showFrame(self):
        print("hey")
        while(True):
            ret, self.img = self.cap.read()
            cv2.imshow('img', self.img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = Test()