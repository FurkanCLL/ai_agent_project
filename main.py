from core.registry import ToolRegistry
from tools.simple_tools import CalculatorTool
from tools.custom_tools import FileReadTool


def test_system_components():
    print("--- Starting Component Tests ---")

    # 1. Initialize Registry
    registry = ToolRegistry()

    # 2. Register our tools
    registry.register_tool(CalculatorTool())
    registry.register_tool(FileReadTool())

    print(f"Registered tools: {registry.tool_names}")

    # 3. Test Calculator
    print("\nTesting Calculator...")
    calc_result = registry.execute_tool("calculator", expression="15 * 4 + 10")
    print(f"Result: {calc_result}")

    # 4. Test File Reader (Let's create a dummy file first)
    print("\nTesting File Reader...")
    with open("test_note.txt", "w") as f:
        f.write("This is a secret note for the AI agent.")

    file_result = registry.execute_tool("read_file", file_path="test_note.txt")
    print(f"File content: {file_result}")

    # 5. Check JSON Declarations (What Gemini will see)
    print("\nChecking tool schemas for Gemini:")
    schemas = registry.get_all_declarations()
    for schema in schemas:
        print(f"- Tool: {schema['name']} is ready.")


if __name__ == "__main__":
    test_system_components()