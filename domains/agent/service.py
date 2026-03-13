from shared.config import Config
from domains.research.service import ResearchService
from domains.content.service import ContentService
from domains.designer.service import DesignerService
from domains.presentation.service import PresentationService


class AgentService:
    """
    상품소개서 자동화 오케스트레이터 클래스
    - 전체 파이프라인을 순서대로 실행
    - Research → Content → Designer → Presentation
    """

    def __init__(self):
        # 환경변수 검증
        Config.validate()

        # 각 도메인 서비스 초기화
        self._research = ResearchService()
        self._content = ContentService()
        self._designer = DesignerService()
        self._presentation = PresentationService()

    def run(self, product_name: str) -> str:
        """
        상품명을 입력받아 상품소개서 PPT를 자동 생성

        Args:
            product_name: 소개서를 만들 상품명

        Returns:
            생성된 PPT 파일 경로
        """
        print(f"\n[에이전트 시작] 상품: {product_name}")

        # 1단계: Brave Search로 상품 정보 수집
        print("\n[1/4] 리서치 중... (Brave Search)")
        research_results = self._research.research_product(product_name)

        # 2단계: GPT-5.4로 슬라이드 콘텐츠 생성
        print("\n[2/4] 콘텐츠 생성 중... (GPT-5.4)")
        slides_content = self._content.generate_all_slides(research_results)

        # 3단계: Gemini 2.5 Pro + Imagen 3으로 슬라이드 이미지 생성
        print("\n[3/4] 디자인 및 이미지 생성 중... (Gemini 2.5 Pro + Imagen 3)")
        slides_data = []
        for slide in slides_content:
            design_result = self._designer.design_slide(
                slide_title=slide["title"],
                slide_content=slide["body"],
            )
            # 콘텐츠와 디자인 결과 병합
            slides_data.append({
                "title": slide["title"],
                "body": slide["body"],
                "key_message": slide["key_message"],
                "image_path": design_result["image_path"],
            })

        # 4단계: python-pptx로 PPT 파일 조립
        print("\n[4/4] PPT 생성 중... (python-pptx)")
        output_path = self._presentation.create_presentation(
            product_name=product_name,
            slides_data=slides_data,
        )

        print(f"\n[완료] 파일 저장 경로: {output_path}")
        return output_path
