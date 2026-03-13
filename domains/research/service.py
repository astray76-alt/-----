from domains.research.skills.web_search_skill import WebSearchSkill
from domains.research.skills.filter_skill import FilterSkill
from domains.research.skills.summarize_skill import SummarizeSkill


class ResearchService:
    """
    리서치 에이전트 서비스 클래스
    - WebSearchSkill → FilterSkill → SummarizeSkill 순으로 실행
    """

    def __init__(self):
        self._search = WebSearchSkill()
        self._filter = FilterSkill()
        self._summarize = SummarizeSkill()

    def research_product(self, product_name: str) -> dict:
        """
        상품 관련 정보를 다각도로 수집 후 요약 텍스트 반환

        Args:
            product_name: 조사할 상품명

        Returns:
            카테고리별 요약 텍스트 딕셔너리
        """
        queries = {
            "overview": f"{product_name} 제품 소개 특징",
            "benefits": f"{product_name} B2B 도입 효과 사례",
            "competitors": f"{product_name} 경쟁사 비교 분석",
            "pricing": f"{product_name} 가격 요금제",
        }

        summaries = {}
        for category, query in queries.items():
            raw = self._search.execute(query)
            filtered = self._filter.execute(raw)
            summaries[category] = self._summarize.execute(filtered)

        return summaries
