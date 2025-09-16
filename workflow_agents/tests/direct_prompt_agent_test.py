import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add the project root directory to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from workflow_agents.base_agents import DirectPromptAgent

"""
Test script for DirectPromptAgent functionality.
This script demonstrates how to use the DirectPromptAgent class to interact with OpenAI's API.
"""


def main():
    """
    Main function to test the DirectPromptAgent functionality.
    """
    print("=== DirectPromptAgent Test Script ===\n")
    
    # Step 1: Load the API Key using dotenv
    print("1. Loading OpenAI API key from environment file...")
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    if not openai_api_key:
        print("Error: OPENAI_API_KEY not found in environment variables.")
        print("Please create a .env file with your OpenAI API key:")
        print("OPENAI_API_KEY=your_api_key_here")
        return
    
    print("✓ API key loaded successfully\n")
    
    # Step 2: Instantiate the Agent
    print("2. Creating DirectPromptAgent instance...")
    direct_agent = DirectPromptAgent(openai_api_key)
    print("✓ DirectPromptAgent instance created successfully\n")
    
    # Step 3: Prompt the Agent
    print("3. Sending prompt to the agent...")
    prompt = "What is the Capital of France?"
    print(f"Prompt: {prompt}")
    
    try:
        response = direct_agent.respond(prompt)
        print(f"Response: {response}\n")
    except Exception as e:
        print(f"Error getting response from agent: {e}")
        return
    
    # Step 4: Explain Knowledge Source
    print("4. Knowledge Source Explanation:")
    print("=" * 50)
    print("The DirectPromptAgent uses general knowledge from the OpenAI GPT-4.1-mini")
    print("language model to respond to prompts. This knowledge comes from the model's training data.")
    print("The agent does not access external databases or perform real-time lookups;")
    print("it relies entirely on the pre-trained knowledge embedded in the LLM.")
    print("=" * 50)


if __name__ == "__main__":
    main()
