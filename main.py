import sys
import cv2
from PySide6.QtCore import QSize
from PySide6.QtGui import QAction, QActionGroup
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QMenu,
    QGroupBox,
    QCheckBox,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QToolButton,
    QSpacerItem,
    QSizePolicy
)

from CameraViewWidget import CameraViewWidget
from globals import cameraIndexes


class MainWiget(QWidget):
    def __init__(self):
        super().__init__()

        self.controlGroupBox = QGroupBox('', self)
        self.controlGroupBox.setMinimumSize(QSize(300, 0))
        self.controlGroupBox.layout = QVBoxLayout(self.controlGroupBox)
        self.controlGroupBox.layout.setSpacing(15)
        self.controlGroupBox.layout.setContentsMargins(5, 5, 5, 5)

        self.controlGroupBox.verticalSpacer = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.controlGroupBox.layout.addItem(
            self.controlGroupBox.verticalSpacer)

        self.cameraInputGroup = QGroupBox('Camera Input', self)
        self.cameraInputGroup.layout = QHBoxLayout(self.cameraInputGroup)
        self.cameraInputGroup.inputBtn = QToolButton(text='Select Camera')
        self.cameraInputGroup.layout.addWidget(self.cameraInputGroup.inputBtn)
        self.controlGroupBox.layout.addWidget(self.cameraInputGroup)

        self.menuGroup = QActionGroup(self)
        self.cameraMenu = QMenu()
        self.cameraActions = []
        for index, cameraIndex in enumerate(cameraIndexes) :
            cameraAction = QAction(f"Camera {cameraIndex}", self)
            cameraAction.setCheckable(True)
            cameraAction.index = cameraIndex
            self.cameraMenu.addAction(cameraAction)
            self.cameraActions.append(cameraAction)
            self.menuGroup.addAction(cameraAction)
            cameraAction.triggered.connect(self.cameraMenuTriggered)

        self.cameraInputGroup.inputBtn.setPopupMode(QToolButton.InstantPopup)
        self.cameraInputGroup.inputBtn.setMenu(self.cameraMenu)

        self.verticalLineGroup = QGroupBox('Vertical Line', self)
        self.verticalLineGroup.layout = QVBoxLayout(self.verticalLineGroup)
        self.verticalLineGroup.checkBox = QCheckBox(
            'Enable', self.verticalLineGroup)
        self.verticalLineGroup.layout.addWidget(
            self.verticalLineGroup.checkBox)

        self.verticalLineGroup.locationLayout = QHBoxLayout()
        self.verticalLineGroup.xLabel = QLabel('X Location')
        self.verticalLineGroup.xEdit = QLineEdit('100', self.verticalLineGroup)

        self.verticalLineGroup.locationLayout.addWidget(
            self.verticalLineGroup.xLabel)
        self.verticalLineGroup.locationLayout.addWidget(
            self.verticalLineGroup.xEdit)

        self.verticalLineGroup.layout.addLayout(
            self.verticalLineGroup.locationLayout)
        self.controlGroupBox.layout.addWidget(self.verticalLineGroup)

        self.horinzontalLineGroup = QGroupBox('Horizontal Line', self)
        self.horinzontalLineGroup.layout = QVBoxLayout(
            self.horinzontalLineGroup)
        self.horinzontalLineGroup.checkBox = QCheckBox(
            'Enable', self.horinzontalLineGroup)
        self.horinzontalLineGroup.layout.addWidget(
            self.horinzontalLineGroup.checkBox)

        self.horinzontalLineGroup.locationLayout = QHBoxLayout()
        self.horinzontalLineGroup.yLabel = QLabel('Y Location')
        self.horinzontalLineGroup.yEdit = QLineEdit('100', self.horinzontalLineGroup)

        self.horinzontalLineGroup.locationLayout.addWidget(
            self.horinzontalLineGroup.yLabel)
        self.horinzontalLineGroup.locationLayout.addWidget(
            self.horinzontalLineGroup.yEdit)

        self.horinzontalLineGroup.layout.addLayout(
            self.horinzontalLineGroup.locationLayout)
        self.controlGroupBox.layout.addWidget(self.horinzontalLineGroup)

        self.crossHairGroup = QGroupBox('Cross Hair', self)
        self.crossHairGroup.layout = QVBoxLayout(self.crossHairGroup)
        self.crossHairGroup.checkBox = QCheckBox('Enable', self.crossHairGroup)
        self.crossHairGroup.layout.addWidget(self.crossHairGroup.checkBox)

        self.crossHairGroup.xLayout = QHBoxLayout()

        self.crossHairGroup.xLabel = QLabel('X Location')
        self.crossHairGroup.xEdit = QLineEdit('300', self.crossHairGroup)
        self.crossHairGroup.xLayout.addWidget(self.crossHairGroup.xLabel)
        self.crossHairGroup.xLayout.addWidget(self.crossHairGroup.xEdit)

        self.crossHairGroup.yLayout = QHBoxLayout()

        self.crossHairGroup.yLabel = QLabel('Y Location')
        self.crossHairGroup.yEdit = QLineEdit('300', self.crossHairGroup)
        self.crossHairGroup.yLayout.addWidget(self.crossHairGroup.yLabel)
        self.crossHairGroup.yLayout.addWidget(self.crossHairGroup.yEdit)

        self.crossHairGroup.layout.addLayout(self.crossHairGroup.xLayout)
        self.crossHairGroup.layout.addLayout(self.crossHairGroup.yLayout)

        self.controlGroupBox.layout.addWidget(self.crossHairGroup)

        self.controlGroupBox.verticalSpacer_down = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.controlGroupBox.layout.addItem(
            self.controlGroupBox.verticalSpacer_down)

        self.layout = QHBoxLayout(self)

        self.cameraWidget = CameraViewWidget(self)
        # self.cameraWidget.openCamera(cameraIndexes[0])

        self.layout.addWidget(self.cameraWidget)
        self.layout.addWidget(self.controlGroupBox)
        self.layout.setStretch(0, 1)

        self.cameraActions[0].trigger()

        self.verticalLineGroup.checkBox.stateChanged.connect(self.resetVerticalLineValue)
        self.verticalLineGroup.xEdit.textChanged.connect(self.resetVerticalLineValue)

        self.horinzontalLineGroup.checkBox.stateChanged.connect(self.resetHorizontalValue)
        self.horinzontalLineGroup.yEdit.textChanged.connect(self.resetHorizontalValue)

        self.crossHairGroup.checkBox.stateChanged.connect(self.resetCrossHairValue)
        self.crossHairGroup.xEdit.textChanged.connect(self.resetCrossHairValue)
        self.crossHairGroup.yEdit.textChanged.connect(self.resetCrossHairValue)

        self.resetVerticalLineValue()
        self.resetHorizontalValue()
        self.resetCrossHairValue()

    def cameraMenuTriggered(self):
        self.cameraWidget.closeCamera()
        for index, cameraAction in enumerate(self.cameraActions) :
            if (cameraAction.isChecked()) :
                self.cameraWidget.openCamera(cameraAction.index)

    def resetVerticalLineValue(self) :
        value = -1
        if self.verticalLineGroup.checkBox.isChecked() :
            try :
                value = int(self.verticalLineGroup.xEdit.text())
            except ValueError:
                value = -1
            self.verticalLineGroup.xEdit.setEnabled(True)
        else:
            self.verticalLineGroup.xEdit.setEnabled(False)
        self.cameraWidget.verticalLine = value

    def resetHorizontalValue(self) :
        value = -1
        if self.horinzontalLineGroup.checkBox.isChecked() :
            try :
                value = int(self.horinzontalLineGroup.yEdit.text())
            except ValueError:
                value = -1
            self.horinzontalLineGroup.yEdit.setEnabled(True)
        else:
            self.horinzontalLineGroup.yEdit.setEnabled(False)
        self.cameraWidget.horizontalLine = value

    def resetCrossHairValue(self) :
        xValue = -1
        yValue = -1
        if self.crossHairGroup.checkBox.isChecked() :
            try :
                xValue = int(self.crossHairGroup.xEdit.text())
            except ValueError:
                xValue = -1
            try :
                yValue = int(self.crossHairGroup.yEdit.text())
            except ValueError:
                yValue = -1
            self.crossHairGroup.xEdit.setEnabled(True)
            self.crossHairGroup.yEdit.setEnabled(True)
        else:
            self.crossHairGroup.xEdit.setEnabled(False)
            self.crossHairGroup.yEdit.setEnabled(False)
        self.cameraWidget.crossHair["x"] = xValue
        self.cameraWidget.crossHair["y"] = yValue

def main():
    global cameraIndexes
    for camera_index in range(3):
        cap = cv2.VideoCapture(camera_index)
        if cap.isOpened():
            cameraIndexes.append(camera_index)
            cap.release()
    if len(cameraIndexes) == 0:
        cameraIndexes = [0]

    app = QApplication(sys.argv)
    main_widget = MainWiget()
    main_widget.resize(700, 500)
    main_widget.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
