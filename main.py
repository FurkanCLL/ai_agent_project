import os
import sys
from dotenv import load_dotenv

# Importing our core components
from core.agent import GeminiAgent
from core.registry import ToolRegistry
from core.memory import MemoryManager

# Importing our tools
from tools.simple_tools import CalculatorTool, ClockTool
from tools.custom_tools import FileReadTool, SystemInfoTool


def main():
    # Load the API Key from .env
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("Error: Please set GEMINI_API_KEY in your .env file.")
        sys.exit(1)

    # Setup the Tool Registry and register all tools
    # This follows the Factory/Registry pattern
    registry = ToolRegistry()
    registry.register_tool(CalculatorTool())
    registry.register_tool(ClockTool())
    registry.register_tool(FileReadTool())
    registry.register_tool(SystemInfoTool())

    # Initialize the Agent
    # We use the successful model we tested before
    agent = GeminiAgent(
        api_key=api_key,
        registry=registry,
        model_name="gemini-2.0-flash-lite"
    )

    print("--- Digital Assistant is Online ---")
    print("Type 'quit' or 'exit' to end the session.\n")

    # Main CLI Chat Loop
    while True:
        try:
            user_input = input("You: ").strip()

            if user_input.lower() in ['quit', 'exit']:
                print("Goodbye!")
                break

            if not user_input:
                continue

            # Run the agent (Reason -> Act -> Observe loop happens inside)
            response = agent.run(user_input)

            print(f"\nAssistant: {response}\n")

        except KeyboardInterrupt:
            print("\nSession ended by user.")
            break
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")


if __name__ == "__main__":
    main()