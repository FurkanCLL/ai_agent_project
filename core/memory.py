from google.genai import types

class MemoryManager:
    """
    Manages the conversation history using strict Google GenAI types.
    """
    def __init__(self):
        # We store history as a list of types.Content objects
        self.history = []

    def add_user_message(self, message: str):
        """Adds a user message as a formal Content object."""
        content = types.Content(
            role="user",
            parts=[types.Part.from_text(text=message)]
        )
        self.history.append(content)

    def add_model_message(self, message: str):
        """Adds a model response as a formal Content object."""
        content = types.Content(
            role="model",
            parts=[types.Part.from_text(text=message)]
        )
        self.history.append(content)

    def get_history(self):
        return self.history

    def clear(self):
        self.history = []