from enum import Enum


class BorderStyle(Enum):
    SQUARE = "square"
    ROUNDED = "rounded"
    CIRCLE = "circle"
    QUARTER_CIRCLE = "quarter_circle"
    SMOOTH_QUARTER_CIRCLE = "smooth_quarter_circle"
    CIRCULAR_QUARTER = "circular_quarter"
    CIRCULAR = "circular"
    ROUNDED_SQUARE = "rounded_square"


BORDER_SVGS = {
    BorderStyle.SQUARE: '''<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 14 14">
                <rect width="14" height="14" fill="white"/>
                <path d="M0,0v14h14V0H0z M12,12H2V2h10V12z"/>
            </svg>''',
    BorderStyle.ROUNDED: '''<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 14 14">
                <rect width="14" height="14" fill="white"/>
                <path d="M4.5,14h5.1C12,14,14,12,14,9.6V4.5C14,2,12,0,9.5,0H4.4C2,0,0,2,0,4.4v5.1C0,12,2,14,4.5,14z M12,4.8v4.4 c0,1.5-1.3,2.8-2.8,2.8H4.8C3.2,12,2,10.8,2,9.2V4.8C2,3.3,3.3,2,4.8,2h4.4C10.8,2,12,3.2,12,4.8z"/>
            </svg>''',
    BorderStyle.CIRCLE: '''<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 14 14">
                <rect width="14" height="14" fill="white"/>
                <path d="M0,7L0,7c0,3.9,3.1,7,7,7h0c3.9,0,7-3.1,7-7v0c0-3.9-3.1-7-7-7h0C3.1,0,0,3.1,0,7z M7,12L7,12c-2.8,0-5-2.2-5-5v0 c0-2.8,2.2-5,5-5h0c2.8,0,5,2.2,5,5v0C12,9.8,9.8,12,7,12z"/>
            </svg>''',
    BorderStyle.QUARTER_CIRCLE: '''<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 14 14">
                <rect width="14" height="14" fill="white"/>
                <path d="M0,0l0,7c0,3.9,3.1,7,7,7h0c3.9,0,7-3.1,7-7v0c0-3.9-3.1-7-7-7H0z M7,12L7,12c-2.8,0-5-2.2-5-5V2h5c2.8,0,5,2.2,5,5v0 C12,9.8,9.8,12,7,12z"/>
            </svg>''',
    BorderStyle.SMOOTH_QUARTER_CIRCLE: '''<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 14 14">
                <rect width="14" height="14" fill="white"/>
                <path d="M0,0l0,7c0,3.9,3.1,7,7,7h7V7c0-3.9-3.1-7-7-7H0z M12,12H7c-2.8,0-5-2.2-5-5v0c0-2.8,2.2-5,5-5h0c2.8,0,5,2.2,5,5V12z"/>
            </svg>''',
    BorderStyle.CIRCULAR_QUARTER: '''<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 14 14">
                <rect width="14" height="14" fill="white"/>
                <path d="M0,0l0,7c0,3.9,3.1,7,7,7h7V7c0-3.9-3.1-7-7-7H0z M7,12L7,12c-2.8,0-5-2.2-5-5v0c0-2.8,2.2-5,5-5h0c2.8,0,5,2.2,5,5v0 C12,9.8,9.8,12,7,12z"/>
            </svg>''',
    BorderStyle.CIRCULAR: '''<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 14 14">
                <rect width="14" height="14" fill="white"/>
                <path d="M0,0l0,14h14V0H0z M7,12L7,12c-2.8,0-5-2.2-5-5v0c0-2.8,2.2-5,5-5h0c2.8,0,5,2.2,5,5v0C12,9.8,9.8,12,7,12z"/>
            </svg>''',
    BorderStyle.ROUNDED_SQUARE: '''<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 14 14">
                <rect width="14" height="14" fill="white"/>
                <path d="M0,0v9.6C0,12,2,14,4.4,14h5.1C12,14,14,12,14,9.6V4.4C14,2,12,0,9.6,0H0z M9.2,12H4.8C3.3,12,2,10.7,2,9.2V2h7.2 C10.7,2,12,3.3,12,4.8v4.4C12,10.7,10.7,12,9.2,12z"/>
            </svg>'''
}
