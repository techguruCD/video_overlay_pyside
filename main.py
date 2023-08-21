import sys
import cv2
from PySide6.QtCore import QTimer, Qt, QSize
from PySide6.QtGui import QImage, QPixmap, QFont, QIcon
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSpacerItem,
    QSizePolicy
)

# Control Variables
camera_count = 2
camera_views = [0] * camera_count

# Editable Variables
mode = 'camera'
measure_idx = 0



def show_one_camera(param):
    global measure_idx
    for idx in range(camera_count):
        camera_views[idx].hide()
    for idx in range(camera_count):
        if idx == measure_idx or param < 0:
            camera_views[idx].show()

# Camera View
class CameraViewWidget(QWidget):
    def __init__(self, camera_index):
        super().__init__()

        self.camera_index = camera_index

        self.video_capture = cv2.VideoCapture(camera_index)
        self.video_capture_available = self.video_capture.isOpened()
        self.video_timer = QTimer(self)
        self.video_timer.timeout.connect(self.update_frame)
        self.video_timer.start(30)

        self.image_label = QLabel(self)
        self.image_label.setScaledContents(True)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        self.setLayout(layout)

    def update_frame(self):
        ret, frame = self.video_capture.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame_rgb.shape
            bytes_per_line = 3 * width
            qt_image = QImage(frame_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
            self.image_label.setPixmap(QPixmap.fromImage(qt_image))
        else :
            self.image_label.setText(f'Camera{self.camera_index + 1}')

    def closeEvent(self, event):
        self.video_capture.release()

class CameraGroupWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.camera_layout = QHBoxLayout()        
        for idx in range(camera_count):
            camera_views[idx] = CameraViewWidget(idx)
            self.camera_layout.addWidget(camera_views[idx])
        self.setLayout(self.camera_layout)
        icon = QIcon("next.png")
        self.next_btn = QPushButton('', self)
        self.next_btn.setFixedSize(80, 80)
        self.next_btn.setIcon(icon)
        icon_size = QSize(80, 80)
        self.next_btn.setFlat(True)
        self.next_btn.setStyleSheet("QPushButton:pressed { background-color: none; }")
        self.next_btn.setIconSize(icon_size)
        self.next_btn.clicked.connect(self.on_nextbtn_click)

    def resizeEvent(self, event):
        new_width = event.size().width()
        new_height = event.size().height()
        self.next_btn.move(new_width-100, 20)
     
    def on_nextbtn_click(self):
        global measure_idx
        measure_idx = 0 if measure_idx == camera_count - 1 else measure_idx + 1
        show_one_camera(measure_idx)

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.display_measurement()

    def init_ui(self):
        self.setWindowTitle('Camera Viewer')
        self.setGeometry(100, 100, 400, 300)

        self.view_layout = QVBoxLayout()

        # Title Layout
        self.title_layout = QHBoxLayout()
        self.title_label = QLabel('Camera View')
        font_title = QFont('Arial', 24, QFont.Bold)
        self.title_label.setFont(font_title)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_layout.addWidget(self.title_label)

        self.camera_widget = CameraGroupWidget()

        # Form Layout
        self.form_layout = QHBoxLayout()
        form_label_layout = QVBoxLayout()
        form_input_layout = QVBoxLayout()

        font_input_labels = QFont('Arial', 16)

        self.first_widget = QWidget()

        labels = ['Square Size:', 'Width:', 'Height:']
        inputs = [QLineEdit('') for _ in range(3)]

        for idx, label_text in enumerate(labels):
            label = QLabel(label_text)
            label.setFont(font_input_labels)
            form_label_layout.addWidget(label)

            input_field = inputs[idx]
            input_field.setFont(font_input_labels)
            form_input_layout.addWidget(input_field)

        self.form_layout.addLayout(form_label_layout)
        self.form_layout.addLayout(form_input_layout)
        self.form_layout.setContentsMargins(20, 20, 50, 20)
        self.form_layout.insertSpacing(1, 30)

        # Info Layout
        self.info_layout = QHBoxLayout()
        info_label_layout = QVBoxLayout()
        info_value_layout = QVBoxLayout()
        info_top_spacer = QSpacerItem(1, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        info_middle_spacer = QSpacerItem(1, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        info_bottom_spacer = QSpacerItem(1, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        font_input_labels = QFont('Arial', 16)

        labels = ['Width:', 'Height:', 'Length:']
        self.value_labels = [QLabel('asdf') for _ in range(3)]

        for idx, label_text in enumerate(labels):
            label = QLabel(label_text)
            label.setFont(font_input_labels)
            info_label_layout.addWidget(label)

            value_label = self.value_labels[idx]
            value_label.setFont(font_input_labels)
            info_value_layout.addWidget(value_label)

        self.info_layout.addLayout(info_label_layout)
        self.info_layout.addLayout(info_value_layout)

        # Save Button Widget
        save_layout = QHBoxLayout()
        save_button = QPushButton('Save')
        save_button.setStyleSheet('''
            QPushButton {
                background-color: rgb(213, 232, 212);
                border: 2px solid rgb(130, 179, 102);
                font-size: 20px;
                padding: 20px 100px;
                border-radius: 10px;
            }
        ''')
        font_save_button = QFont('Arial', 16, QFont.Bold)
        save_button.setFont(font_save_button)
        save_button.clicked.connect(self.on_savebtn_click)
        save_left_spacer = QSpacerItem(40, 1, QSizePolicy.Expanding, QSizePolicy.Minimum)
        save_right_spacer = QSpacerItem(40, 1, QSizePolicy.Expanding, QSizePolicy.Minimum)
        save_layout.addItem(save_left_spacer)
        save_layout.addWidget(save_button)
        save_layout.addItem(save_right_spacer)

        # Reset Button Widget
        reset_button = QPushButton('Reset')
        reset_button.setStyleSheet('''
            QPushButton {
                background-color: rgb(213, 232, 212);
                border: 2px solid rgb(130, 179, 102);
                font-size: 20px;
                padding: 20px 100px;
                border-radius: 10px;
            }
        ''')
        font_reset_button = QFont('Arial', 16, QFont.Bold)
        reset_button.setFont(font_reset_button)
        reset_button.clicked.connect(self.on_resetbtn_click)

        self.view_layout.addLayout(self.title_layout)
        
        self.setLayout(self.view_layout)

        self.first_layout = QVBoxLayout()
        self.first_sub_layout = QHBoxLayout()
        self.first_sub_layout.addLayout(self.form_layout)
        self.first_sub_layout.addLayout(save_layout)
        self.first_sub_layout.setStretch(0, 1)
        self.first_sub_layout.setStretch(1, 1)
        self.first_layout.addWidget(self.camera_widget)
        self.first_layout.addLayout(self.first_sub_layout)
        self.first_widget.setLayout(self.first_layout)
        self.view_layout.addWidget(self.first_widget)

        self.second_layout = QHBoxLayout()
        second_sub_layout = QVBoxLayout()
        second_sub_layout.addItem(info_top_spacer)
        second_sub_layout.addLayout(self.info_layout)
        second_sub_layout.addItem(info_middle_spacer)
        second_sub_layout.addWidget(reset_button)
        second_sub_layout.addItem(info_bottom_spacer)
        second_sub_layout.setContentsMargins(40, 0, 40, 0)

        self.second_layout.addLayout(second_sub_layout)
        self.second_widget = QWidget()
        self.second_widget.setLayout(self.second_layout)
        self.view_layout.addWidget(self.second_widget)

        self.view_layout.setStretch(0, 0)
        self.view_layout.setStretch(1, 1)
        self.view_layout.setStretch(2, 1)

        self.second_widget.hide()
        self.camera_widget.next_btn.hide()

    def clear_view_layout(self):
        print('clear')

    def on_savebtn_click(self):
        global measure_idx
        measure_idx = 0
        show_one_camera(measure_idx)
        self.first_layout.removeWidget(self.camera_widget)
        self.second_layout.insertWidget(0, self.camera_widget)
        self.first_widget.hide()
        self.second_widget.show()
        self.title_label.setText('Measurement')

        self.second_layout.setStretch(0, 1)
        self.second_layout.setStretch(1, 0)
        self.camera_widget.next_btn.show()

    def on_resetbtn_click(self):
        self.second_layout.removeWidget(self.camera_widget)
        self.first_layout.insertWidget(0, self.camera_widget)
        self.second_widget.hide()
        self.first_widget.show()
        show_one_camera(-1)
        self.title_label.setText('View camera')
        self.camera_widget.next_btn.hide()
    def display_measurement(self, width=35, height=25, length=135):
        self.value_labels[0].setText(str(width))
        self.value_labels[1].setText(str(height))
        self.value_labels[2].setText(str(length))

def main():
    app = QApplication(sys.argv)
    main_widget = MainWidget()
    main_widget.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()