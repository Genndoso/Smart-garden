import cv2
import sys
from PySide2 import QtCore, QtGui, QtWidgets
import qimage2ndarray


class VideoPlayer(QtWidgets.QWidget):
    pause = False
    video = False
    
    def __init__(self, width = 840, height = 480, fps=30):
        QtWidgets.QWidget.__init__(self)
        self.video_size = QtCore.QSize(width, height)
        self.camera_capture = cv2.VideoCapture(cv2.CAP_DSHOW)
        self.eyes_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
        #self.video_capture = cv2.VideoCapture()
        self.frames = []



        self.frame_timer = QtCore.QTimer()
        self.setup_camera(fps)
        self.fps = fps

        self.frame_label = QtWidgets.QLabel()
        self.quit_button = QtWidgets.QPushButton("Quit")
        self.play_pause_button = QtWidgets.QPushButton("Pause")
        #self.camera_video_button = QtWidgets.QPushButton("Switch to video")

        self.main_layout = QtWidgets.QGridLayout()
        self.setup_ui()
      #  self.image_read()

        QtCore.QObject.connect(self.play_pause_button, QtCore.SIGNAL('clicked()'), self.play_pause)
        #QtCore.QObject.connect(self.camera_video_button, QtCore.SIGNAL('clicked()'), self.camera_video_button)

    def setup_ui(self):
        self.frame_label.setFixedSize(self.video_size)
        self.quit_button.clicked.connect(self.close_win)

        self.main_layout.addWidget(self.frame_label, 0,0,1,2)

        self.main_layout.addWidget(self.play_pause_button, 1, 0, 1, 1)
        self.main_layout.addWidget(self.quit_button, 2,0,1,2)

        self.setLayout(self.main_layout)

    def play_pause(self):
        if not self.pause:
            self.frame_timer.stop()
            self.play_pause_button.setText("Play")
        else:
            self.frame_timer.start(int(1000//self.fps))
            self.play_pause_button.setText("Pause")
        self.pause = not self.pause

    '''def image_read(self,ret,frame):
        while True:
            ret, frame = self.camera_capture.read()
            eyes =  self.eyes_cascade.detectMultiScale(frame,scaleFactor=1.5, minNeighbors=5, minSize=(20,10))

            for (x,y,w,h) in self.eyes:
                cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2)
'''


    def setup_camera(self, fps):
        self.camera_capture.set(3, self.video_size.width())
        self.camera_capture.set(4, self.video_size.height())

        self.frame_timer.timeout.connect(self.display_video_stream)
        self.frame_timer.start(int(1000) // fps)

    def display_video_stream(self):
        ret, frame = self.camera_capture.read()

        if not ret:
            raise ValueError('No camera captured')

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame,1)


        eyes = self.eyes_cascade.detectMultiScale(frame, scaleFactor=1.5, minNeighbors=5, minSize=(20, 10))

        for (x, y, w, h) in eyes:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        image = qimage2ndarray.array2qimage(frame)
        self.frames.append(qimage2ndarray.rgb_view(image))
        self.most_recent_image = qimage2ndarray.rgb_view(image)
        self.frame_label.setPixmap(QtGui.QPixmap.fromImage(image))
 #''
    def close_win(self):
        cv2.destroyAllWindows()
        print(self.most_recent_image)
        #self.camera_capture.release()
        #self.video_capture.release()
        self.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec_())