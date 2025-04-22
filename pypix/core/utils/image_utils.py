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


def apply_frame_qr(frame_img: Image.Image, qr_img: Image.Image, scale: float = 0.7) -> Image.Image:
    frame_img = frame_img.convert("RGBA")
    qr_img = qr_img.convert("RGBA")

    new_qr_size = int(frame_img.width * scale) + int(frame_img.height * scale) // 10
    qr_img = qr_img.resize((new_qr_size, new_qr_size), Image.Resampling.LANCZOS)

    x = (frame_img.width - new_qr_size) // 2
    y = int(((frame_img.height - new_qr_size) // 2) - 30)

    frame_img.paste(qr_img, (x, y), qr_img)

    return frame_img
