from PIL import Image, ImageDraw

def mandelbrot(c, max_iterations):
    z = 0
    n = 0
    while abs(z) <= 2 and n < max_iterations:
        z = z*z + c
        n += 1
    return n
    # z_n+1 = z_n^2 + c

def clamp(val, min, max):
    return min(max(val, min), max)

real_offset = -2
imaginary_offset = -1

width = 600
height = 600

# "colorful" colour system being used is HSV due to the easy functionality to scroll through the entire colour spectrum, allowing for easily customisable palettes. RGB is useful for a static colour palette.
target = Image.new('HSV', (width, height), (220, 1, 1))
draw = ImageDraw.Draw(target)

max_iterations = 80

for x in range(0, width):
    for y in range(0, height):
        c = complex(real_offset + (x / width) * 2,
                    imaginary_offset + (y / height) * 2)
        m = mandelbrot(c, max_iterations)
        H = int(m)
        S = 255
        V = 255 if m < max_iterations else 10
        # color = 255 - int(m * 255 / max_iterations) # WORKS ON RGB COLOUR SYSTEM ONLY
        draw.point([x, y], (H, S, V))

target.convert('RGB').save('mandelbrot_mono.png', 'PNG')