from openai import OpenAI
from shared.config import Config


class OutlineSkill:
    """슬라이드 구성 기획 스킬 - GPT-5.4로 전체 목차 생성"""

    def __init__(self):
        self._client = OpenAI(api_key=Config.OPENAI_API_KEY)

    def execute(self, product_name: str, research_summary: str) -> list[str]:
        """
        상품 리서치를 바탕으로 슬라이드 목차 생성

        Args:
            product_name: 상품명
            research_summary: 리서치 요약 텍스트

        Returns:
            슬라이드 제목 리스트
        """
        prompt = f"""
B2B 상품소개서 슬라이드 목차를 작성해주세요.

상품명: {product_name}
리서치 요약:
{research_summary}

규칙:
- 5~7개 슬라이드로 구성
- 각 슬라이드 제목만 한 줄씩 출력
- 번호 없이 제목만 작성
"""
        response = self._client.chat.completions.create(
            model=Config.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
        )

        raw = response.choices[0].message.content
        # 줄바꿈으로 분리 후 빈 줄 제거
        return [line.strip() for line in raw.strip().split("\n") if line.strip()]
