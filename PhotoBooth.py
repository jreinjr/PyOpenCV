
import sys
import cv2
from datetime import datetime as dt
from Calibrate import Calibrate
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi

class PhotoBooth(QDialog):
    def __init__(self):
        super(PhotoBooth,self).__init__()
        loadUi('PhotoBooth.ui', self)
        self.calibrate = Calibrate()
        self.image = None
        self.fpath_calib = None
        self.fpath_corners = None

        self.cap = cv2.VideoCapture(1)
        self.showStream = False
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

        self.showCorners = False
        self.showCalib = False

        self._toggle_stream.clicked.connect(self.toggle_stream_clicked)
        self._toggle_corners.clicked.connect(self.toggle_corners_clicked)
        self._toggle_calib.clicked.connect(self.toggle_calib_clicked)
        self._save_corners.clicked.connect(self.save_corners_clicked)
        self._filepath_corners.clicked.connect(self.filepath_corners_clicked)
        self._save_calib.clicked.connect(self.save_calib_clicked)
        self._filepath_calib.clicked.connect(self.filepath_calib_clicked)


    # Set filepath for corners images
    def filepath_corners_clicked(self):
        self.fpath_corners = QFileDialog.getExistingDirectory(self, "Open Directory", "../", QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks )
        self._filepath_corners.setText(self.fpath_corners)

    # Save corners frame
    def save_corners_clicked(self):
        if self.showStream and self.fpath_corners:
           fmt = "%y%m%d_%H%M%S_%f"
           fname_corners = self.fpath_corners + "/" + dt.utcnow().strftime(fmt) + ".jpg"
           print("Saving " + fname_corners)
           cv2.imwrite(fname_corners, self.img)

    # Set filepath for calibration file
    def filepath_calib_clicked(self):
        self.fpath_calib = QFileDialog.getExistingDirectory(self, "Open Directory", "../", QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks )
        self._filepath_calib.setText(self.fpath_calib)

    # Save calibration file
    def save_calib_clicked(self):
        if self.showStream and self.fpath_calib:
            print("save calib")
        
    # Open webcam stream
    def toggle_stream_clicked(self):
        if(self.showStream):
            self.timer.stop()
            self.showStream = False
        else:
            self.timer.start(5)
            self.showStream = True

    # Toggle corners overlay
    def toggle_corners_clicked(self):
        self.showCorners = not self.showCorners

    # Toggle calibrated image
    def toggle_calib_clicked(self):
        self.showCalib = not self.showCalib

    def update_frame(self):
        ret, self.img = self.cap.read()
        if ret:
            self.displayImage(self._frame, self.img)
       
    # Display image img in label lbl
    def displayImage(self, lbl, img):
        preview = img
        if self.showCorners:
            preview = self.calibrate.getChessboard(preview)
        preview = self.convertImage(preview)
        lbl.setPixmap(QPixmap.fromImage(preview))
        lbl.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)

    # Convert image from RGB to BGR for OpenCV
    def convertImage(self, img):
        qformat=QImage.Format_Indexed8
        if len(img.shape)==3:
            if(img.shape[2]) == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        img = QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)
        img = img.rgbSwapped()
        return img

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PhotoBooth()
    window.setWindowTitle('PhotoBooth')
    window.show()
    sys.exit(app.exec_())