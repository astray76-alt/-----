class SummarizeSkill:
    """검색 결과 텍스트 요약 스킬"""

    def execute(self, results: list[dict]) -> str:
        """
        필터링된 검색 결과를 GPT에 넘길 텍스트로 변환

        Args:
            results: FilterSkill 반환값

        Returns:
            불릿 형태의 요약 텍스트
        """
        lines = [
            f"- {item['title']}: {item['description']}"
            for item in results
        ]
        return "\n".join(lines)
