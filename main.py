from shared.input_handler import InputHandler
from domains.agent.service import AgentService


class Main:
    """프로그램 진입점 클래스"""

    @classmethod
    def run(cls) -> None:
        """입력값 로드 후 에이전트 실행"""
        # 입력값 로드 (input.json 또는 대화형)
        handler = InputHandler()
        inputs = handler.load()

        # 에이전트 실행
        agent = AgentService()
        agent.run(
            product_name=inputs["product_name"],
            outline=inputs["outline"],
            content_direction=inputs["content_direction"],
            reference_texts=inputs["reference_texts"],
        )


if __name__ == "__main__":
    Main.run()
