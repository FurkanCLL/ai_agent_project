from google import genai
from google.genai import types
from .registry import ToolRegistry
from .memory import MemoryManager


class GeminiAgent:
    def __init__(self, api_key: str, registry: ToolRegistry, model_name: str = "gemini-2.5-flash-lite"):
        self.client = genai.Client(api_key=api_key)
        self.registry = registry
        self.memory = MemoryManager()
        self.model_name = model_name

    def run(self, user_input: str):
        self.memory.add_user_message(user_input)

        max_iterations = 5
        for i in range(max_iterations):
            all_tools = self.registry.get_all_declarations()
            tools_config = [types.Tool(function_declarations=all_tools)]

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

            tool_calls = [part.function_call for part in parts if part.function_call]

            if not tool_calls:
                # FIX: Safer way to extract text from the model's response parts
                parts_text = "".join([p.text for p in parts if p.text])
                final_text = parts_text if parts_text else "I executed the tool but have no further comments."

                self.memory.add_model_message(final_text)
                return final_text

            self.memory.history.append(candidate_content)

            for tool_call in tool_calls:
                print(f"  [System] Executing: {tool_call.name}")

                safe_args = tool_call.args if isinstance(tool_call.args, dict) else {}

                observation = self.registry.execute_tool(
                    tool_name=tool_call.name,
                    **safe_args
                )

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

        return "Thinking limit reached."