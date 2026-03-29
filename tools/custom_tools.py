import os
import platform
from .base import BaseTool


class FileReadTool(BaseTool):
    """
    A custom tool to read the content of a local text file.
    """

    @property
    def name(self) -> str:
        return "read_file"

    @property
    def description(self) -> str:
        return "Read the content of a local text file. Useful for analyzing documents."

    def execute(self, file_path: str, **kwargs):
        """Reads a file and returns its content or an error."""
        if not os.path.exists(file_path):
            return f"Error: The file at {file_path} does not exist."

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # We return only the first 500 characters to avoid huge tokens
                return content[:500] + ("..." if len(content) > 500 else "")
        except Exception as e:
            return f"Error reading file: {str(e)}"

    def get_parameters_schema(self):
        return {
            "type": "OBJECT",
            "properties": {
                "file_path": {
                    "type": "STRING",
                    "description": "The path to the file to be read, e.g., 'notes.txt'"
                }
            },
            "required": ["file_path"]
        }

class SystemInfoTool(BaseTool):
    """
    A custom tool to retrieve basic information about the host system.
    """
    @property
    def name(self) -> str:
        return "get_system_info"

    @property
    def description(self) -> str:
        return "Returns basic system information like OS, processor, and architecture."

    def execute(self, **kwargs):
        info = {
            "OS": platform.system(),
            "Release": platform.release(),
            "Architecture": platform.machine(),
            "Processor": platform.processor()
        }
        return f"System Information: {info}"

    def get_parameters_schema(self):
        return {
            "type": "OBJECT",
            "properties": {}
        }