import sys

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QThread, QObject, pyqtSignal

from animation_window import AnimationWindow
from mandelbrot_set import MandelbrotSet


def main():
    width = 160
    height = 120
    fps = 20

    # Some interesting targets
    mandelbrot_antennas = (-0.1638, 1.0353)
    seahorse_valley = (-0.746, -0.1)
    elephant_valley = (0.2855, 0.012)

    # Animation parameters
    target = mandelbrot_antennas
    steps = 30

    def easing(begin, end, length):
        """
        :param begin: first value
        :param end: last value
        :param length: length of expected values
        :return: eased out values so that the change is first big and small at the end
        """
        change = end - begin
        last = length - 1
        return [begin - ((i / last - 1.0) ** 4 - 1.0) * change for i in range(length)]

    class CalculatorThread(QThread, QObject):

        new_image = pyqtSignal(list)
        finished = pyqtSignal()

        def __init__(self, mb_set, xyw_list):
            super().__init__()
            self.mb_set = mb_set
            self.xyw_list = xyw_list

        def run(self):
            for x, y, w in self.xyw_list:
                self.new_image.emit(self.mb_set.calculate((x, y), w))
            self.finished.emit()

    app = QApplication(sys.argv)
    win = AnimationWindow("Mini Mandelbrot", width, height, fps)
    mandelbrot = MandelbrotSet(width, height, 1000)
    calculation = CalculatorThread(mandelbrot, zip(
        easing(-0.5, target[0], steps),
        easing(0.0, target[1], steps),
        easing(3, 0.0005, steps)
    ))
    calculation.new_image.connect(win.add_frame)
    calculation.finished.connect(win.start)
    calculation.start()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
