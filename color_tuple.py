

def hsl_to_rgb(hsl):
    """
    Color space conversion.
    http://www.niwa.nu/2013/05/math-behind-colorspace-conversions-rgb-hsl/
    :param hsl tuple (hue, saturation, lightness) each a number in range 0.0-1.0
    :return rgb tuple (red, green, blue) each a number in range 0-255
    """
    def int255(f): return int(max(0.0, min(1.0, f)) * 255)
    def rgb255(rgb): return [int255(rgb[0]), int255(rgb[1]), int255(rgb[2])]

    if hsl[1] == 0.0:
        return rgb255([hsl[2], hsl[2], hsl[2]])

    t1 = (hsl[2] * (1.0 + hsl[1])) if (hsl[2] < 0.5) else (hsl[2] + hsl[1] - hsl[2] * hsl[1])
    t2 = 2.0 * hsl[2] - t1
    t12 = (t1 - t2) * 6.0
    tr = (hsl[0] + 0.333) % 1.0
    tg = hsl[0]
    tb = (hsl[0] - 0.333 + 1.0) if (hsl[0] < 0.333) else (hsl[0] - 0.333)

    def ch_test(tc): return (t2 + t12 * tc if 6.0 * tc < 1.0
                             else (t1 if 2.0 * tc < 1.0
                                   else (t2 + t12 * (0.666 - tc)
                                         if 3.0 * tc < 2.0 else t2)))

    return rgb255([ch_test(tr), ch_test(tg), ch_test(tb)])


def palette(size, points):
    """
    Creates an indexed color palette by sliding colors between the fixed color points.
    :param size the size or length of a palette
    :param points the fixed colors as tuples of (index, hue, saturation, lightness)
    :return sequence of colors as tuples (red, green, blue)
    """
    out = []
    if len(points) > 1:
        def index(point): return point[0]
        def hsl(point): return point[1:]

        # Fill first color until first point.
        for _ in range(index(points[0])):
            out.append(hsl_to_rgb(hsl(points[0])))

        for i in range(len(points) - 1):
            p, p1 = points[i], points[i + 1]

            if i == 0 or index(p) > index(points[i - 1]):
                out.append(hsl_to_rgb((hsl(p))))

            # Interpolate color values until next color point.
            d = index(p1) - index(p)
            h0, s0, l0 = hsl(p)
            dh, ds, dl = [(v1 - v0) / d for v1, v0 in zip(hsl(p1), hsl(p))]
            for j in range(1, d):
                out.append(hsl_to_rgb((h0 + j * dh, s0 + j * ds, l0 + j * dl)))

        # Fill last color to end.
        for i in range(index(points[-1]), size):
            out.append(hsl_to_rgb(hsl(points[-1])))

    return out
