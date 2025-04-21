from enum import Enum
from PIL import Image, ImageColor


class GradientMode(Enum):
    NORMAL = "normal"
    GRADIENT = "gradient"
    MULTI = "multi"


class QRCodeStyler:
    @staticmethod
    def apply_gradient(
        img: Image.Image,
        color: str | tuple = "blue",
        mode: GradientMode = GradientMode.GRADIENT
    ) -> Image.Image:
        width, height = img.size

        if isinstance(color, str):
            color = ImageColor.getrgb(color)

        gradient = Image.new('RGB', (width, height), color=0)

        for x in range(width):
            for y in range(height):
                if mode == GradientMode.MULTI:
                    r = int((x / width) * 255)
                    g = int((y / height) * 255)
                    b = 255 - r
                    gradient.putpixel((x, y), (r, g, b))

                elif mode == GradientMode.GRADIENT:
                    factor = (x + y) / (width + height)
                    r = int(color[0] * factor)
                    g = int(color[1] * factor)
                    b = int(color[2] * factor)
                    gradient.putpixel((x, y), (r, g, b))

                elif mode == GradientMode.NORMAL:
                    gradient.putpixel((x, y), color)

        mask = img.convert('L').point(lambda i: i < 255 and 255)
        return Image.composite(gradient, img.convert('RGB'), mask)
