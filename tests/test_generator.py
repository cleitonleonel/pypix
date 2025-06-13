import pytest
from pypix.core.qrgen import GeneratorQR
from pypix.core.styles.marker_styles import MarkerStyle
from pypix.core.styles.border_styles import BorderStyle
from pypix.core.styles.line_styles import LineStyle
from pypix.core.styles.qr_styler import QRCodeStyler, GradientMode


@pytest.mark.parametrize("style_mode", [GradientMode.NORMAL, GradientMode.GRADIENT, GradientMode.MULTI])
@pytest.mark.parametrize("color", ["red", "blue", "green", "#FF00FF"])
def test_generate_qr_with_styles(style_mode, color):
    generator = GeneratorQR()
    generator.style_mode = style_mode

    QRCodeStyler.mode = style_mode
    QRCodeStyler.color = color

    img = generator.create_custom_qr(
        data="https://example.com",
        size=10,
        border=4,
        center_image=None,
        marker_style=MarkerStyle.PLUS,
        border_style=BorderStyle.CIRCLE,
        line_style=LineStyle.ROUNDED,
    )

    assert img is not None
    assert img.size[0] > 0 and img.size[1] > 0
    assert img.mode in ["RGB", "RGBA"]
