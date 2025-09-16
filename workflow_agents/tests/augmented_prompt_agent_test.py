import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add the project root directory to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import after path modification
from workflow_agents.base_agents import AugmentedPromptAgent

"""
Test script for AugmentedPromptAgent functionality.
This script demonstrates how to use the AugmentedPromptAgent class to interact with OpenAI's API
using a defined persona to shape the agent's responses.
"""


def main():
    """
    Main function to test the AugmentedPromptAgent functionality.
    """
    print("=== AugmentedPromptAgent Test Script ===\n")
    
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
    
    # Step 2: Define a persona for the agent
    print("2. Defining persona for the AugmentedPromptAgent...")
    persona = "a knowledgeable medieval historian specializing in European castle architecture and feudal society"
    print(f"Persona: {persona}")
    print("✓ Persona defined successfully\n")
    
    # Step 3: Instantiate the Agent with the persona
    print("3. Creating AugmentedPromptAgent instance...")
    augmented_agent = AugmentedPromptAgent(openai_api_key, persona)
    print("✓ AugmentedPromptAgent instance created successfully\n")
    
    # Step 4: Send a prompt to the agent
    print("4. Sending prompt to the augmented agent...")
    prompt = "What are the key defensive features of a typical medieval castle?"
    print(f"Prompt: {prompt}")
    
    try:
        # Store the response in the required variable name
        augmented_agent_response = augmented_agent.respond(prompt)
        print(f"\nResponse: {augmented_agent_response}\n")
    except Exception as e:
        print(f"Error getting response from agent: {e}")
        return
    
    # Step 5: Print and explain the response characteristics
    print("5. Response Analysis and Explanations:")
    print("=" * 60)
    print("KNOWLEDGE TYPE ANALYSIS:")
    print("The agent likely used the following types of knowledge:")
    print("• Historical architectural knowledge about medieval fortifications")
    print("• General knowledge about defensive structures and their purposes from medieval times")
    print("• Knowledge of materials and construction techniques of the era")
    print()
    print("PERSONA IMPACT ANALYSIS:")
    print("How the specified persona affected the final output:")
    print("• Response style: The agent adopted an authoritative, scholarly tone")
    print("  appropriate for a medieval historian")
    print("• Technical depth: The response included specialized terminology")
    print("  and detailed architectural concepts")
    print("• Historical context: The agent provided context about the historical")
    print("  development and purpose of defensive features")
    print("• Expertise focus: The response emphasized European castle architecture")
    print("  as specified in the persona")
    print("• Educational approach: The agent structured the response in an")
    print("  informative, academic manner typical of a historian")
    print()
    print("COMPARISON TO DIRECT PROMPT:")
    print("Without the persona, a generic response might have been:")
    print("• Less specialized vocabulary")
    print("• More general defensive concepts")
    print("• Less historical context and expert insight")
    print("• More basic explanations without scholarly depth")
    print("=" * 60)


if __name__ == "__main__":
    main()
