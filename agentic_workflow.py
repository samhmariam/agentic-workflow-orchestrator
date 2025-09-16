
import os
from dotenv import load_dotenv
from workflow_agents.base_agents import ActionPlanningAgent, KnowledgeAugmentedPromptAgent, EvaluationAgent, RoutingAgent

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("Error: OPENAI_API_KEY not found in environment variables. Please create a .env file with your OpenAI API key: OPENAI_API_KEY=your_api_key_here")

# load the product spec
with open("Product-Spec-Email-Router.txt", "r") as file:
    product_spec = file.read()

# Instantiate all the agents

# Action Planning Agent
knowledge_action_planning = (
    "Stories are defined from a product spec by identifying a "
    "persona, an action, and a desired outcome for each story. "
    "Each story represents a specific functionality of the product "
    "described in the specification. \n"
    "Features are defined by grouping related user stories. \n"
    "Tasks are defined for each story and represent the engineering "
    "work required to develop the product. \n"
    "A development Plan for a product contains all these components"
)
action_planning_agent = ActionPlanningAgent(openai_api_key, knowledge_action_planning)

# Product Manager - Knowledge Augmented Prompt Agent
persona_product_manager = "You are a Product Manager, you are responsible for defining the user stories for a product."
knowledge_product_manager = (
    "Stories are defined by writing sentences with a persona, an action, and a desired outcome. "
    "The sentences always start with: As a "
    "Write several stories for the product spec below, where the personas are the different users of the product. "
    f"Product Spec: {product_spec}"
)
product_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key, persona_product_manager, knowledge_product_manager)

# Product Manager - Evaluation Agent
persona_product_manager_eval = "You are an evaluation agent that checks the answers of other worker agents."
evaluation_criteria_product_manager = (
    "The answer should be user stories that follow the following structure: \n"
    "As a [type of user], I want [an action or feature] so that [benefit/value]."
)
product_manager_evaluation_agent = EvaluationAgent(
    openai_api_key,
    persona_product_manager_eval,
    evaluation_criteria_product_manager,
    product_manager_knowledge_agent,
    max_interactions=3
)


# Program Manager - Knowledge Augmented Prompt Agent
persona_program_manager = "You are a Program Manager, you are responsible for defining the features for a product."
knowledge_program_manager = "Features of a product are defined by organizing similar user stories into cohesive groups."
program_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key, persona_program_manager, knowledge_program_manager)

# Program Manager - Evaluation Agent
persona_program_manager_eval = "You are an evaluation agent that checks the answers of other worker agents."
program_manager_evaluation_agent = EvaluationAgent(
    openai_api_key,
    persona_program_manager_eval,
    evaluation_criteria =(
        "The answer should be product features that follow the following structure: \n"
        "Feature Name: A clear, concise title that identifies the capability\n"
        "Description: A brief explanation of what the feature does and its purpose\n"
        "Key Functionality: The specific capabilities or actions the feature provides\n"
        "User Benefit: How this feature creates value for the user"
    ),
    worker_agent=program_manager_knowledge_agent,
    max_interactions=3
)

# Development Engineer - Knowledge Augmented Prompt Agent
persona_dev_engineer = "You are a Development Engineer, you are responsible for defining the development tasks for a product."
knowledge_dev_engineer = "Development tasks are defined by identifying what needs to be built to implement each user story."
# Instantiate a development_engineer_knowledge_agent using 'persona_dev_engineer' and 'knowledge_dev_engineer'
development_engineer_knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key, persona_dev_engineer, knowledge_dev_engineer)

# Development Engineer - Evaluation Agent
persona_dev_engineer_eval = "You are an evaluation agent that checks the answers of other worker agents."
development_engineer_evaluation_agent = EvaluationAgent(
    openai_api_key,
    persona_dev_engineer_eval,
    evaluation_criteria =(
        "The answer should be tasks following this exact structure: \n"
        "Task ID: A unique identifier for tracking purposes\n"
        "Task Title: Brief description of the specific development work\n"
        "Related User Story: Reference to the parent user story\n"
        "Description: Detailed explanation of the technical work required\n"
        "Acceptance Criteria: Specific requirements that must be met for completion\n"
        "Estimated Effort: Time or complexity estimation\n"
        "Dependencies: Any tasks that must be completed first"
    ),
    worker_agent=development_engineer_knowledge_agent,
    max_interactions=3
)


def product_manager_support_function(query):
    response = product_manager_knowledge_agent.respond(query)
    evaluation = product_manager_evaluation_agent.evaluate(response)
    return evaluation['final_response'] 
def program_manager_support_function(query):
    response = program_manager_knowledge_agent.respond(query)
    evaluation = program_manager_evaluation_agent.evaluate(response)
    return evaluation['final_response']
def development_engineer_support_function(query):
    response = development_engineer_knowledge_agent.respond(query)
    evaluation = development_engineer_evaluation_agent.evaluate(response)
    return evaluation['final_response']                 
   

routes = [
    {
        'name': 'Product Manager',
        'description': 'Responsible for defining product personas and user stories only. Does not define features or tasks. Does not group stories.',
        'func': product_manager_support_function
    },
    {
        'name': 'Program Manager',
        'description': 'Responsible for defining product features and requirements. Does not define user stories or tasks.',
        'func': program_manager_support_function
    },
    {
        'name': 'Development Engineer',
        'description': 'Responsible for defining development tasks and technical requirements. Does not define user stories or features.',
        'func': development_engineer_support_function
    }
]

# Routing Agent
routing_agent = RoutingAgent(openai_api_key, routes)

# Job function persona support functions
# TODO: 11 - Define the support functions for the routes of the routing agent (e.g., product_manager_support_function, program_manager_support_function, development_engineer_support_function).
# Each support function should:
#   1. Take the input query (e.g., a step from the action plan).
#   2. Get a response from the respective Knowledge Augmented Prompt Agent.
#   3. Have the response evaluated by the corresponding Evaluation Agent.
#   4. Return the final validated response.


def run_workflow(workflow_prompt="What would the development tasks for this product be?"):
    """
    Run the agentic workflow with the given prompt.
    
    Args:
        workflow_prompt (str): The main task to complete in the workflow
        
    Returns:
        list: List of completed steps and their results
    """
    print("\n*** Workflow execution started ***\n")
    print(f"Task to complete in this workflow, workflow prompt = {workflow_prompt}")

    print("\nDefining workflow steps from the workflow prompt")
    workflow_steps = action_planning_agent.extract_steps_from_prompt(workflow_prompt)
    completed_steps = []
    
    for step in workflow_steps:
        # Route the step to the appropriate support function
        agent = routing_agent.route(step)
        result = agent(step)
        completed_steps.append(result)
        print(f"Executed step: {step}, Result: {result}")
    
    print("\n*** Workflow execution completed ***\n")
    print(f"Final output of the workflow: {completed_steps[-1] if completed_steps else 'No steps executed.'}\n")
    
    return completed_steps


if __name__ == "__main__":
    # Run the workflow when the module is executed directly
    default_prompt = "What would the development tasks for this product be?"
    run_workflow(default_prompt)

