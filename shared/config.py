import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()


class Config:
    """프로젝트 전역 설정 관리 클래스"""

    # OpenAI API 설정
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-5.4")

    # Brave Search 설정
    BRAVE_API_KEY: str = os.getenv("BRAVE_API_KEY", "")
    BRAVE_SEARCH_COUNT: int = int(os.getenv("BRAVE_SEARCH_COUNT", "10"))

    # Google Gemini / Imagen 설정
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.5-pro")
    IMAGEN_MODEL: str = os.getenv("IMAGEN_MODEL", "imagen-3.0-generate-001")

    # 출력 경로 설정
    OUTPUT_DIR: str = os.getenv("OUTPUT_DIR", "output")
    IMAGE_OUTPUT_DIR: str = os.getenv("IMAGE_OUTPUT_DIR", "output/images")

    @classmethod
    def validate(cls) -> None:
        """필수 환경변수 검증"""
        missing = []

        if not cls.OPENAI_API_KEY:
            missing.append("OPENAI_API_KEY")
        if not cls.BRAVE_API_KEY:
            missing.append("BRAVE_API_KEY")
        if not cls.GEMINI_API_KEY:
            missing.append("GEMINI_API_KEY")

        if missing:
            raise EnvironmentError(
                f"필수 환경변수가 설정되지 않았습니다: {', '.join(missing)}\n"
                f".env.example을 참고하여 .env 파일을 생성해주세요."
            )
