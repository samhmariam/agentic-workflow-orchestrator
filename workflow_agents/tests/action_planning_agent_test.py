import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add the project root directory to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from workflow_agents.base_agents import ActionPlanningAgent

"""
Test script for ActionPlanningAgent functionality.
This script tests the agent's ability to extract action steps from a prompt.
"""


def main():
    """
    Test the ActionPlanningAgent with the specified prompt about scrambled eggs.
    """
    print("=== ActionPlanningAgent Test Script ===\n")
    
    # Step 1: Import Libraries and Class (completed above)
    print("1. Libraries and ActionPlanningAgent class imported successfully\n")
    
    # Step 2: Load API Key
    print("2. Loading OpenAI API key from environment...")
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    if not openai_api_key:
        print("Error: OPENAI_API_KEY not found in environment variables.")
        print("Please create a .env file with your OpenAI API key:")
        print("OPENAI_API_KEY=your_api_key_here")
        return
    
    print("✓ API key loaded successfully\n")
    
    # Step 3: Instantiate the Agent
    print("3. Creating ActionPlanningAgent instance...")
    
    # Define knowledge for cooking-related actions
    knowledge = """
    Available cooking actions:
    - Gather ingredients
    - Prepare cooking equipment
    - Heat the pan
    - Crack eggs
    - Scramble eggs
    - Season the eggs
    - Serve the dish
    - Clean up
    """
    
    planning_agent = ActionPlanningAgent(openai_api_key, knowledge)
    print("✓ ActionPlanningAgent instance created successfully\n")
    
    # Step 4: Verify Functionality
    print("4. Testing agent with the specified prompt...\n")
    
    test_prompt = "One morning I wanted to have scrambled eggs"
    print(f"Test prompt: \"{test_prompt}\"")
    print("-" * 50)
    
    try:
        # Extract steps using the agent
        extracted_steps = planning_agent.extract_steps_from_prompt(test_prompt)
        
        print("Extracted action steps:")
        for i, step in enumerate(extracted_steps, 1):
            print(f"  {i}. {step}")
        
        print(f"\nTotal steps extracted: {len(extracted_steps)}")
        
    except Exception as e:
        print(f"Error during step extraction: {str(e)}")
    
    print("\n=== Test Completed ===")


if __name__ == "__main__":
    main()
