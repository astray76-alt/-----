import google.generativeai as genai
from shared.config import Config


class DesignPlanSkill:
    """Gemini 2.5 Pro로 슬라이드 디자인 방향 기획 스킬"""

    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self._model = genai.GenerativeModel(Config.GEMINI_MODEL)

    def execute(self, slide_title: str, slide_body: str) -> str:
        """
        슬라이드 내용을 분석해 디자인 방향 기획

        Args:
            slide_title: 슬라이드 제목
            slide_body: 슬라이드 본문

        Returns:
            디자인 방향 텍스트 (레이아웃, 색상, 분위기 포함)
        """
        prompt = f"""
B2B 상품소개서 슬라이드 디자인을 기획해주세요.

슬라이드 제목: {slide_title}
슬라이드 본문: {slide_body}

다음 항목을 작성해주세요:
- 레이아웃: (텍스트와 이미지 배치 방향)
- 색상 테마: (주조색, 보조색, 분위기)
- 이미지 컨셉: (어떤 시각 이미지가 이 슬라이드에 적합한지)
"""
        response = self._model.generate_content(prompt)
        return response.text.strip()
