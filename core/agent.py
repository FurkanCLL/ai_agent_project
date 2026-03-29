from google import genai
from google.genai import types
from .registry import ToolRegistry
from .memory import MemoryManager


class GeminiAgent:
    """
    The core Agent class that implements the ReAct loop.
    It reasons using Gemini and acts using the ToolRegistry.
    """

    def __init__(self, api_key: str, registry: ToolRegistry, model_name: str = "gemini-2.0-flash-lite"):
        self.client = genai.Client(api_key=api_key)
        self.registry = registry
        self.memory = MemoryManager()
        self.model_name = model_name

    def run(self, user_input: str):
        """
        Main entry point for a chat turn. Implements the Reason -> Act -> Observe loop.
        """
        # 1. Remember what the user said
        self.memory.add_user_message(user_input)

        # Allow the agent to loop a few times if it needs multiple tools
        max_iterations = 5

        for i in range(max_iterations):
            # Prepare the tools declaration for Gemini
            tools_list = self.registry.get_all_declarations()

            # 2. REASON: Ask Gemini what to do next
            # Pass the entire conversation history
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=self.memory.get_history(),
                config=types.GenerateContentConfig(
                    tools=tools_list,
                    system_instruction="You are a helpful assistant. Use tools when needed."
                )
            )

            # Get the first candidate's response
            response_content = response.candidates[0].content

            # Check if Gemini wants to call a tool (Function Calling)
            tool_calls = [part.func_call for part in response_content.parts if part.func_call]

            if not tool_calls:
                # No tool calls? Then Gemini has a final answer for us.
                final_text = response.text
                self.memory.add_model_message(final_text)
                return final_text

            # 3. ACT: Gemini decided to use one or more tools
            # Must handle each tool call and collect results
            for tool_call in tool_calls:
                print(f"  [Agent is thinking...] Calling tool: {tool_call.name}")

                # Execute the tool via our Registry
                observation = self.registry.execute_tool(
                    tool_name=tool_call.name,
                    **tool_call.args
                )

                # 4. OBSERVE: We add the tool result back to memory
                # In Gemini API, tool results must be sent back as a 'function_response'
                self.memory.history.append({
                    "role": "user",  # Technically 'tool' role, but we follow the SDK's history format
                    "parts": [
                        types.Part.from_function_response(
                            name=tool_call.name,
                            response={"result": observation}
                        )
                    ]
                })

            # After adding tool results to memory, the loop continues
            # to let Gemini 'Reason' about the results and give a final answer.

        return "I'm sorry, I reached my maximum reasoning steps without a final answer."