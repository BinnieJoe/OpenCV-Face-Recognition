import cv2 as cv
import numpy as np
from PyQt5.QtWidgets import *
import sys

class VideoSpecialEffect(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VideoSpecialEffect")
        self.setGeometry(50, 50, 700, 150)

        videoButton=QPushButton("StartVideo", self)
        self.pickBox=QComboBox(self)
        self.pickBox.addItems(['Embossing', 'Cartoon', 'Scatch(contrast)', 'Scatch(color)', 'Oil point'])
        quitButton=QPushButton('Out', self)
        
        videoButton.setGeometry(10, 10, 180, 40)  
        self.pickBox.setGeometry(200, 10, 180, 40)  
        quitButton.setGeometry(390, 10, 180, 40)  

        videoButton.clicked.connect(self.VideoSpecialEffectFunction)
        quitButton.clicked.connect(self.quitFunction)


    def VideoSpecialEffectFunction(self):
        self.cap = cv.VideoCapture(0, cv.CAP_DSHOW)
        if not self.cap.isOpened(): sys.exit("CameraConnectFail")

        while True:
            ret, frame = self.cap.read()
            if not ret: break

            effect = self.pickBox.currentIndex()
            if effect == 0:
                femboss = np.array([[-1.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
                gray=cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
                gray16 = np.int16(gray)
                special_img = np.uint8(np.clip(cv.filter2D(gray16, -1, femboss) + 128, 0, 255))
                name = 'Embossing'
            elif effect == 1:
                special_img = cv.stylization(frame, sigma_s=60, sigma_r=0.45)
                name = 'Cartoon'
            elif effect == 2:
                special_img,_ = cv.pencilSketch(frame, sigma_s=60, sigma_r=0.07, shade_factor=0.02)
                name = 'Scatch(contrast)'
            elif effect == 3:
                _,special_img = cv.pencilSketch(frame, sigma_s=60, sigma_r=0.07, shade_factor=0.02)
                name = 'Scatch(color)'
            elif effect == 4:
                special_img = cv.xphoto.oilPainting(frame, 10, 1, cv.COLOR_BGR2Lab)
                name = 'Oil point'
            
            cv.imshow(name, special_img)
            cv.waitKey(1)

    def quitFunction(self):
        self.cap.release()
        cv.destroyAllWindows()
        self.close()

app=QApplication(sys.argv)
win=VideoSpecialEffect()
win.show()
app.exec_()

