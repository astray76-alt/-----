import requests
from shared.config import Config


class ResearchService:
    """
    리서치 에이전트 서비스 클래스
    - Brave Search API를 통해 B2B 상품 관련 정보를 수집
    """

    # Brave Search REST API 엔드포인트
    _BASE_URL = "https://api.search.brave.com/res/v1/web/search"

    def __init__(self):
        # 요청 헤더 설정 (API 키 포함)
        self._headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": Config.BRAVE_API_KEY,
        }

    def search(self, query: str, count: int = None) -> list[dict]:
        """
        Brave Search로 웹 검색 수행

        Args:
            query: 검색어
            count: 가져올 결과 수 (기본값은 Config 설정 사용)

        Returns:
            검색 결과 리스트 (title, url, description 포함)
        """
        params = {
            "q": query,
            "count": count or Config.BRAVE_SEARCH_COUNT,
            "search_lang": "ko",
            "country": "KR",
        }

        response = requests.get(self._BASE_URL, headers=self._headers, params=params)
        response.raise_for_status()

        # 웹 검색 결과 파싱
        results = response.json().get("web", {}).get("results", [])

        return [
            {
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "description": item.get("description", ""),
            }
            for item in results
        ]

    def research_product(self, product_name: str) -> dict:
        """
        상품 관련 정보를 다각도로 수집

        Args:
            product_name: 조사할 상품명

        Returns:
            카테고리별 검색 결과 딕셔너리
        """
        # 상품의 다양한 측면을 검색
        queries = {
            "overview": f"{product_name} 제품 소개 특징",
            "benefits": f"{product_name} B2B 도입 효과 사례",
            "competitors": f"{product_name} 경쟁사 비교 분석",
            "pricing": f"{product_name} 가격 요금제",
        }

        results = {}
        for category, query in queries.items():
            results[category] = self.search(query)

        return results

    def summarize_results(self, search_results: list[dict]) -> str:
        """
        검색 결과 리스트를 텍스트로 요약

        Args:
            search_results: search() 반환값

        Returns:
            결합된 텍스트 요약
        """
        lines = []
        for item in search_results:
            if item["description"]:
                lines.append(f"- {item['title']}: {item['description']}")

        return "\n".join(lines)
