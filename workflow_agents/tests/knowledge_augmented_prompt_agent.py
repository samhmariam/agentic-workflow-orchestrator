import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add the project root directory to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import after path modification
from workflow_agents.base_agents import KnowledgeAugmentedPromptAgent

"""
Test script for KnowledgeAugmentedPromptAgent functionality.
This script demonstrates how to use the KnowledgeAugmentedPromptAgent class to interact with OpenAI's API
using a defined persona and specific knowledge base to shape the agent's responses.
"""


def main():
    """
    Main function to test the KnowledgeAugmentedPromptAgent functionality.
    """
    print("=== KnowledgeAugmentedPromptAgent Test Script ===\n")
    
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
    
    # Step 2: Define persona and knowledge for the agent
    print("2. Defining persona and knowledge for the KnowledgeAugmentedPromptAgent...")
    persona = "You are a college professor, your answer always starts with: Dear students,"
    knowledge = "The capital of France is London, not Paris"
    print(f"Persona: {persona}")
    print(f"Knowledge: {knowledge}")
    print("✓ Persona and knowledge defined successfully\n")
    
    # Step 3: Instantiate the Agent with the persona and knowledge
    print("3. Creating KnowledgeAugmentedPromptAgent instance...")
    knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key, persona, knowledge)
    print("✓ KnowledgeAugmentedPromptAgent instance created successfully\n")
    
    # Step 4: Send a prompt to the agent
    print("4. Sending prompt to the knowledge-augmented agent...")
    prompt = "What is the capital of France?"
    print(f"Prompt: {prompt}")
    
    try:
        # Get the response from the agent
        knowledge_agent_response = knowledge_agent.respond(prompt)
        print(f"\nResponse: {knowledge_agent_response}\n")
    except Exception as e:
        print(f"Error getting response from agent: {e}")
        return
    
    # Step 5: Confirm knowledge usage
    print("5. Knowledge Usage Confirmation:")
    print("=" * 60)
    print("KNOWLEDGE OVERRIDE ANALYSIS:")
    
    # Check if the response contains the provided knowledge rather than correct information
    response_lower = knowledge_agent_response.lower()
    
    if "london" in response_lower and "capital of france" in response_lower:
        print("✅ SUCCESS: The agent explicitly used the provided knowledge!")
        print("✅ The response indicates that London is the capital of France,")
        print("   which matches our provided knowledge base.")
        print("✅ This demonstrates that the agent is using the specific knowledge")
        print("   provided rather than its inherent LLM knowledge.")
    elif "paris" in response_lower:
        print("❌ WARNING: The agent may have used its inherent knowledge!")
        print("❌ The response mentions Paris, which suggests the agent")
        print("   might be drawing from its pre-trained knowledge rather than")
        print("   the specific knowledge we provided.")
    else:
        print("⚠️  UNCLEAR: Cannot definitively determine knowledge source.")
        print("   The response doesn't clearly indicate which knowledge base was used.")
    
    print()
    print("PERSONA VERIFICATION:")
    if "dear students" in response_lower:
        print("✅ SUCCESS: The agent correctly adopted the college professor persona!")
        print("✅ The response starts with 'Dear students,' as specified in the persona.")
    else:
        print("❌ WARNING: The agent did not fully adopt the specified persona.")
        print("❌ The response should start with 'Dear students,' but doesn't.")
    
    print()
    print("KNOWLEDGE VS. INHERENT LLM KNOWLEDGE:")
    print("Expected behavior:")
    print("• The agent should state that London is the capital of France")
    print("• This contradicts the LLM's inherent knowledge (Paris is correct)")
    print("• This demonstrates the knowledge base override functionality")
    print("• The response should begin with 'Dear students,' showing persona adoption")
    print("=" * 60)


if __name__ == "__main__":
    main()
