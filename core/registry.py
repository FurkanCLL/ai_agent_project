from typing import Dict, List
from tools.base import BaseTool


class ToolRegistry:
    """
    A registry class that manages all available tools.
    This implements the Registry/Factory pattern to decouple the agent
    from specific tool implementations.
    """

    def __init__(self):
        # Dictionary to store tools: { 'tool_name': ToolInstance }
        self._tools: Dict[str, BaseTool] = {}

    def register_tool(self, tool: BaseTool):
        """Adds a new tool to the registry."""
        self._tools[tool.name] = tool

    def get_all_declarations(self) -> List[dict]:
        """Returns a list of all tool schemas for Gemini function calling."""
        return [tool.get_declaration() for tool in self._tools.values()]

    def execute_tool(self, tool_name: str, **kwargs):
        """Finds and runs a tool by its name."""
        tool = self._tools.get(tool_name)
        if not tool:
            return f"Error: Tool '{tool_name}' not found in registry."

        # Calling the execute method of the specific tool strategy
        return tool.execute(**kwargs)

    @property
    def tool_names(self) -> List[str]:
        """Returns a list of registered tool names."""
        return list(self._tools.keys())