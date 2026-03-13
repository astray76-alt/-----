from domains.designer.skills.design_plan_skill import DesignPlanSkill
from domains.designer.skills.image_prompt_skill import ImagePromptSkill
from domains.designer.skills.image_generation_skill import ImageGenerationSkill


class DesignerService:
    """
    디자이너 에이전트 서비스 클래스
    - DesignPlanSkill → ImagePromptSkill → ImageGenerationSkill 순으로 실행
    """

    def __init__(self):
        self._design_plan = DesignPlanSkill()
        self._image_prompt = ImagePromptSkill()
        self._image_generation = ImageGenerationSkill()

    def design_slide(self, slide_title: str, slide_body: str) -> dict:
        """
        슬라이드 디자인 기획부터 이미지 생성까지 전체 실행

        Args:
            slide_title: 슬라이드 제목
            slide_body: 슬라이드 본문

        Returns:
            디자인 결과 딕셔너리 (design_plan, imagen_prompt, image_path)
        """
        # 1단계: Gemini 2.5 Pro로 디자인 방향 기획
        design_plan = self._design_plan.execute(slide_title, slide_body)

        # 2단계: Gemini 2.5 Pro로 Imagen 프롬프트 생성
        imagen_prompt = self._image_prompt.execute(slide_title, design_plan)

        # 3단계: Imagen 3으로 이미지 생성
        image_path = self._image_generation.execute(slide_title, imagen_prompt)

        return {
            "design_plan": design_plan,
            "imagen_prompt": imagen_prompt,
            "image_path": image_path,
        }
