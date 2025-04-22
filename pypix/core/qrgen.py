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
    apply_frame_qr
)


class Generator(qrcode.QRCode):

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

    def _draw_custom_position_patterns(
        self,
        img: Image.Image,
        border_img: Image.Image,
        center_img: Image.Image,
        size: int,
        border: int
    ) -> None:
        def draw_pattern(x: int, y: int) -> None:
            pattern = Image.new('RGBA', (size * 7, size * 7), (0, 0, 0, 0))
            pattern.paste(border_img, (0, 0), border_img)
            pattern.paste(center_img, (size * 2, size * 2), center_img)
            img.paste(pattern, (x, y), pattern)

        draw_pattern(border * size, border * size)
        draw_pattern(img.width - size * 7 - border * size, border * size)
        draw_pattern(border * size, img.height - size * 7 - border * size)
