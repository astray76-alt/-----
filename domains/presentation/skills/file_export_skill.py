import os
from pptx.presentation import Presentation
from shared.config import Config


class FileExportSkill:
    """PPT 파일 저장 스킬"""

    def __init__(self):
        os.makedirs(Config.OUTPUT_DIR, exist_ok=True)

    def execute(self, prs: Presentation, product_name: str) -> str:
        """
        Presentation 객체를 pptx 파일로 저장

        Args:
            prs: python-pptx Presentation 객체
            product_name: 파일명에 사용할 상품명

        Returns:
            저장된 파일 경로
        """
        safe_name = product_name.replace(" ", "_")
        output_path = os.path.join(Config.OUTPUT_DIR, f"{safe_name}_상품소개서.pptx")
        prs.save(output_path)
        return output_path
