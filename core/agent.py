from google import genai
from google.genai import types
from .registry import ToolRegistry
from .memory import MemoryManager
from utils.logger import AgentObserver


class GeminiAgent:
    def __init__(self, api_key: str, registry: ToolRegistry, model_name: str = "gemini-2.5-flash-lite"):
        self.client = genai.Client(api_key=api_key)
        self.registry = registry
        self.memory = MemoryManager()
        self.model_name = model_name
        self._observers = []  # List to hold our observers

    def add_observer(self, observer: AgentObserver):
        """Attaches a new observer to the agent."""
        self._observers.append(observer)

    def _notify_observers(self, event_type: str, data: str):
        """Sends updates to all attached observers."""
        for observer in self._observers:
            observer.update(event_type, data)

    def run(self, user_input: str):
        # Save user input to memory
        self.memory.add_user_message(user_input)

        # Loop to allow multiple reasoning steps
        max_iterations = 5
        for i in range(max_iterations):
            # 2. Get available tools
            all_tools = self.registry.get_all_declarations()
            tools_config = [types.Tool(function_declarations=all_tools)]

            # Ask Gemini what to do
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=self.memory.get_history(),
                config=types.GenerateContentConfig(
                    tools=tools_config,
                    system_instruction="You are a helpful assistant. Use tools if necessary. Always explain the result of the tools to the user."
                )
            )

            candidate_content = response.candidates[0].content
            parts = candidate_content.parts if candidate_content.parts else []

            # Check if model wants to use any tools
            tool_calls = [part.function_call for part in parts if part.function_call]

            # If no tools are needed, return the final text
            if not tool_calls:
                parts_text = "".join([p.text for p in parts if p.text])
                final_text = parts_text if parts_text else "I executed the tool but have no further comments."

                self.memory.add_model_message(final_text)
                return final_text

            # Record model's tool call decision into history
            self.memory.history.append(candidate_content)

            # Execute the requested tools
            for tool_call in tool_calls:
                # Notify observers that a tool is starting
                self._notify_observers("tool_start", f"Calling {tool_call.name}")

                # Ensure args is a dictionary to prevent iteration errors
                safe_args = tool_call.args if isinstance(tool_call.args, dict) else {}

                observation = self.registry.execute_tool(
                    tool_name=tool_call.name,
                    **safe_args
                )

                # Send the tool result back as if the user provided it
                tool_response_content = types.Content(
                    role="user",
                    parts=[
                        types.Part(
                            function_response=types.FunctionResponse(
                                name=tool_call.name,
                                response={"result": str(observation)}
                            )
                        )
                    ]
                )
                self.memory.history.append(tool_response_content)

                # Notify observers that the tool finished
                self._notify_observers("tool_end", f"Received result from {tool_call.name}")

        return "Thinking limit reached."