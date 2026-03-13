import sys
from domains.agent.service import AgentService


class Main:
    """프로그램 진입점 클래스"""

    @classmethod
    def run(cls) -> None:
        """상품명을 인자로 받아 에이전트 실행"""
        if len(sys.argv) < 2:
            print("사용법: python main.py <상품명>")
            print("예시:  python main.py 'Slack'")
            sys.exit(1)

        product_name = sys.argv[1]
        agent = AgentService()
        agent.run(product_name)


if __name__ == "__main__":
    Main.run()
