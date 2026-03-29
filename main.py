import os
import sys
from dotenv import load_dotenv

from core.agent import GeminiAgent
from core.registry import ToolRegistry
from tools.simple_tools import CalculatorTool, ClockTool
from tools.custom_tools import FileReadTool, SystemInfoTool


def main():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("Error: Please set GEMINI_API_KEY in your .env file.")
        sys.exit(1)

    registry = ToolRegistry()
    registry.register_tool(CalculatorTool())
    registry.register_tool(ClockTool())
    registry.register_tool(FileReadTool())
    registry.register_tool(SystemInfoTool())

    agent = GeminiAgent(
        api_key=api_key,
        registry=registry,
        model_name="gemini-2.5-flash-lite"
    )

    print("\n--- Digital Assistant is Online ---")
    print("Type 'quit' or 'exit' to end the session.\n")

    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() in ['quit', 'exit']:
                print("Goodbye!")
                break
            if not user_input:
                continue

            response = agent.run(user_input)
            print(f"\nAssistant: {response}\n")

        except Exception as e:
            print(f"\nAn error occurred: {e}")


if __name__ == "__main__":
    main()