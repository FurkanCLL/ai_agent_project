from .base import BaseTool
from datetime import datetime


class CalculatorTool(BaseTool):
    """
    A simple tool that performs basic arithmetic operations.
    """

    @property
    def name(self) -> str:
        return "calculator"

    @property
    def description(self) -> str:
        # We tell Gemini exactly when to use this tool
        return "Perform a mathematical calculation (addition, subtraction, multiplication, division)."

    def execute(self, expression: str, **kwargs):
        """
        Calculates the result of a math expression string.
        """
        try:
            # Note: eval() is used here for simplicity in a student project,
            # but in real production apps, we should use a safer math parser.
            result = eval(expression)
            return f"The result of {expression} is {result}"
        except Exception as e:
            return f"Error calculating {expression}: {str(e)}"

    def get_parameters_schema(self):
        """
        Returns the JSON schema that tells the LLM what arguments this tool needs.
        """
        return {
            "type": "OBJECT",
            "properties": {
                "expression": {
                    "type": "STRING",
                    "description": "The math expression to evaluate, e.g., '2 + 2' or '15 * (3+2)'"
                }
            },
            "required": ["expression"]
        }

class ClockTool(BaseTool):
    """
    A simple tool to get the current date and time.
    """
    @property
    def name(self) -> str:
        return "get_time"

    @property
    def description(self) -> str:
        return "Returns the current date and time. Use this when the user asks for the time."

    def execute(self, **kwargs):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"The current date and time is {now}"

    def get_parameters_schema(self):
        # This tool doesn't need any input parameters
        return {
            "type": "OBJECT",
            "properties": {}
        }