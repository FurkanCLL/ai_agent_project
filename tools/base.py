from abc import ABC, abstractmethod


# This is our Abstract Base Class for all tools.
# Every tool we create must follow this template.
class BaseTool(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        """The name of the tool (e.g., 'get_weather')"""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Description of what the tool does for Gemini to understand"""
        pass

    @abstractmethod
    def execute(self, **kwargs):
        """The main logic of the tool will be here"""
        pass

    def get_declaration(self):
        """Returns the JSON schema for Gemini's function calling"""
        # We will implement this part to tell Gemini how to use this tool
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.get_parameters_schema()
        }

    @abstractmethod
    def get_parameters_schema(self):
        """Each tool will define its own parameters here"""
        pass