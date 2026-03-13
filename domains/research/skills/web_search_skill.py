import requests
from shared.config import Config


class WebSearchSkill:
    """Brave Search API 호출 스킬"""

    _BASE_URL = "https://api.search.brave.com/res/v1/web/search"

    def __init__(self):
        # 요청 헤더 (API 키 포함)
        self._headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": Config.BRAVE_API_KEY,
        }

    def execute(self, query: str, count: int = None) -> list[dict]:
        """
        단일 쿼리로 웹 검색 실행

        Args:
            query: 검색어
            count: 결과 수

        Returns:
            원시 검색 결과 리스트 (title, url, description)
        """
        params = {
            "q": query,
            "count": count or Config.BRAVE_SEARCH_COUNT,
            "search_lang": "ko",
            "country": "KR",
        }

        response = requests.get(self._BASE_URL, headers=self._headers, params=params)
        response.raise_for_status()

        results = response.json().get("web", {}).get("results", [])

        return [
            {
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "description": item.get("description", ""),
            }
            for item in results
        ]
