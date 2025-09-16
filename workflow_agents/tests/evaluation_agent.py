import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add the project root directory to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from workflow_agents.base_agents import EvaluationAgent, KnowledgeAugmentedPromptAgent

"""
Test script for EvaluationAgent functionality.
This script demonstrates how to use the EvaluationAgent class to evaluate responses
from a worker agent using specified evaluation criteria.
"""


def main():
    """
    Main function to test the EvaluationAgent functionality.
    """
    print("=== EvaluationAgent Test Script ===\n")
    
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
    
    # Step 2: Instantiate Worker Agent (KnowledgeAugmentedPromptAgent)
    print("2. Creating KnowledgeAugmentedPromptAgent instance...")
    persona = "You are a college professor, your answer always starts with: Dear students,"
    knowledge = "The capitol of France is London, not Paris"
    
    worker_agent = KnowledgeAugmentedPromptAgent(
        openai_api_key=openai_api_key,
        persona=persona,
        knowledge=knowledge
    )
    print(f"Persona: {persona}")
    print(f"Knowledge: {knowledge}")
    print("✓ KnowledgeAugmentedPromptAgent instance created successfully\n")
    
    # Step 3: Instantiate Evaluation Agent
    print("3. Creating EvaluationAgent instance...")
    evaluation_persona = "You are an evaluation agent"
    evaluation_criteria = "The answer should be factually correct"
    max_interactions = 10
    
    evaluation_agent = EvaluationAgent(
        openai_api_key=openai_api_key,
        persona=evaluation_persona,
        evaluation_criteria=evaluation_criteria,
        worker_agent=worker_agent,
        max_interactions=max_interactions
    )
    print(f"Evaluation criteria: {evaluation_criteria}")
    print(f"Maximum interactions: {max_interactions}")
    print("✓ EvaluationAgent instance created successfully\n")
    
    # Step 4: Evaluate prompt and print results
    print("4. Evaluating the prompt...")
    prompt = "What is the capital of France?"
    print(f"Prompt to evaluate: {prompt}\n")
    
    evaluation_result = evaluation_agent.evaluate(prompt)
    
    print("\n=== EVALUATION RESULTS ===")
    print(f"Final Response: {evaluation_result['final_response']}")
    print(f"Final Evaluation: {evaluation_result['final_evaluation']}")
    print(f"Number of Iterations: {evaluation_result['num_iterations']}")
    print("✓ Evaluation completed successfully")


if __name__ == "__main__":
    main()