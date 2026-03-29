from abc import ABC, abstractmethod

class AgentObserver(ABC):
    """
    Abstract base class for the Observer pattern.
    Any logger or monitor should inherit from this.
    """
    @abstractmethod
    def update(self, event_type: str, data: str):
        pass

class ConsoleLogger(AgentObserver):
    """
    A simple observer that prints agent actions to the console.
    """
    def update(self, event_type: str, data: str):
        # We print logs clearly to track agent's hidden actions
        print(f"  [LOG | {event_type.upper()}] -> {data}")