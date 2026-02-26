import os
import json
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from tools import harbor_tools

class HarborAgent:
    """
    Harbor is the orientation and grounding agent.
    Its purpose is to provide calm, repetitive-safe answers about:
    - Date
    - Time
    - Location
    - Upcoming events
    - Daily structure
    Its goal is to reduce panic through familiarity.
    This agent is powered by Microsoft Foundry and uses tools to get its information.
    """

    AGENT_NAME = "harbor-orientation-agent"
    
    SYSTEM_PROMPT = """You are Harbor, a calm and reassuring orientation agent.
Your purpose is to help users who may be feeling disoriented by providing grounding information.

You have access to the following tools:
- get_current_date: Returns the current date.
- get_current_time: Returns the current time.
- get_user_location: Retrieves the user's location. Requires user_id.
- get_todays_events: Retrieves today's events for the user. Requires user_id.

When a user asks a question, determine which tool to use and call it.
Always respond in a warm, gentle, and reassuring tone.
Keep sentences short and simple.
Never say "You forgot" or "As I told you before".
"""

    # Tool definitions for the Foundry agent
    TOOL_DEFINITIONS = [
        {
            "type": "function",
            "function": {
                "name": "get_current_date",
                "description": "Returns the current date, formatted nicely.",
                "parameters": {"type": "object", "properties": {}, "required": []}
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_current_time",
                "description": "Returns the current time, formatted nicely.",
                "parameters": {"type": "object", "properties": {}, "required": []}
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_user_location",
                "description": "Retrieves the user's current location from the database.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "integer", "description": "The ID of the user."}
                    },
                    "required": ["user_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_todays_events",
                "description": "Retrieves today's scheduled events for the user from the database.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "integer", "description": "The ID of the user."}
                    },
                    "required": ["user_id"]
                }
            }
        }
    ]

    def __init__(self, project_endpoint, model_deployment_name, db_name='withyou.db'):
        load_dotenv()
        self.db_name = db_name
        self.model_deployment_name = model_deployment_name
        
        self.project_client = AIProjectClient(
            endpoint=project_endpoint,
            credential=DefaultAzureCredential(),
        )
        self.openai_client = self.project_client.get_openai_client()
        
        # Map tool names to their implementations
        self.tool_implementations = {
            "get_current_date": harbor_tools.get_current_date,
            "get_current_time": harbor_tools.get_current_time,
            "get_user_location": lambda user_id: harbor_tools.get_user_location(user_id, self.db_name),
            "get_todays_events": lambda user_id: harbor_tools.get_todays_events(user_id, self.db_name),
        }

    def _execute_tool(self, tool_name, arguments):
        """Executes a tool and returns the result."""
        if tool_name in self.tool_implementations:
            func = self.tool_implementations[tool_name]
            return func(**arguments)
        return f"Unknown tool: {tool_name}"

    def answer(self, user_id, query):
        """
        Answers an orientation-related query using AI-powered tool selection.
        """
        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {"role": "user", "content": f"User ID is {user_id}. The user asks: {query}"}
        ]

        # First call: Let the model decide which tool to use
        response = self.openai_client.chat.completions.create(
            model=self.model_deployment_name,
            messages=messages,
            tools=self.TOOL_DEFINITIONS,
            tool_choice="auto"
        )

        assistant_message = response.choices[0].message

        # Check if the model wants to call a tool
        if assistant_message.tool_calls:
            # Process tool calls
            tool_results = []
            for tool_call in assistant_message.tool_calls:
                tool_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)
                
                # Execute the tool
                result = self._execute_tool(tool_name, arguments)
                tool_results.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "content": str(result)
                })

            # Add the assistant's message and tool results to the conversation
            messages.append(assistant_message)
            messages.extend(tool_results)

            # Second call: Let the model generate a final response based on tool results
            final_response = self.openai_client.chat.completions.create(
                model=self.model_deployment_name,
                messages=messages,
            )
            response_message = final_response.choices[0].message.content
        else:
            # No tool call, use the direct response
            response_message = assistant_message.content

        return {
            "message": response_message,
            "reassurance_level": "low",
            "followup_suggestion": "none"
        }
