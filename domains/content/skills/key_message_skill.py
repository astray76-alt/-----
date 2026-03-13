from openai import OpenAI
from shared.config import Config


class KeyMessageSkill:
    """핵심 메시지 추출 스킬 - 슬라이드를 관통하는 한 문장 생성"""

    def __init__(self):
        self._client = OpenAI(api_key=Config.OPENAI_API_KEY)

    def execute(self, slide_title: str, body_text: str) -> str:
        """
        슬라이드 본문에서 핵심 메시지 한 문장 추출

        Args:
            slide_title: 슬라이드 제목
            body_text: CopywritingSkill이 생성한 본문 텍스트

        Returns:
            핵심 메시지 한 문장
        """
        prompt = f"""
아래 슬라이드 내용을 한 문장으로 압축해주세요.

슬라이드 제목: {slide_title}
본문:
{body_text}

규칙:
- 30자 이내
- 의사결정자(임원, 구매담당자)에게 설득력 있는 문장
- 문장 부호 포함한 완전한 문장으로 작성
"""
        response = self._client.chat.completions.create(
            model=Config.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
        )

        return response.choices[0].message.content.strip()
