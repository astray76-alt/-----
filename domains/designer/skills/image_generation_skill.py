import os
import google.generativeai as genai
from shared.config import Config


class ImageGenerationSkill:
    """Imagen 3으로 실제 이미지 파일 생성 스킬"""

    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self._model = genai.ImageGenerationModel(Config.IMAGEN_MODEL)
        os.makedirs(Config.IMAGE_OUTPUT_DIR, exist_ok=True)

    def execute(self, slide_title: str, imagen_prompt: str) -> str:
        """
        이미지 생성 후 파일로 저장

        Args:
            slide_title: 파일명에 사용할 슬라이드 제목
            imagen_prompt: ImagePromptSkill이 생성한 프롬프트

        Returns:
            저장된 이미지 파일 경로
        """
        result = self._model.generate_images(
            prompt=imagen_prompt,
            number_of_images=1,
            aspect_ratio="16:9",
        )

        safe_title = slide_title.replace(" ", "_").replace("/", "-")
        image_path = os.path.join(Config.IMAGE_OUTPUT_DIR, f"{safe_title}.png")
        result.images[0].save(image_path)

        return image_path
