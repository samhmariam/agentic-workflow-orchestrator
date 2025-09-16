import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add the project root directory to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import after path modification
from workflow_agents.base_agents import KnowledgeAugmentedPromptAgent, RoutingAgent

"""
Test script for RoutingAgent functionality.
This script demonstrates how to use the RoutingAgent class to route prompts to specialized 
KnowledgeAugmentedPromptAgent instances based on semantic similarity.
"""


def main():
    """
    Main function to test the RoutingAgent with specialized knowledge agents.
    """
    # Load environment variables from .env file if it exists
    load_dotenv()
    
    # Get OpenAI API key from environment variable
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    if not openai_api_key:
        print("Error: OPENAI_API_KEY environment variable not found.")
        print("Please set your OpenAI API key as an environment variable or in a .env file.")
        return

    # Texas-specific knowledge for the Texas agent
    texas_knowledge = """
    Texas is the second-largest state in the United States by both area and population.
    The capital of Texas is Austin, and the largest city is Houston.
    Texas was an independent republic from 1836 to 1845 before joining the United States.
    Rome, Texas is a small unincorporated community in Delta County, Texas.
    Rome, Texas was established in the 1840s and named after Rome, Italy.
    The community of Rome, Texas was primarily agricultural and never grew very large.
    Texas is known for its oil industry, cattle ranching, and distinctive culture.
    The Alamo is a historic site in San Antonio, Texas, where a famous battle occurred in 1836.
    """

    # Europe-specific knowledge for the Europe agent
    europe_knowledge = """
    Europe is a continent comprising the westernmost peninsulas of Eurasia.
    Rome is the capital city of Italy and was the center of the Roman Empire.
    Rome, Italy was founded according to legend by Romulus and Remus in 753 BC.
    Ancient Rome was one of the most powerful civilizations in history.
    The Roman Empire at its peak controlled much of Europe, North Africa, and the Middle East.
    The Colosseum in Rome is one of the most famous landmarks in the world.
    Vatican City, an independent city-state, is located within Rome.
    Rome is known as the "Eternal City" and has a history spanning over 2,500 years.
    The Renaissance had significant influence in Rome with great artists and architects.
    """

    # Math-specific knowledge for the Math agent
    math_knowledge = """
    Mathematics involves the study of numbers, quantities, shapes, and patterns.
    Basic arithmetic operations include addition, subtraction, multiplication, and division.
    When calculating time for multiple stories or tasks, multiply the time per unit by the number of units.
    If one story takes 2 days and there are 20 stories, the total time is 2 × 20 = 40 days.
    Word problems often require identifying the relevant numbers and operations needed.
    Time calculations can involve days, hours, minutes, or other time units.
    Multiplication is repeated addition: 2 + 2 + 2 + ... (20 times) = 2 × 20 = 40.
    Problem-solving in mathematics requires understanding what is being asked.
    """

    print("=== Setting up specialized knowledge agents ===")
    
    # Instantiate Texas agent
    texas_agent = KnowledgeAugmentedPromptAgent(
        openai_api_key=openai_api_key,
        persona="a knowledgeable expert on Texas history and geography",
        knowledge=texas_knowledge
    )
    print("✓ Texas agent created")

    # Instantiate Europe agent
    europe_agent = KnowledgeAugmentedPromptAgent(
        openai_api_key=openai_api_key,
        persona="a knowledgeable expert on European history and geography",
        knowledge=europe_knowledge
    )
    print("✓ Europe agent created")

    # Instantiate Math agent
    math_agent = KnowledgeAugmentedPromptAgent(
        openai_api_key=openai_api_key,
        persona="a helpful mathematics tutor and problem solver",
        knowledge=math_knowledge
    )
    print("✓ Math agent created")

    # Define agent functions/lambdas for the routing agent
    def texas_function(prompt):
        """Function to handle Texas-related queries."""
        return texas_agent.respond(prompt)

    def europe_function(prompt):
        """Function to handle Europe-related queries."""
        return europe_agent.respond(prompt)

    def math_function(prompt):
        """Function to handle math-related queries."""
        return math_agent.respond(prompt)

    print("✓ Agent functions defined")

    # Create the agents list for the RoutingAgent
    agents = [
        {
            "name": "Texas Expert",
            "description": "Expert on Texas history, geography, cities, and places in Texas including Rome, Texas",
            "func": texas_function
        },
        {
            "name": "Europe Expert", 
            "description": "Expert on European history, geography, cities, and places in Europe including Rome, Italy",
            "func": europe_function
        },
        {
            "name": "Math Expert",
            "description": "Expert on mathematics, calculations, word problems, and numerical computations",
            "func": math_function
        }
    ]

    # Instantiate the RoutingAgent
    routing_agent = RoutingAgent(
        openai_api_key=openai_api_key,
        agents=agents
    )
    print("✓ RoutingAgent created and configured")

    # Test prompts
    test_prompts = [
        "Tell me about the history of Rome, Texas",
        "Tell me about the history of Rome, Italy", 
        "One story takes 2 days, and there are 20 stories"
    ]

    print("\n=== Testing RoutingAgent with various prompts ===")
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n--- Test {i} ---")
        print(f"Prompt: {prompt}")
        print("-" * 50)
        
        try:
            response = routing_agent.route_prompt(prompt)
            print(f"Response: {response}")
        except Exception as e:
            print(f"Error: {e}")
        
        print("-" * 50)


if __name__ == "__main__":
    main()
