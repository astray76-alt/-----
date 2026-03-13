import json
import os
import requests
from pypdf import PdfReader


class InputHandler:
    """
    실행 입력값 처리 클래스
    - input.json 파일이 있으면 파일에서 로드
    - 없으면 대화형 입력으로 fallback
    - 레퍼런스 파일(txt, pdf) 및 URL 텍스트 추출 지원
    """

    _INPUT_FILE = "input.json"

    def load(self) -> dict:
        """
        input.json 존재 여부에 따라 파일 또는 대화형으로 입력값 로드

        Returns:
            입력값 딕셔너리 (product_name, outline, content_direction, reference_texts)
        """
        if os.path.exists(self._INPUT_FILE):
            print(f"[입력] {self._INPUT_FILE} 파일을 불러옵니다.")
            raw = self._load_from_file()
        else:
            print("[입력] input.json 없음 → 대화형 입력 모드로 시작합니다.")
            raw = self._load_interactive()

        # 레퍼런스 파일/URL을 텍스트로 변환
        reference_texts = self._load_references(raw.get("references", []))

        return {
            "product_name": raw["product_name"],
            "outline": raw.get("outline", []),
            "content_direction": raw.get("content_direction", ""),
            "reference_texts": reference_texts,
        }

    def _load_from_file(self) -> dict:
        """input.json 파일에서 입력값 로드"""
        with open(self._INPUT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not data.get("product_name"):
            raise ValueError("input.json에 product_name이 없습니다.")

        return data

    def _load_interactive(self) -> dict:
        """대화형 입력 모드"""
        print("\n" + "="*50)
        print("  상품소개서 자동화 에이전트 - 입력 설정")
        print("="*50)

        # 상품명 (필수)
        product_name = ""
        while not product_name:
            product_name = input("\n상품명을 입력하세요: ").strip()

        # 목차 직접 지정 여부
        outline = []
        use_outline = input("\n목차를 직접 지정하시겠습니까? (Y/N, 기본 N): ").strip().upper()
        if use_outline == "Y":
            print("슬라이드 제목을 한 줄씩 입력하세요. 빈 줄 입력 시 완료.")
            while True:
                title = input(f"  {len(outline)+1}번 슬라이드: ").strip()
                if not title:
                    break
                outline.append(title)

        # 콘텐츠 방향 지정
        content_direction = input(
            "\n콘텐츠 작성 방향을 입력하세요 (없으면 Enter): "
        ).strip()

        # 레퍼런스 입력
        references = []
        use_ref = input("\n레퍼런스를 추가하시겠습니까? (Y/N, 기본 N): ").strip().upper()
        if use_ref == "Y":
            print("파일 경로 또는 URL을 한 줄씩 입력하세요. 빈 줄 입력 시 완료.")
            while True:
                ref = input("  레퍼런스: ").strip()
                if not ref:
                    break
                references.append(ref)

        return {
            "product_name": product_name,
            "outline": outline,
            "content_direction": content_direction,
            "references": references,
        }

    def _load_references(self, references: list[str]) -> str:
        """
        레퍼런스 목록에서 텍스트 추출 (txt, pdf, URL 지원)

        Args:
            references: 파일 경로 또는 URL 리스트

        Returns:
            추출된 전체 텍스트 (구분선으로 합침)
        """
        if not references:
            return ""

        texts = []
        for ref in references:
            try:
                if ref.startswith("http://") or ref.startswith("https://"):
                    # URL: 웹 페이지 텍스트 추출
                    text = self._extract_from_url(ref)
                elif ref.endswith(".pdf"):
                    # PDF 파일 텍스트 추출
                    text = self._extract_from_pdf(ref)
                elif ref.endswith(".txt"):
                    # 텍스트 파일 직접 읽기
                    text = self._extract_from_txt(ref)
                else:
                    print(f"[경고] 지원하지 않는 레퍼런스 형식입니다: {ref}")
                    continue

                texts.append(f"[레퍼런스: {ref}]\n{text}")
                print(f"  ✅ 레퍼런스 로드: {ref}")

            except Exception as e:
                print(f"  ⚠️ 레퍼런스 로드 실패 ({ref}): {e}")

        return "\n\n".join(texts)

    def _extract_from_url(self, url: str) -> str:
        """URL에서 텍스트 추출 (HTML 태그 제거)"""
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # 간단한 HTML 태그 제거
        import re
        text = re.sub(r"<[^>]+>", " ", response.text)
        text = re.sub(r"\s+", " ", text).strip()

        # 너무 긴 경우 앞 3000자만 사용
        return text[:3000]

    def _extract_from_pdf(self, path: str) -> str:
        """PDF 파일에서 텍스트 추출"""
        reader = PdfReader(path)
        pages_text = [page.extract_text() for page in reader.pages if page.extract_text()]
        return "\n".join(pages_text)

    def _extract_from_txt(self, path: str) -> str:
        """텍스트 파일 읽기"""
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
