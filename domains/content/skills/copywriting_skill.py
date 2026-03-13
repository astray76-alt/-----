from openai import OpenAI
from shared.config import Config


class CopywritingSkill:
    """슬라이드 본문 텍스트 작성 스킬 - GPT-5.4로 불릿 포인트 생성"""

    def __init__(self):
        self._client = OpenAI(api_key=Config.OPENAI_API_KEY)

    def execute(self, slide_title: str, research_summary: str) -> str:
        """
        슬라이드 제목에 맞는 본문 불릿 포인트 생성

        Args:
            slide_title: 슬라이드 제목
            research_summary: 해당 슬라이드 관련 리서치 요약

        Returns:
            불릿 포인트 본문 텍스트
        """
        prompt = f"""
B2B 상품소개서의 '{slide_title}' 슬라이드 본문을 작성해주세요.

참고 자료:
{research_summary}

규칙:
- 3~5개 불릿 포인트
- 각 항목은 '• '로 시작
- 한 항목당 20~40자 이내
- 구체적인 수치나 효과 포함
"""
        response = self._client.chat.completions.create(
            model=Config.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
        )

        return response.choices[0].message.content.strip()
