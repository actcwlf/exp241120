import sys
import cv2
import argparse
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap

class VideoPlayer(QMainWindow):
    def __init__(self, video_path1, video_path2):
        super().__init__()

        self.setWindowTitle("Simple Video Player")

        self.setGeometry(100, 100, 960, 540)

        # Main widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Layout
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Video display label
        self.video_label = QLabel(self)
        self.video_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.video_label)

        # Control buttons
        # self.play_button = QPushButton("Play", self)
        # self.play_button.clicked.connect(self.play_video)
        # self.layout.addWidget(self.play_button)
        #
        # self.pause_button = QPushButton("Pause", self)
        # self.pause_button.clicked.connect(self.pause_video)
        # self.layout.addWidget(self.pause_button)

        # Timer for video playback
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_frame_slot)

        self.video_path1 = video_path1
        self.video_path2 = video_path2

        # Video capture
        self.cap1 = cv2.VideoCapture(video_path1)
        self.cap2 = cv2.VideoCapture(video_path2)
        self.playing = False
        self.video_ended = False  # Flag to track if the video ended

        self.play_video()

    # def play_video(self):
    #     if self.cap1 is not None and not self.playing:
    #         self.playing = True
    #         self.timer.start(30)  # Adjust the timer interval as needed

    def play_video(self):
        if not self.playing:
            if self.video_ended:
                # Restart the video from the beginning
                self.cap1.set(cv2.CAP_PROP_POS_FRAMES, 0)
                self.cap2.set(cv2.CAP_PROP_POS_FRAMES, 0)
                self.video_ended = False

            self.playing = True
            self.timer.start(30)  # Adjust the timer interval as needed

    def pause_video(self):
        if self.playing:
            self.playing = False
            self.timer.stop()

    def next_frame_slot(self):
        if self.cap1.isOpened() and self.cap2.isOpened():
            ret1, frame1 = self.cap1.read()
            ret2, frame2 = self.cap2.read()
            if ret1 and ret2:
                frame = frame1
                frame[:, 960:, :] = frame2[:, 960:, :]
                frame[:, 959:961, :] = 0

                font = cv2.FONT_HERSHEY_SIMPLEX
                position = (10, 30)  # Position for the text
                font_scale = 1
                color = (255, 255, 255)  # White text
                thickness = 1
                cv2.putText(frame, self.video_path1, position, font, font_scale, color, thickness, cv2.LINE_AA)

                position = (970, 30)  # Position for the text
                cv2.putText(frame, self.video_path2, position, font, font_scale, color, thickness, cv2.LINE_AA)

                window_size = self.video_label.size()
                resized_frame = cv2.resize(frame, (window_size.width(), window_size.height()),
                                           interpolation=cv2.INTER_AREA)

                # Convert the frame to a QImage
                rgb_image = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)

                # Set the QImage to the QLabel
                self.video_label.setPixmap(QPixmap.fromImage(qt_image))
            else:
                # If no frame is returned, stop the video
                self.timer.stop()
                # self.cap1.release()
                # self.cap2.release()
                self.playing = False
                self.video_ended = True

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            if self.playing:
                self.pause_video()
            else:
                self.play_video()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Simple Video Player")
    parser.add_argument('--video_path1', type=str, help='Path to the video file on the left',  default='./videos/nerv/ReadySetGo.mkv')
    parser.add_argument('--video_path2', type=str, help='Path to the video file on the right', default='./videos/gsvc/ReadySetGo.mkv')

    args = parser.parse_args()

    app = QApplication(sys.argv)
    player = VideoPlayer(args.video_path1, args.video_path2)
    player.show()
    sys.exit(app.exec_())
