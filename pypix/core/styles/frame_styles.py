from enum import Enum
from typing import Dict


class FrameStyle(Enum):
    """
    FrameStyle Enums
    """
    CLEAN = "clean"
    TECH = "tech"
    CREATIVE = "creative"
    PAY = "pay"
    CUSTOM_TEXT = "custom_text"
    SIMPLE = "simple"
    ROUNDED = "rounded"
    LABEL = "label"
    SCAN_ME_BASIC = "scan_me_basic"
    SCAN_ME_GRADIENT = "scan_me_gradient"
    SCAN_ME_DARK = "scan_me_dark"
    SCAN_ME_NEON = "scan_me_neon"
    SCAN_ME_PURPLE = "scan_me_purple"
    SCAN_ME_MINIMAL = "scan_me_minimal"

    def svg(self, custom_text: str = "") -> str:
        if self == FrameStyle.CUSTOM_TEXT:
            return generate_svg_with_text(custom_text)

        return FRAME_SVGS[self]


FRAME_SVGS: Dict[FrameStyle, str] = {
    FrameStyle.CLEAN: """
<svg width="500" height="500" xmlns="http://www.w3.org/2000/svg">
  <rect x="10" y="10" width="480" height="480" rx="30" ry="30"
        fill="none" stroke="#000000" stroke-width="15"/>
</svg>
""",
    FrameStyle.TECH: """
<svg width="500" height="500" xmlns="http://www.w3.org/2000/svg">
  <path d="M30,0 L0,0 L0,30 M470,0 L500,0 L500,30
           M30,500 L0,500 L0,470 M470,500 L500,500 L500,470"
        fill="none" stroke="#00ffcc" stroke-width="15"/>
</svg>
""",
    FrameStyle.CREATIVE: """
<svg width="500" height="500" xmlns="http://www.w3.org/2000/svg">
  <circle cx="250" cy="250" r="230" fill="none"
          stroke="#ff69b4" stroke-width="20" stroke-dasharray="20,10"/>
</svg>
""",
    FrameStyle.PAY: """
<svg width="500" height="500" xmlns="http://www.w3.org/2000/svg">
  <rect x="10" y="10" width="480" height="480" rx="40" ry="40"
        fill="none" stroke="#00BFA5" stroke-width="12"/>
  <text x="250" y="480" text-anchor="middle" font-size="28"
        font-family="Arial" fill="#00BFA5">Pague com PIX</text>
</svg>
""",
    FrameStyle.ROUNDED: """
<svg width="500" height="500" xmlns="http://www.w3.org/2000/svg">
  <rect x="10" y="10" width="480" height="480" 
    rx="10" ry="10" fill="none" stroke="#0984e3" stroke-width="10"/>
</svg>
""",
    FrameStyle.LABEL: """
<svg width="500" height="500" xmlns="http://www.w3.org/2000/svg">
  <rect x="10" y="10" width="480" height="480" rx="15" ry="15" fill="none" 
    stroke="#6c5ce7" stroke-width="6"/>
    <text x="250" y="470" text-anchor="middle" fill="#6c5ce7" font-size="20" 
  font-family="Arial">Pague com Pix</text>
</svg>
""",
    FrameStyle.SIMPLE: """
<svg width="500" height="500" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="20" width="480" height="480" rx="20" ry="20" 
    fill="none" stroke="#00B894" stroke-width="8"/>
</svg>
""",
    FrameStyle.SCAN_ME_BASIC: """
<svg width="500" height="500" xmlns="http://www.w3.org/2000/svg">
  <rect x="10" y="10" width="480" height="480" rx="25" ry="25"
        fill="none" stroke="#0984e3" stroke-width="10"/>
  <rect x="10" y="430" width="480" height="55" fill="#0984e3" rx="8" ry="8"/>
  <text x="250" y="470" text-anchor="middle" font-size="24"
        font-family="Arial" fill="#ffffff">SCAN ME</text>
</svg>""",
    FrameStyle.SCAN_ME_GRADIENT: """
<svg width="500" height="500" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#00b894;stop-opacity:1"/>
      <stop offset="100%" style="stop-color:#00b894;stop-opacity:1"/>
    </linearGradient>
  </defs>
  <rect x="10" y="10" width="480" height="480" rx="25" ry="25"
        fill="none" stroke="url(#grad)" stroke-width="12"/>
  <rect x="10" y="430" width="480" height="60" fill="#00b894" rx="10" ry="10"/>
  <text x="250" y="470" text-anchor="middle" font-size="24"
        font-family="Verdana" fill="#ffffff">SCAN ME</text>
</svg>""",
    FrameStyle.SCAN_ME_NEON: """
<svg width="500" height="500" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="20" width="460" height="460" rx="20" ry="20"
        fill="none" stroke="#a29bfe" stroke-width="10"/>
  <rect x="20" y="420" width="460" height="60" fill="#a29bfe" rx="8" ry="8"/>
  <text x="250" y="460" text-anchor="middle" font-size="24"
        font-family="Courier New" fill="#ffffff">SCAN ME</text>
</svg>""",
    FrameStyle.SCAN_ME_DARK: """
<svg width="500" height="500" xmlns="http://www.w3.org/2000/svg">
  <rect x="10" y="10" width="480" height="480" rx="25" ry="25"
        fill="none" stroke="#2d3436" stroke-width="10"/>
  <rect x="10" y="430" width="480" height="55" fill="#2d3436" rx="8" ry="8"/>
  <text x="250" y="470" text-anchor="middle" font-size="24"
        font-family="Arial" fill="#ffffff">SCAN ME</text>
</svg>
""",
    FrameStyle.SCAN_ME_PURPLE: """
<svg width="500" height="500" xmlns="http://www.w3.org/2000/svg">
  <rect x="15" y="15" width="470" height="470" rx="20" ry="20"
        fill="none" stroke="#6c5ce7" stroke-width="6"/>
  <rect x="15" y="425" width="470" height="57" fill="#6c5ce7" rx="8" ry="8"/>
  <text x="250" y="465" text-anchor="middle" font-size="22"
        font-family="Arial" font-weight="bold" fill="#ffffff">SCAN ME</text>
</svg>
""",
    FrameStyle.SCAN_ME_MINIMAL: """
<svg width="500" height="500" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="20" width="460" height="460" rx="15" ry="15"
        fill="none" stroke="#b2bec3" stroke-width="5"/>
  <rect x="20" y="440" width="460" height="40" fill="#b2bec3" rx="8" ry="8"/>
  <text x="250" y="468" text-anchor="middle" font-size="20"
        font-family="Courier New" fill="#2d3436">SCAN ME</text>
</svg>
"""
}


def generate_svg_with_text(text: str) -> str:
    return f"""
<svg width="500" height="500" xmlns="http://www.w3.org/2000/svg">
  <rect x="10" y="10" width="480" height="480" rx="25" ry="25"
        fill="none" stroke="#000000" stroke-width="10"/>
  <rect x="10" y="430" width="480" height="55" fill="#000000" rx="8" ry="8"/>
  <text x="250" y="470" text-anchor="middle" font-size="24"
        font-family="Arial" fill="#ffffff">{text}</text>
</svg>
"""
