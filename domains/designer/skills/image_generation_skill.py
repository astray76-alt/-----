import os
import base64
from google import genai
from google.genai import types
from shared.config import Config


class ImageGenerationSkill:
    """Gemini 2.0 Flash로 이미지 파일 생성 스킬 (Google AI Studio 호환)"""

    def __init__(self):
        self._client = genai.Client(api_key=Config.GEMINI_API_KEY)
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
        response = self._client.models.generate_content(
            model=Config.IMAGEN_MODEL,
            contents=imagen_prompt,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
            ),
        )

        # 응답에서 이미지 데이터 추출 후 저장
        safe_title = slide_title.replace(" ", "_").replace("/", "-")
        image_path = os.path.join(Config.IMAGE_OUTPUT_DIR, f"{safe_title}.png")

        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                image_bytes = base64.b64decode(part.inline_data.data)
                with open(image_path, "wb") as f:
                    f.write(image_bytes)
                break

        return image_path
