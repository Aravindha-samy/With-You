import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition

class AuroraAgent:
    """
    Aurora is the central orchestration intelligence for the With You cognitive support system.
    Its mission is to interpret user intent, assess emotional state, and route requests
    to the appropriate domain agent.
    """

    def __init__(self, project_endpoint, model_deployment_name):
        load_dotenv()
        self.project_client = AIProjectClient(
            endpoint=project_endpoint,
            credential=DefaultAzureCredential(),
        )
        self.openai_client = self.project_client.get_openai_client()
        self.model_deployment_name = model_deployment_name
        self.agent_name = "aurora-intent-classifier"
        self._create_agent_if_not_exists()

    def _create_agent_if_not_exists(self):
        """
        Creates the Foundry agent for intent classification if it doesn't already exist.
        """
        try:
            # Check if agent exists by trying to get it
            self.project_client.agents.get(self.agent_name)
            print(f"Agent '{self.agent_name}' already exists.")
        except Exception:
            # If not, create it
            print(f"Creating agent '{self.agent_name}'.")
            instructions = "You are a helpful assistant that classifies the user's intent. The possible intents are: orientation, identity, emotional, story, caregiver, unknown. Respond with only the intent."
            agent = self.project_client.agents.create_version(
                agent_name=self.agent_name,
                definition=PromptAgentDefinition(
                    model=self.model_deployment_name,
                    instructions=instructions,
                ),
            )
            print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")


    def classify_intent(self, query):
        """
        Classifies the user's intent based on their query using a Foundry agent.
        """
        
        response = self.openai_client.responses.create(
            extra_body={"agent_reference": {"name": self.agent_name, "type": "agent_reference"}},
            input=query,
        )
        print response
        # The response from the model will be the classified intent.
        # You might need to parse the output_text to get the intent.
        # For this example, we assume the model returns just the intent string.
        intent = response.output_text.strip().lower()
        
        if intent in ["orientation", "identity", "emotional", "story", "caregiver"]:
            return intent
        else:
            return "unknown"
