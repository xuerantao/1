import color_tuple


class MandelbrotSet(object):
    """
    Mandelbrot set are the complex numbers c that do not escape
    the circle of radius 2 in a squaring loop z = 0; z = z^2 + c.
    http://en.wikipedia.org/wiki/Mandelbrot_set
    """

    def __init__(self, pixel_width, pixel_height, max_iteration):
        """
        :param pixel_width: a width of pixel area to model
        :param pixel_height: a height of pixel area to model
        :param max_iteration: a maximum number of iterations for a pixel
        """
        self.width = pixel_width
        self.height = pixel_height
        self.max_iteration = max_iteration
        self.palette = color_tuple.palette(100, [
            (0, 300.0 / 360, 1.0, 0.0),
            (15, 250.0 / 360, 1.0, 0.5),
            (99, 300.0 / 360, 1.0, 1.0)
        ])
        self.palette_length = len(self.palette) - 1

    def calculate(self, complex_center, complex_width):
        """
        Calculates color for each pixel in a given view.
        :param complex_center: a center point of a view in complex plane (real, imaginary)
        :param complex_width: a width of a view in complex plane
        :return: running array of modeled pixels (red, green, blue)
        """
        pixels = []
        d = complex_width / self.width
        y = complex_center[1] - (self.height / 2) * d
        for yi in range(0, self.height):
            x = complex_center[0] - (self.width / 2) * d
            for xi in range(0, self.width):
                pixels.append(self.escape_iteration(x, y))
                x += d
            y += d
        return [self.palette[int(i / self.max_iteration * self.palette_length)] for i in pixels]

    def escape_iteration(self, x, y):
        """
        Given complex numbers c = x + yi and z = 0,
        tests how many iterations z = z^2 + c stays inside a circle of radius 2.
        Optimizations are made to remove time consuming multiplications.
        """
        def square(v): return v * v
        iteration = 0
        r, i = 0.0, 0.0
        r2, i2 = 0.0, 0.0
        while iteration < self.max_iteration and r2 + i2 < 4.0:
            i = square(r + i) - r2 - i2 + y
            r = r2 - i2 + x
            r2 = square(r)
            i2 = square(i)
            iteration += 1
        return iteration
