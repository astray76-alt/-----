from pptx.dml.color import RGBColor
from pptx.util import Pt


class ThemeSkill:
    """슬라이드 색상/폰트 테마 관리 스킬"""

    # 기본 테마 색상
    COLOR_TITLE = RGBColor(0x1F, 0x39, 0x64)    # 진한 남색
    COLOR_BODY = RGBColor(0x33, 0x33, 0x33)      # 진한 회색
    COLOR_ACCENT = RGBColor(0x2E, 0x75, 0xB6)    # 파란색 강조
    COLOR_WHITE = RGBColor(0xFF, 0xFF, 0xFF)      # 흰색
    COLOR_SUBTITLE = RGBColor(0xBD, 0xD7, 0xEE)  # 연한 파란색

    # 폰트 크기
    FONT_COVER_TITLE = Pt(44)
    FONT_COVER_SUBTITLE = Pt(24)
    FONT_SLIDE_TITLE = Pt(28)
    FONT_SLIDE_BODY = Pt(16)
    FONT_KEY_MESSAGE = Pt(14)
    FONT_CLOSING = Pt(40)

    def apply_background(self, slide, color: RGBColor) -> None:
        """슬라이드 배경색 적용"""
        fill = slide.background.fill
        fill.solid()
        fill.fore_color.rgb = color

    def apply_text_style(self, run, size: Pt, color: RGBColor, bold: bool = False, italic: bool = False) -> None:
        """텍스트 런에 폰트 스타일 일괄 적용"""
        run.font.size = size
        run.font.color.rgb = color
        run.font.bold = bold
        run.font.italic = italic
