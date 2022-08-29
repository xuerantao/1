
import sys

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QThread, QObject, pyqtSignal

from animation_window import AnimationWindow


def main():
    width = 160
    height = 120
    fps = 20

    app = QApplication(sys.argv)
    win = AnimationWindow("Test", width, height, fps)
    for color in [(255, 0, 0), (0, 255, 0), (0, 0, 255)]:
        win.add_frame([color] * (width * height))
    win.start()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()