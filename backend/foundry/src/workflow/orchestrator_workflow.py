from agents.harbor import HarborAgent
from agents.aurora import AuroraAgent

class Workflow:
    def __init__(self, db_name, project_endpoint, model_deployment_name):
        self.harbor = HarborAgent(project_endpoint, model_deployment_name, db_name)
        self.aurora = AuroraAgent(project_endpoint, model_deployment_name)

    def run_structured_query(self, user_id, button_identifier):
        """
        Runs a structured query from a button press.
        """
        # For a structured query, Aurora's logic is simple.
        # It identifies the target agent based on the button.
        if button_identifier == "where_am_i":
            agent_to_call = self.harbor
            query = "where am I"
        else:
            # In a real scenario, you'd have a mapping of buttons to agents.
            return {"message": "I'm not sure what that button does."}

        # The orchestrator calls the appropriate agent.
        response = agent_to_call.answer(user_id, query)
        return response

    def run_free_text_query(self, user_id, query):
        """
        Runs a free text query from the user.
        """
        # Aurora analyzes the query to determine the intent.
        intent = self.aurora.classify_intent(query)

        # Based on the intent, the orchestrator calls the appropriate agent.
        if intent == "orientation":
            response = self.harbor.answer(user_id, query)
            
        else:
            response = {"message": "I'm not sure how to help with that yet."}
        
        return response
