from openai import OpenAI
from shared.config import Config


class ContentService:
    """
    콘텐츠 생성 에이전트 서비스 클래스
    - GPT-5.4를 사용해 B2B 상품소개서 슬라이드 텍스트 생성
    """

    def __init__(self):
        # OpenAI 클라이언트 초기화
        self._client = OpenAI(api_key=Config.OPENAI_API_KEY)

    def generate_slide_content(self, slide_type: str, research_summary: str) -> dict:
        """
        슬라이드 유형에 맞는 텍스트 콘텐츠 생성

        Args:
            slide_type: 슬라이드 유형 (overview / benefits / competitors / pricing)
            research_summary: ResearchService에서 수집한 요약 텍스트

        Returns:
            슬라이드 콘텐츠 딕셔너리 (title, body, key_message 포함)
        """
        prompt = f"""
당신은 B2B 영업 전문가이자 상품소개서 작성 전문가입니다.
아래 리서치 자료를 바탕으로 '{slide_type}' 슬라이드의 텍스트를 작성해주세요.

리서치 자료:
{research_summary}

다음 형식으로 응답해주세요:
- 제목: (슬라이드 제목, 15자 이내)
- 본문: (핵심 내용 3~5개 불릿 포인트)
- 핵심 메시지: (슬라이드를 관통하는 한 문장)
"""
        response = self._client.chat.completions.create(
            model=Config.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
        )

        raw_text = response.choices[0].message.content

        # 응답에서 각 항목 파싱
        return {
            "slide_type": slide_type,
            "raw": raw_text,
            "title": self._parse_field(raw_text, "제목"),
            "body": self._parse_field(raw_text, "본문"),
            "key_message": self._parse_field(raw_text, "핵심 메시지"),
        }

    def generate_all_slides(self, research_results: dict) -> list[dict]:
        """
        전체 슬라이드 콘텐츠 일괄 생성

        Args:
            research_results: ResearchService.research_product() 반환값

        Returns:
            슬라이드별 콘텐츠 리스트
        """
        slides = []
        for slide_type, results in research_results.items():
            # 검색 결과를 텍스트로 변환
            summary = "\n".join(
                f"- {item['title']}: {item['description']}"
                for item in results
                if item["description"]
            )
            slide = self.generate_slide_content(slide_type, summary)
            slides.append(slide)

        return slides

    def _parse_field(self, text: str, field_name: str) -> str:
        """
        GPT 응답에서 특정 필드 추출

        Args:
            text: GPT 전체 응답 텍스트
            field_name: 추출할 필드명 (예: '제목', '본문')

        Returns:
            추출된 필드 값 문자열
        """
        keyword = f"- {field_name}:"
        if keyword in text:
            # 해당 필드부터 다음 줄까지 추출
            after = text.split(keyword)[-1]
            return after.split("\n- ")[0].strip()
        return ""
