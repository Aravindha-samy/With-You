import os
from dotenv import load_dotenv
from agents.harbor import HarborAgent

def main():
    """
    Main function to demonstrate the Harbor agent.
    """
    load_dotenv()
    
    db_name = 'withyou.db'
    project_endpoint = os.environ.get("PROJECT_ENDPOINT")
    model_deployment_name = os.environ.get("MODEL_DEPLOYMENT_NAME", "gpt-4.1")
    
    harbor = HarborAgent(project_endpoint, model_deployment_name, db_name)

    # Simulate a user asking a question
    user_id = 1 # Example user ID
    query = "What day is it?"
    
    response = harbor.answer(user_id, query)
    print(f"User Query: '{query}'")
    print(f"Harbor's Response: {response['message']}")
    print("-" * 20)

    query = "Where am I?"
    response = harbor.answer(user_id, query)
    print(f"User Query: '{query}'")
    print(f"Harbor's Response: {response['message']}")
    print("-" * 20)

    query = "What is happening today?"
    response = harbor.answer(user_id, query)
    print(f"User Query: '{query}'")
    print(f"Harbor's Response: {response['message']}")
    print("-" * 20)


if __name__ == '__main__':
    main()
