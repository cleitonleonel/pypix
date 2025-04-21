import cairosvg
from PIL import Image, ImageDraw
import io


def svg_to_pil(svg_string: str, size: int) -> Image.Image:
    png_data = cairosvg.svg2png(
        bytestring=svg_string.encode('utf-8'),
        output_width=size,
        output_height=size
    )
    img = Image.open(io.BytesIO(png_data))
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    return img


def add_center_image(img: Image.Image, center_image: str, radius: int = None) -> None:
    center_img = Image.open(center_image).convert("RGBA")
    center_size = min(img.width, img.height) // 3
    center_img = center_img.resize((center_size, center_size), Image.LANCZOS)

    if radius is None:
        radius = center_size // 2

    mask = Image.new("L", center_img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, center_size, center_size), radius=radius, fill=255)

    rounded_center = Image.new("RGBA", center_img.size)
    rounded_center.paste(center_img, (0, 0), mask)

    center_pos = (
        (img.width - center_size) // 2,
        (img.height - center_size) // 2
    )

    img.paste(rounded_center, center_pos, rounded_center)
