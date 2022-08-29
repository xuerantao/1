import time

from PyQt6.QtWidgets import QMainWindow, QLabel
from PyQt6.QtGui import QImage, QPixmap, QColor
from PyQt6.QtCore import QThread, QSize


class AnimationWindow(QMainWindow):

    def __init__(self, title, width, height, frame_rate):
        super().__init__()
        self.frames = []
        self.index = 0
        self.thread = AnimationWindow.Thread(self, frame_rate)

        self.setWindowTitle(title)
        self.setFixedSize(QSize(width, height))
        self.label = QLabel(self)
        self.label.setMinimumSize(width, height)
        self.setCentralWidget(self.label)
        self.show()

    def add_frame(self, pixels):
        """
        Adds frame to animation.
        :param pixels: a sequence of color tuples having length width * height
        """
        image = QImage(self.size(), QImage.Format.Format_RGB32)
        width = image.width()
        assert len(pixels) == width * image.height()
        for i, rgb in enumerate(pixels):
            image.setPixelColor(i % width, i // width, QColor(rgb[0], rgb[1], rgb[2]))
        self.frames.append(QPixmap.fromImage(image))
        self.show_frame(len(self.frames) - 1)

    def show_frame(self, index):
        self.label.setPixmap(self.frames[index])
        self.label.update()

    def next_frame(self):
        self.index += 1
        self.index %= len(self.frames)
        self.show_frame(self.index)

    def start(self):
        """
        Starts a Qt thread that will loop added frames until interrupted.
        """
        if len(self.frames) > 0:
            self.thread.start()

    class Thread(QThread):

        def __init__(self, window, frame_rate):
            super().__init__()
            self.window = window
            self.delay = 1 / frame_rate

        def run(self):
            while self.isRunning():
                time.sleep(self.delay)
                self.window.next_frame()
