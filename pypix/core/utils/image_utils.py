from typing import Any
from PIL import (
    Image,
    ImageDraw,
    ImageSequence
)

import io
import cairosvg


def svg_to_pil(svg_string: str, size: int) -> Image.Image:
    """Convert an SVG string to a PIL Image with a specified size.
    Args:
        svg_string (str): The SVG content as a string.
        size (int): The desired width and height for the output image.
    Returns:
        Image.Image: A PIL Image object created from the SVG string.

    """
    png_data = cairosvg.svg2png(
        bytestring=svg_string.encode('utf-8'),
        output_width=size,
        output_height=size
    )
    img = Image.open(io.BytesIO(png_data))
    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    return img


def add_center_image(
        img: Image.Image,
        center_image: str,
        radius: int = None
) -> None:
    """Add a rounded center image to the given image.
    Args:
        img (Image.Image): The main image to which the center image will be added.
        center_image (str): Path to the center image file.
        radius (int, optional): Radius for rounding the corners of the center image. Defaults to None.
    Returns:
        None: The function modifies the original image in place.

    """
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


def add_center_gif(
        img: Image.Image,
        center_gif: str,
        gif_len_percent: 0.25,
        radius: float = None,
        is_frame_style: bool = False
) -> tuple[list[Any], int]:
    """Add a rounded GIF to the center of the given image.
    Args:
        img (Image.Image): The main image to which the GIF will be added.
        center_gif (str): Path to the GIF file to be added.
        gif_len_percent (float): Percentage of the QR code size that the GIF should occupy.
        radius (float, optional): Radius for rounding the corners of the GIF. Defaults to None.
        is_frame_style (bool): Whether the GIF is a frame style. Defaults to False.
    Returns:
        tuple: A tuple containing a list of frames and the duration of the GIF.

    """
    original_gif = Image.open(center_gif)
    center_size_img = min(img.width, img.height) // 2
    new_gif_len = int(center_size_img * gif_len_percent)
    gif_size = (new_gif_len, new_gif_len)
    pos_x = (img.width - gif_size[0]) // 2
    pos_y = (img.height - gif_size[1]) // 2
    if is_frame_style:
        pos_y = int(pos_y - int(gif_len_percent * 50))  # Adjust position for frame style
    paste_position = (pos_x, pos_y)

    if radius is None:
        final_radius = min(gif_size) // 2
    else:
        final_radius = int(min(gif_size) * radius)

    mask = Image.new("L", gif_size, 0)
    draw = ImageDraw.Draw(mask)

    draw.rounded_rectangle(
        (0, 0, gif_size[0], gif_size[1]),
        radius=final_radius,
        fill=255
    )
    frames_finais = []

    for frame_gif in ImageSequence.Iterator(original_gif):
        img_qr_com_logo_frame = img.copy()
        frame_gif_rgba = frame_gif.convert("RGBA")
        frame_gif_resized = frame_gif_rgba.resize(
            gif_size,
            Image.Resampling.LANCZOS
        )
        img_qr_com_logo_frame.paste(frame_gif_resized, paste_position, mask)
        frames_finais.append(img_qr_com_logo_frame)

    duration = original_gif.info.get('duration', 100)

    return frames_finais, duration


def apply_frame_qr(
        frame_img: Image.Image,
        qr_img: Image.Image,
        scale: float = 0.7
) -> Image.Image:
    """Apply a frame to a QR code image.
    Args:
        frame_img (Image.Image): The frame image to be applied.
        qr_img (Image.Image): The QR code image to which the frame will be applied.
        scale (float): Scale factor for resizing the QR code image.
    Returns:
        Image.Image: The QR code image with the frame applied.

    """
    frame_img = frame_img.convert("RGBA")
    qr_img = qr_img.convert("RGBA")

    new_qr_size = int(frame_img.width * scale) + int(frame_img.height * scale) // 10
    qr_img = qr_img.resize((new_qr_size, new_qr_size), Image.Resampling.LANCZOS)

    x = (frame_img.width - new_qr_size) // 2
    y = int(((frame_img.height - new_qr_size) // 2) - 30)

    frame_img.paste(qr_img, (x, y), qr_img)

    return frame_img
