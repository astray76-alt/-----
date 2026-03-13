import os
import google.generativeai as genai
from shared.config import Config


class DesignerService:
    """
    디자이너 에이전트 서비스 클래스
    - Gemini 2.5 Pro: 슬라이드 디자인 방향 기획 및 이미지 프롬프트 생성
    - Imagen 3: 실제 이미지 파일 생성
    """

    def __init__(self):
        # Google AI SDK 초기화
        genai.configure(api_key=Config.GEMINI_API_KEY)

        # Gemini 2.5 Pro 모델 초기화 (디자인 기획용)
        self._gemini = genai.GenerativeModel(Config.GEMINI_MODEL)

        # Imagen 3 모델 초기화 (이미지 생성용)
        self._imagen = genai.ImageGenerationModel(Config.IMAGEN_MODEL)

        # 이미지 저장 경로 생성
        os.makedirs(Config.IMAGE_OUTPUT_DIR, exist_ok=True)

    def plan_slide_design(self, slide_title: str, slide_content: str) -> dict:
        """
        Gemini 2.5 Pro를 사용해 슬라이드 디자인 방향 기획 및 이미지 프롬프트 생성

        Args:
            slide_title: 슬라이드 제목
            slide_content: 슬라이드 내용 요약

        Returns:
            디자인 계획 딕셔너리 (레이아웃, 색상, 이미지 프롬프트 포함)
        """
        prompt = f"""
당신은 B2B 상품소개서 디자인 전문가입니다.
아래 슬라이드 내용을 분석하여 디자인 계획을 수립하고, Imagen으로 생성할 이미지 프롬프트를 영어로 작성해주세요.

슬라이드 제목: {slide_title}
슬라이드 내용: {slide_content}

다음 형식으로 응답해주세요:
- 레이아웃: (슬라이드 레이아웃 방향)
- 색상 테마: (주요 색상 및 분위기)
- 이미지 역할: (이미지가 슬라이드에서 하는 역할)
- Imagen 프롬프트: (영어로 작성된 이미지 생성 프롬프트, 구체적이고 상세하게)
"""
        # Gemini 2.5 Pro로 디자인 기획 생성
        response = self._gemini.generate_content(prompt)
        raw_text = response.text

        # 응답에서 Imagen 프롬프트 추출
        imagen_prompt = self._extract_imagen_prompt(raw_text)

        return {
            "slide_title": slide_title,
            "design_plan": raw_text,
            "imagen_prompt": imagen_prompt,
        }

    def generate_slide_image(self, slide_title: str, imagen_prompt: str) -> str:
        """
        Imagen 3를 사용해 슬라이드용 이미지 생성 및 저장

        Args:
            slide_title: 파일명에 사용할 슬라이드 제목
            imagen_prompt: Gemini가 생성한 이미지 프롬프트

        Returns:
            저장된 이미지 파일 경로
        """
        # Imagen 3으로 이미지 생성
        result = self._imagen.generate_images(
            prompt=imagen_prompt,
            number_of_images=1,
            aspect_ratio="16:9",  # 슬라이드 비율
        )

        # 이미지 파일 저장
        safe_title = slide_title.replace(" ", "_").replace("/", "-")
        image_path = os.path.join(Config.IMAGE_OUTPUT_DIR, f"{safe_title}.png")
        result.images[0].save(image_path)

        return image_path

    def design_slide(self, slide_title: str, slide_content: str) -> dict:
        """
        디자인 기획부터 이미지 생성까지 전체 파이프라인 실행

        Args:
            slide_title: 슬라이드 제목
            slide_content: 슬라이드 내용 요약

        Returns:
            디자인 결과 딕셔너리 (디자인 계획 + 생성된 이미지 경로)
        """
        # 1단계: Gemini 2.5 Pro로 디자인 기획 및 프롬프트 생성
        design_plan = self.plan_slide_design(slide_title, slide_content)

        # 2단계: Imagen 3으로 실제 이미지 생성
        image_path = self.generate_slide_image(
            slide_title=slide_title,
            imagen_prompt=design_plan["imagen_prompt"],
        )

        return {
            "slide_title": slide_title,
            "design_plan": design_plan["design_plan"],
            "imagen_prompt": design_plan["imagen_prompt"],
            "image_path": image_path,
        }

    def _extract_imagen_prompt(self, gemini_response: str) -> str:
        """
        Gemini 응답에서 'Imagen 프롬프트:' 이후 텍스트 추출

        Args:
            gemini_response: Gemini 2.5 Pro의 전체 응답 텍스트

        Returns:
            추출된 이미지 프롬프트 문자열
        """
        # 'Imagen 프롬프트:' 키워드 이후 내용 파싱
        keyword = "Imagen 프롬프트:"
        if keyword in gemini_response:
            return gemini_response.split(keyword)[-1].strip()

        # 키워드가 없으면 전체 응답을 프롬프트로 사용
        return gemini_response.strip()
