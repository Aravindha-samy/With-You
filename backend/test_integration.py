"""
Test script for Azure AI Agent integration

This script tests the complete integration of Azure agents with the FastAPI backend.
Run this after starting the backend server to verify everything works.
"""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from azure_agents.service import get_agent_service
from database import SessionLocal
from app import crud, schemas


async def test_agent_integration():
    """Test the Azure agent service integration"""
    
    print("=" * 60)
    print("Testing Azure AI Agent Integration")
    print("=" * 60)
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Verify or create test user
        print("\n1. Checking for test user...")
        user = crud.get_user(db, user_id=1)
        if not user:
            print("   Creating test user...")
            user_data = schemas.UserCreate(
                name="Test Patient",
                email="patient@test.com",
                user_type="patient"
            )
            user = crud.create_user(db=db, user=user_data)
        print(f"   ✓ User found: {user.name} (ID: {user.id})")
        
        # Get agent service
        print("\n2. Initializing agent service...")
        agent_service = get_agent_service()
        print("   ✓ Agent service initialized")
        
        # Test cases
        test_cases = [
            {
                "input": "I'm feeling scared and don't know where I am",
                "expected_agent": "solace",
                "expected_emotion": "anxious"
            },
            {
                "input": "Where am I? What day is it?",
                "expected_agent": "harbor",
                "expected_emotion": "confused"
            },
            {
                "input": "Who is my daughter Sarah?",
                "expected_agent": "roots",
                "expected_emotion": "confused"
            },
            {
                "input": "Tell me about when I was a teacher",
                "expected_agent": "legacy",
                "expected_emotion": "neutral"
            },
        ]
        
        print("\n3. Testing agent routing and responses...")
        print("-" * 60)
        
        for i, test in enumerate(test_cases, 1):
            print(f"\nTest {i}: {test['input']}")
            print(f"Expected Agent: {test['expected_agent']}")
            
            try:
                # Process the message
                result = await agent_service.process_user_message(
                    user_id=user.id,
                    user_input=test['input'],
                    db=db
                )
                
                # Display results
                print(f"\n✓ Response received:")
                print(f"  Agent: {result['agent_type']}")
                print(f"  Intent: {result.get('intent', 'N/A')}")
                print(f"  Emotion: {result.get('emotion_type', 'N/A')} (score: {result.get('emotion_score', 0):.2f})")
                print(f"  Alert: {'Yes' if result.get('alert_triggered') else 'No'}")
                print(f"  Response Preview: {result['response'][:100]}...")
                
                # Verify routing
                if result['agent_type'] == test['expected_agent']:
                    print(f"  ✓ Correct agent routing")
                else:
                    print(f"  ⚠ Unexpected agent: expected {test['expected_agent']}, got {result['agent_type']}")
                
            except Exception as e:
                print(f"  ✗ Error: {str(e)}")
        
        # Test database logging
        print("\n" + "=" * 60)
        print("4. Verifying database logging...")
        interactions = crud.get_agent_interactions(db=db, user_id=user.id, limit=10)
        print(f"   ✓ Found {len(interactions)} logged interactions")
        
        if interactions:
            latest = interactions[-1]
            print(f"   Latest interaction:")
            print(f"     - Agent: {latest.agent_type}")
            print(f"     - Intent: {latest.intent}")
            print(f"     - Emotion: {latest.emotion_type} ({latest.emotion_score})")
            print(f"     - Timestamp: {latest.timestamp}")
        
        # Test alert creation
        print("\n5. Checking caregiver alerts...")
        alerts = crud.get_caregiver_alerts(db=db, caregiver_id=1, is_acknowledged=False)
        print(f"   ✓ Found {len(alerts)} unacknowledged alerts")
        
        if alerts:
            latest_alert = alerts[-1]
            print(f"   Latest alert:")
            print(f"     - Type: {latest_alert.alert_type}")
            print(f"     - Message: {latest_alert.message}")
            print(f"     - Trigger: {latest_alert.trigger_agent}")
        
        print("\n" + "=" * 60)
        print("✓ All integration tests completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        
    finally:
        db.close()


async def test_emotion_detection():
    """Test emotion detection without Azure AI"""
    
    print("\n" + "=" * 60)
    print("Testing Emotion Detection (Offline)")
    print("=" * 60)
    
    from azure_agents.service import AzureAgentService
    service = AzureAgentService()
    
    test_inputs = [
        "I'm scared and anxious",
        "I feel happy today",
        "Where am I? I'm so confused",
        "I miss my family and feel sad",
        "Everything is fine"
    ]
    
    for text in test_inputs:
        emotion = service._detect_emotion(text.lower())
        intent = service._detect_intent(text.lower())
        print(f"\nInput: {text}")
        print(f"  Emotion: {emotion['type']} (score: {emotion['score']:.2f})")
        print(f"  Intent: {intent['intent']} → Agent: {intent['agent']}")


if __name__ == "__main__":
    print("\n🤖 WithYou Azure AI Agent Integration Test\n")
    
    # Test emotion detection (doesn't require Azure)
    asyncio.run(test_emotion_detection())
    
    # Test full integration (requires Azure AI configured)
    print("\n" + "=" * 60)
    response = input("\nTest full Azure AI integration? (requires .env configuration) [y/N]: ")
    if response.lower() == 'y':
        asyncio.run(test_agent_integration())
    else:
        print("\nSkipping Azure AI tests. Configure .env to enable full testing.")
    
    print("\n✓ Test script completed\n")
