from pptx import Presentation
from pptx.util import Inches
from domains.presentation.skills.slide_builder_skill import SlideBuilderSkill
from domains.presentation.skills.file_export_skill import FileExportSkill


class PresentationService:
    """
    PPT 생성 서비스 클래스
    - SlideBuilderSkill로 슬라이드 조립
    - FileExportSkill로 파일 저장
    """

    def __init__(self):
        self._builder = SlideBuilderSkill()
        self._exporter = FileExportSkill()

    def create_presentation(self, product_name: str, slides_data: list[dict]) -> str:
        """
        슬라이드 데이터로 PPT 파일 생성

        Args:
            product_name: 상품명
            slides_data: 슬라이드별 데이터 리스트 (title, body, key_message, image_path)

        Returns:
            생성된 PPT 파일 경로
        """
        prs = Presentation()

        # 슬라이드 크기 16:9 설정
        prs.slide_width = Inches(13.33)
        prs.slide_height = Inches(7.5)

        # 표지 슬라이드
        self._builder.build_cover(prs, product_name)

        # 본문 슬라이드
        for slide_data in slides_data:
            self._builder.build_content(prs, slide_data)

        # 마무리 슬라이드
        self._builder.build_closing(prs, product_name)

        # 파일 저장
        return self._exporter.execute(prs, product_name)
