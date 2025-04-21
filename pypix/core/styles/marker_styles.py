from enum import Enum


class MarkerStyle(Enum):
    SQUARE = "square"
    ROUNDED = "rounded"
    CIRCLE = "circle"
    QUARTER_CIRCLE = "quarter_circle"
    STAR = "star"
    DIAMOND = "diamond"
    PLUS = "plus"


MARKER_SVGS = {
    MarkerStyle.SQUARE: '''<svg xmlns="http://www.w3.org/2000/svg" width="6" height="6"><rect width="6" height="6"/></svg>''',
    MarkerStyle.ROUNDED: '''<svg xmlns="http://www.w3.org/2000/svg" width="6" height="6"><path d="M6,1.7v2.7C6,5.2,5.2,6,4.3,6H1.7C0.7,6,0,5.3,0,4.3V1.7C0,0.8,0.8,0,1.7,0h2.7C5.3,0,6,0.7,6,1.7z"/></svg>''',
    MarkerStyle.CIRCLE: '''<svg xmlns="http://www.w3.org/2000/svg" width="6" height="6"><circle cx="3" cy="3" r="3"/></svg>''',
    MarkerStyle.QUARTER_CIRCLE: '''<svg xmlns="http://www.w3.org/2000/svg" width="6" height="6"><path d="M3,6L3,6C1.3,6,0,4.7,0,3l0-3l3,0c1.7,0,3,1.3,3,3v0C6,4.7,4.7,6,3,6z"/></svg>''',
    MarkerStyle.STAR: '''<svg xmlns="http://www.w3.org/2000/svg" width="6" height="6"><path d="M3.2,0.3l0.6,1.3C4,1.8,4.1,1.9,4.3,1.9l1.4,0.2c0.2,0,0.3,0.3,0.2,0.5l-1,1C4.7,3.7,4.7,3.9,4.7,4.1L5,5.5 c0,0.2-0.2,0.4-0.4,0.3L3.3,5.2c-0.2-0.1-0.4-0.1-0.6,0L1.4,5.8C1.2,5.9,1,5.8,1,5.5l0.2-1.4c0-0.2,0-0.4-0.2-0.5l-1-1 C-0.1,2.4,0,2.2,0.2,2.1l1.4-0.2c0.2,0,0.4-0.2,0.5-0.3l0.6-1.3C2.9,0.1,3.1,0.1,3.2,0.3z"/></svg>''',
    MarkerStyle.DIAMOND: '''<svg xmlns="http://www.w3.org/2000/svg" width="6" height="6"><rect x="0.9" y="0.9" transform="matrix(0.7071 -0.7071 0.7071 0.7071 -1.2426 3)" width="4.2" height="4.2"/></svg>''',
    MarkerStyle.PLUS: '''<svg xmlns="http://www.w3.org/2000/svg" width="6" height="6"><polygon points="6,1.5 4.5,1.5 4.5,0 1.5,0 1.5,1.5 0,1.5 0,4.5 1.5,4.5 1.5,6 4.5,6 4.5,4.5 6,4.5"/></svg>'''
}
