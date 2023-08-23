import cv2
from PySide6.QtCore import QTimer
from PySide6.QtGui import QImage, QPixmap, QPainter, QPen, QColor
from PySide6.QtWidgets import (
    QWidget,
    QLabel
)


class CameraViewWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.camera_index = -1
        self.video_capture = None
        self.video_timer = QTimer(self)
        self.video_timer.timeout.connect(self.update_frame)
        self.video_timer.start(30)
        self.cameraImage = QPixmap()

        self.image_label = QLabel(self)
        self.image_label.setScaledContents(True)
        self.setStyleSheet(
            "QLabel{ border: 6px solid rgb(191, 144, 0); border-radius: 5px; }")

        self.verticalLine = 100
        self.horizontalLine = 100
        self.crossHair = {"x": 300, "y": 300}

    def __del__(self):
        self.video_timer.stop()
        if self.video_capture != None:
            self.video_capture.release()

    def openCamera(self, index=-1):
        if index != -1:
            self.camera_index = index
        self.video_capture = cv2.VideoCapture(self.camera_index)
        # self.video_capture_available = self.video_capture.isOpened()

    def closeCamera(self):
        if (self.video_capture != None):
            self.video_capture.release()
            self.video_capture = None
            self.camera_index = -1

    def update_frame(self):
        if self.video_capture != None:
            ret, frame = self.video_capture.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                height, width, channel = frame_rgb.shape
                bytes_per_line = 3 * width
                qt_image = QImage(frame_rgb.data, width, height,
                                  bytes_per_line, QImage.Format_RGB888)
                painter = QPainter(qt_image)
                if self.verticalLine >= 0 :
                    pen = QPen()
                    pen.setColor(QColor(68, 114, 195))
                    pen.setWidth(4)
                    painter.setPen(pen)
                    painter.drawLine(self.verticalLine, 0, self.verticalLine, qt_image.height())
                if self.horizontalLine >= 0 :
                    pen = QPen()
                    pen.setColor(QColor(112, 172, 71))
                    pen.setWidth(4)
                    painter.setPen(pen)
                    painter.drawLine(0, self.horizontalLine, qt_image.width(), self.horizontalLine)
                if self.crossHair["x"] >= 0 and self.crossHair["y"] >= 0 :
                    pen = QPen()
                    pen.setColor(QColor(236, 125, 49))
                    pen.setWidth(4)
                    painter.setPen(pen)
                    painter.drawLine(self.crossHair["x"] - 30, self.crossHair["y"], self.crossHair["x"] + 30, self.crossHair["y"])
                    painter.drawLine(self.crossHair["x"], self.crossHair["y"] - 30, self.crossHair["x"], self.crossHair["y"] + 30)
                # painter.drawRect(0, 0, 200, 200)
                painter.end()
                self.image_label.setPixmap(QPixmap.fromImage(qt_image))
                return
        self.image_label.setText(f'Camera{self.camera_index + 1}')

    def resizeEvent(self, event):
        x_ratio = 5
        y_ratio = 4

        new_width = event.size().width()
        new_height = event.size().height()

        label_width = 0
        label_height = 0

        if new_width * y_ratio > new_height * x_ratio:
            label_height = new_height
            label_width = new_height * x_ratio / y_ratio
        else:
            label_width = new_width
            label_height = new_width * y_ratio / x_ratio

        self.image_label.setGeometry(
            (new_width - label_width) / 2, (new_height - label_height) / 2, label_width, label_height)

    def closeEvent(self, event):
        self.video_capture.release()

