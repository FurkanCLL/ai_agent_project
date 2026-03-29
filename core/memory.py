class MemoryManager:
    """
    Manages the conversation history for the AI agent.
    """
    def __init__(self):
        # We store history as a list of dictionaries for Gemini
        self.history = []

    def add_user_message(self, message: str):
        """Adds a message from the user to the memory."""
        self.history.append({"role": "user", "parts": [message]})

    def add_model_message(self, message: str):
        """Adds a message from the AI model to the memory."""
        self.history.append({"role": "model", "parts": [message]})

    def get_history(self):
        """Returns the full conversation history."""
        return self.history

    def clear(self):
        """Clears the memory for a new session."""
        self.history = []