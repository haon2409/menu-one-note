from PIL import Image, ImageDraw

width, height = 600, 800
line_spacing = 30
bg_color = (255, 255, 255)
line_color = (200, 200, 200)

image = Image.new("RGB", (width, height), bg_color)
draw = ImageDraw.Draw(image)

for y in range(0, height, line_spacing):
    draw.line([(0, y), (width, y)], fill=line_color, width=1)

image.save("lined_background.png")
