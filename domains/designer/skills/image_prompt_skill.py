import google.generativeai as genai
from shared.config import Config


class ImagePromptSkill:
    """Gemini 2.5 Pro로 Imagen용 이미지 프롬프트 생성 스킬"""

    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self._model = genai.GenerativeModel(Config.GEMINI_MODEL)

    def execute(self, slide_title: str, design_plan: str) -> str:
        """
        디자인 기획을 바탕으로 Imagen 3 프롬프트 생성

        Args:
            slide_title: 슬라이드 제목
            design_plan: DesignPlanSkill이 생성한 디자인 방향

        Returns:
            Imagen 3에 전달할 영어 이미지 프롬프트
        """
        prompt = f"""
아래 슬라이드 디자인 기획을 바탕으로 Imagen 3 이미지 생성 프롬프트를 영어로 작성해주세요.

슬라이드 제목: {slide_title}
디자인 기획:
{design_plan}

규칙:
- 반드시 영어로 작성
- 구체적이고 시각적인 묘사 포함
- B2B 비즈니스 톤 유지
- 프롬프트 텍스트만 출력 (설명 없이)
"""
        response = self._model.generate_content(prompt)
        return response.text.strip()
