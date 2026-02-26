import os
import sys

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from dotenv import load_dotenv
from workflow.orchestrator_workflow import Workflow

def test_free_text_query():
    """
    Test the run_free_text_query function of the orchestrator workflow.
    """
    load_dotenv()
    
    db_name = 'withyou.db'
    project_endpoint = os.environ.get("PROJECT_ENDPOINT")
    model_deployment_name = os.environ.get("MODEL_DEPLOYMENT_NAME", "gpt-4.1")
    
    if not project_endpoint:
        print("ERROR: PROJECT_ENDPOINT environment variable is not set.")
        print("Please set it in your .env file or as an environment variable.")
        return
    
    print(f"Using PROJECT_ENDPOINT: {project_endpoint}")
    print(f"Using MODEL_DEPLOYMENT_NAME: {model_deployment_name}")
    print("=" * 50)
    
    # Initialize the workflow
    workflow = Workflow(db_name, project_endpoint, model_deployment_name)
    
    user_id = 1  # Example user ID
    
    # Test queries for orientation intent
    test_queries = [
        "What day is it today?",
        "Where am I?",
        "Is anyone visiting today?",
        "What time is it?",
        "Who is my daughter?",  
    ]
    
    for query in test_queries:
        print(f"\nUser Query: '{query}'")
        print("-" * 30)
        
        try:
            response = workflow.run_free_text_query(user_id, query)
            print(f"Response: {response['message']}")
        except Exception as e:
            print(f"Error: {e}")
        
        print("-" * 30)


if __name__ == '__main__':
    test_free_text_query()
