from PIL import Image, ImageDraw
import random
from math import *
import timeit

start = timeit.default_timer()


def mandelbrot(c, max_iterations):
    z = 0
    n = 0
    H = 0
    while abs(z) <= 2 and n < max_iterations:
        z = z**2 + c
        n += 1
        # interpolation between colours for a smooth gradient instead of an instant change in colour (the colour has no meaning in the fractal mathemtically, so modifying it will not change any accuracy in the rendering of the fractal)
        H = int(n - log10(abs(z)) / log10(max_iterations))
    return n, H
    # z_n+1 = z_n^2 + c


def clamp(val, min, max):
    return min(max(val, min), max)

# 0.01 is approx 1 pixel offsetting (precision of approximation depletes as offsets increase, beware)
# mandelbrot coordinates apply to these coordinates as well, keeping in mind that the imaginary offset is the inverse (negative) of the real offset (meaning if you would like to position the point of focus at the Julia Set (0.79, 0.15i), you would have to input (0.79, -0.15i) as the real and imaginary offset) without the i
real_offset = -0.79
imaginary_offset = -0.15

width = 512
height = 512

magnification = 100  # zooms into the point at the center of the screen. to figure out where that is, enable the crosshair code commented after the generating for loops, or wait for the gridbox update!

# "colorful" colour system being used is HSV due to the easy functionality to scroll through the entire colour spectrum, allowing for easily customisable palettes. RGB is useful for a static colour palette.
target = Image.new('HSV', (width, height), (220, 1, 1))
draw = ImageDraw.Draw(target)

# the higher this number, the more accurate the fractal will be, but the longer it will take to render. be careful modifying this number, as it is the number of iterations the algorithm will run before deciding that the point is not in the Mandelbrot Set, therefore requiring more iterations and processing speed, hence potentially causing crashes or slowdowns. do not try to modify this number while you are using your computer unless it is exceptionally beefy. I was able to set this number to 10000 without crashes or much of an impact on other processes (video-streaming and gaming not tested) and rendered a fractal in 174.953s (Intel i7 8550u, 16GB RAM, integrated graphics)
max_iterations = 10000

# at the same max_iteration value, running at 512x512 with a magnification of 100 located at the julia set rendered in 817.038s... optimisations required.

# interpolation uses up additional processing power, keep that in mind. results with the current colouring algorithm aren't too aesthetically pleasing either, when at high resolutions, magnifications and iterations

for x in range(0, width):
    for y in range(0, height):
        # for the julia set, complex[0] (the real part of the complex number, preceding the comma) should be equal to -0.79 with the complex part equaling 0.15i
        c = complex((real_offset * magnification) + (x / width) * 2 - 1,
                    (imaginary_offset * magnification) + (y / height) * 2 - 1)
        m = mandelbrot(c / magnification, max_iterations)[0]
        # H = int(abs(175 - (2*m)))
        H = int(mandelbrot(c / magnification, max_iterations)[1])
        S = 255
        V = 255 if m < max_iterations else 10

        # RGB FILLING CODE OBSOLETE. CHECK END OF FILE FOR OBSOLETE CODE

        # color = 255 - int(m * 255 / max_iterations) # WORKS ON RGB COLOUR SYSTEM ONLY
        draw.point([x, y], (H, S, V))

draw.point([width / 2, height / 2], (255, 255, 255))
# "crosshair" for locating center of screen for precision zoom

target.convert('RGB').save('rendering/number_theorems.png', 'PNG')

print(f"Time to run operation \n{max_iterations} on ({real_offset}, {-imaginary_offset}i) at [{width}x{height}]:", round(
    timeit.default_timer() - start, 3), "s")

# rgb (effect) filling
# if m < max_iterations:
#     if max_iterations - m < 70:
#         H = int(5*x/m)%255
#         V = 255
#     else:
#         V = 255
# else:
#     H = 255-int(x/3.5)
#     V = 200