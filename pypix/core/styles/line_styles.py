from enum import Enum
from qrcode.image.styles.moduledrawers import (
    SquareModuleDrawer,
    GappedSquareModuleDrawer,
    CircleModuleDrawer,
    RoundedModuleDrawer,
    VerticalBarsDrawer,
    HorizontalBarsDrawer,
)


class LineStyle(Enum):
    SQUARE = "square"
    GAPPED_SQUARE = "gapped_square"
    CIRCLE = "circle"
    ROUNDED = "rounded"
    VERTICAL_BARS = "vertical_bars"
    HORIZONTAL_BARS = "horizontal_bars"


LINE_STYLES = {
    LineStyle.SQUARE: SquareModuleDrawer(),
    LineStyle.GAPPED_SQUARE: GappedSquareModuleDrawer(),
    LineStyle.CIRCLE: CircleModuleDrawer(),
    LineStyle.ROUNDED: RoundedModuleDrawer(),
    LineStyle.VERTICAL_BARS: VerticalBarsDrawer(),
    LineStyle.HORIZONTAL_BARS: HorizontalBarsDrawer(),
}
