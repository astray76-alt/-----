class FilterSkill:
    """검색 결과 필터링 스킬 - 설명 없는 항목 및 중복 URL 제거"""

    def execute(self, results: list[dict]) -> list[dict]:
        """
        관련성 낮은 결과 필터링

        Args:
            results: WebSearchSkill 반환값

        Returns:
            필터링된 검색 결과 리스트
        """
        seen_urls = set()
        filtered = []

        for item in results:
            # 설명이 없는 항목 제거
            if not item.get("description"):
                continue

            # 중복 URL 제거
            if item["url"] in seen_urls:
                continue

            seen_urls.add(item["url"])
            filtered.append(item)

        return filtered
