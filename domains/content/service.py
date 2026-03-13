from domains.content.skills.outline_skill import OutlineSkill
from domains.content.skills.copywriting_skill import CopywritingSkill
from domains.content.skills.key_message_skill import KeyMessageSkill


class ContentService:
    """
    콘텐츠 생성 에이전트 서비스 클래스
    - OutlineSkill → CopywritingSkill → KeyMessageSkill 순으로 실행
    """

    def __init__(self):
        self._outline = OutlineSkill()
        self._copywriting = CopywritingSkill()
        self._key_message = KeyMessageSkill()

    def generate_all_slides(self, product_name: str, research_results: dict) -> list[dict]:
        """
        리서치 결과로 전체 슬라이드 콘텐츠 생성

        Args:
            product_name: 상품명
            research_results: ResearchService.research_product() 반환값

        Returns:
            슬라이드별 콘텐츠 리스트 (title, body, key_message)
        """
        # 전체 리서치를 합쳐 목차 생성
        combined_summary = "\n".join(research_results.values())
        slide_titles = self._outline.execute(product_name, combined_summary)

        slides = []
        for title in slide_titles:
            # 제목과 가장 관련 있는 카테고리 요약 선택
            summary = self._pick_relevant_summary(title, research_results)

            body = self._copywriting.execute(title, summary)
            key_message = self._key_message.execute(title, body)

            slides.append({
                "title": title,
                "body": body,
                "key_message": key_message,
            })

        return slides

    def _pick_relevant_summary(self, title: str, research_results: dict) -> str:
        """슬라이드 제목과 가장 관련 있는 리서치 카테고리 요약 반환"""
        keyword_map = {
            "overview": ["소개", "개요", "특징", "기능"],
            "benefits": ["효과", "도입", "사례", "장점", "혜택"],
            "competitors": ["비교", "경쟁", "차별", "우위"],
            "pricing": ["가격", "요금", "플랜", "비용"],
        }

        for category, keywords in keyword_map.items():
            if any(kw in title for kw in keywords):
                return research_results.get(category, "")

        # 매칭 없으면 overview 반환
        return research_results.get("overview", "")
