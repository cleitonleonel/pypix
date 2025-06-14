import qrcode
from qrcode.image.styledpil import StyledPilImage
from PIL import Image
from typing import Optional
from pypix.core.styles.qr_styler import QRCodeStyler, GradientMode
from pypix.core.styles.marker_styles import MarkerStyle, MARKER_SVGS
from pypix.core.styles.border_styles import BorderStyle, BORDER_SVGS
from pypix.core.styles.line_styles import LineStyle, LINE_STYLES
from pypix.core.styles.frame_styles import FrameStyle
from pypix.core.utils.image_utils import (
    svg_to_pil,
    add_center_image,
    add_center_gif,
    apply_frame_qr
)


class GeneratorQR(qrcode.QRCode):
    """Generator class for creating custom QR codes with various styles and options.
    This class extends the qrcode.QRCode class and provides methods to create
    custom QR codes with features like size, border, center image, marker style,
    border style, line style, gradient color, gradient mode, frame style, and style mode.
    It also includes methods to add GIFs to the QR code and draw custom position patterns.
    Attributes:
        border (int): Size of the border around the QR code.
        box_size (int): Size of each QR code module.
        error_correction (int): Error correction level for the QR code.
        version (int): Version of the QR code.
        frame_style (FrameStyle): Style for the frame around the QR code.
        style_mode (str): Mode for styling, e.g., "Normal" or "Full".
    Methods:
        create_custom_qr(data: str, size: int = 10, border: int = 4,
                          center_image: Optional[str] = None,
                          marker_style: MarkerStyle = MarkerStyle.PLUS,
                          border_style: BorderStyle = BorderStyle.CIRCLE,
                          line_style: LineStyle = LineStyle.ROUNDED,
                          gradient_color: str = "blue",
                          gradient_mode: GradientMode = GradientMode.GRADIENT,
                          frame_style: FrameStyle = None,
                          style_mode: str = 'Normal') -> Image.Image:
            Creates a custom QR code image with various styles and options.
        add_gif(img: Image.Image, center_gif: str, gif_len_percent: float = 0.25,
                radius: float = None) -> tuple[list[Any], int]:
            Adds a GIF to the center of the QR code image.
        _draw_custom_position_patterns(img: Image.Image, border_img: Image.Image,
                                       center_img: Image.Image, size: int, border: int) -> None:
            Draws custom patterns at the corners of the QR code image.

    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.border = None
        self.box_size = None
        self.error_correction = None
        self.version = None
        self.frame_style = None
        self.style_mode = None

    def create_custom_qr(
            self,
            data: str,
            size: int = 10,
            border: int = 4,
            center_image: Optional[str] = None,
            marker_style: MarkerStyle = MarkerStyle.PLUS,
            border_style: BorderStyle = BorderStyle.CIRCLE,
            line_style: LineStyle = LineStyle.ROUNDED,
            gradient_color: str = "blue",
            gradient_mode: GradientMode = GradientMode.GRADIENT,
            frame_style: FrameStyle = None,
            style_mode: str = 'Normal',
    ) -> Image.Image:
        """This function creates a custom QR code image with various styles and options.
        It allows customization of size, border, center image, marker style, border style,
        line style, gradient color, gradient mode, frame style, and style mode.
        Args:
            data (str): The data to encode in the QR code.
            size (int): Size of each QR code module.
            border (int): Size of the border around the QR code.
            center_image (Optional[str]): Path to an image to be placed at the center of the QR code.
            marker_style (MarkerStyle): Style for the position markers.
            border_style (BorderStyle): Style for the border around the QR code.
            line_style (LineStyle): Style for the lines in the QR code.
            gradient_color (str): Color for the gradient effect.
            gradient_mode (GradientMode): Mode for the gradient effect.
            frame_style (FrameStyle): Style for the frame around the QR code.
            style_mode (str): Mode for styling, e.g., "Normal" or "Full".

        Returns:
            Image.Image: The generated QR code image with the specified styles.

        """
        self.version = 7
        self.error_correction = qrcode.constants.ERROR_CORRECT_H
        self.box_size = size
        self.border = border
        self.frame_style = frame_style
        self.style_mode = style_mode

        self.add_data(data)
        self.make(fit=True)

        img = self.make_image(
            fill_color="black",
            back_color="white",
            image_factory=StyledPilImage,
            module_drawer=LINE_STYLES[line_style]
        )
        img = img.convert("RGBA")

        img = QRCodeStyler.apply_gradient(
            img,
            color=gradient_color,
            mode=gradient_mode
        )

        border_img = svg_to_pil(BORDER_SVGS[border_style], size * 7)
        center_img = svg_to_pil(MARKER_SVGS[marker_style], size * 3)

        self._draw_custom_position_patterns(
            img,
            border_img,
            center_img,
            size,
            border
        )

        if self.style_mode == "Full":
            img = QRCodeStyler.apply_gradient(
                img,
                color=gradient_color,
                mode=gradient_mode
            )

        if center_image:
            add_center_image(img, center_image)

        if self.frame_style:
            svg_str = self.frame_style
            if not isinstance(self.frame_style, str):
                svg_str = self.frame_style.svg()
            frame_img = svg_to_pil(svg_str, size=500)
            img = apply_frame_qr(frame_img, img)

        return img

    def add_center_animation(
            self,
            img: Image.Image,
            center_gif: str,
            gif_len_percent: 0.25,
            radius: float = None
    ):
        """This function takes a QR code image and a GIF file, resizes the GIF to fit
        the center of the QR code, and adds it to the image. The GIF is resized based
        on the specified percentage of the QR code size, and corners can be rounded
        if a radius is provided. The function returns the modified image frames and
        the duration of the GIF.

        Args:
            img (Image.Image): The QR code image to which the GIF will be added.
            center_gif (str): Path to the GIF file to be added.
            gif_len_percent (float): Percentage of the QR code size that the GIF should occupy.
            radius (float, optional): Radius for rounding the corners of the GIF. Defaults to None.
        Returns:
            tuple: A tuple containing the list of frames and the duration of the GIF.
        """
        is_frame_style = isinstance(self.frame_style, FrameStyle)
        frames, duration = add_center_gif(
            img,
            center_gif,
            gif_len_percent,
            radius,
            is_frame_style
        )
        return frames, duration

    @staticmethod
    def _draw_custom_position_patterns(
            img: Image.Image,
            border_img: Image.Image,
            center_img: Image.Image,
            size: int,
            border: int
    ) -> None:
        """This function draws custom patterns at the corners of the QR code image.
        It places a border pattern at the top-left, top-right, and bottom-left corners,
        and a center pattern in the middle of the QR code.
        The patterns are drawn using the provided images and the specified size and border.

        Args:
            img (Image.Image): The QR code image to modify.
            border_img (Image.Image): Image for the border pattern.
            center_img (Image.Image): Image for the center pattern.
            size (int): Size of the QR code modules.
            border (int): Size of the border around the QR code.
        Returns:
            None: The function modifies the image in place.
        """

        def draw_pattern(x: int, y: int) -> None:
            pattern = Image.new('RGBA', (size * 7, size * 7), (0, 0, 0, 0))
            pattern.paste(border_img, (0, 0), border_img)
            pattern.paste(center_img, (size * 2, size * 2), center_img)
            img.paste(pattern, (x, y), pattern)

        draw_pattern(border * size, border * size)
        draw_pattern(img.width - size * 7 - border * size, border * size)
        draw_pattern(border * size, img.height - size * 7 - border * size)
