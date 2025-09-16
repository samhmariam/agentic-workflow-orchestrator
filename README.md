# Agentic Workflow Orchestrator

An AI-powered workflow orchestration system that automates product development planning through intelligent agent collaboration. This system breaks down complex product requirements into actionable development plans using specialized AI agents for different roles in the product development lifecycle.

## Overview

The Agentic Workflow Orchestrator demonstrates how multiple AI agents can work together to transform a product specification into a comprehensive development plan. The system uses a routing mechanism to delegate tasks to specialized agents that simulate different roles in a product team.

## Features

- **Multi-Agent Architecture**: Specialized agents for Product Manager, Program Manager, and Development Engineer roles
- **Intelligent Routing**: Automatically routes tasks to the most appropriate agent based on task characteristics
- **Evaluation System**: Built-in quality assurance through evaluation agents that validate outputs
- **Action Planning**: Breaks down complex workflows into manageable steps
- **Knowledge Augmentation**: Agents use domain-specific knowledge to improve response quality

## Architecture

### Core Agents

1. **Action Planning Agent**: Extracts workflow steps from high-level prompts
2. **Routing Agent**: Determines which specialized agent should handle each task
3. **Product Manager Agent**: Defines user stories and personas
4. **Program Manager Agent**: Organizes stories into product features
5. **Development Engineer Agent**: Creates technical tasks and implementation plans
6. **Evaluation Agents**: Validate outputs from worker agents

### Workflow Process

1. Input a high-level workflow prompt (e.g., "What would the development tasks for this product be?")
2. Action Planning Agent breaks down the prompt into specific steps
3. Each step is routed to the appropriate specialized agent
4. Worker agents generate responses using domain knowledge
5. Evaluation agents validate and refine responses
6. Final consolidated output is produced

## Installation

### Prerequisites

- Python 3.11 or higher
- OpenAI API key

### Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd agentic-workflow-orchestrator
   ```

2. Install dependencies using uv:
   ```bash
   uv sync
   ```

3. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

### Running the Workflow

Execute the main workflow:
```bash
uv run python agentic_workflow.py
```

### Redirecting Output

Save workflow output to a file:
```bash
uv run python agentic_workflow.py > workflow_output.md 2>&1
```

### Programmatic Usage

Import and use the workflow function:
```python
from agentic_workflow import run_workflow

results = run_workflow("Custom workflow prompt")
```

## Project Structure

```
├── agentic_workflow.py          # Main workflow orchestrator
├── workflow_agents/
│   ├── base_agents.py          # Core agent implementations
│   └── tests/                  # Agent tests
├── Product-Spec-Email-Router.txt # Sample product specification
├── pyproject.toml              # Project dependencies
└── README.md                   # This file
```

## Example Output

The system processes a product specification (Email Router) and generates:

1. **User Stories**: Persona-based requirements
   - "As a Customer Support Representative, I want..."
   - "As a Subject Matter Expert, I want..."
   - "As an IT Administrator, I want..."

2. **Product Features**: Organized capabilities
   - User Authentication
   - Email Classification
   - Routing Logic
   - Dashboard & Analytics

3. **Development Tasks**: Technical implementation details
   - Database schema design
   - API endpoint creation
   - UI component development
   - Testing strategies

## Dependencies

- `openai==1.78.1` - OpenAI API client
- `python-dotenv==1.1.0` - Environment variable management
- `pandas==2.2.3` - Data manipulation (for potential data processing tasks)

## Contributing

This project is part of the Udacity Agentic AI Nanodegree program. Feel free to explore the code and adapt it for your own agentic workflow needs.

## License

This project is for educational purposes as part of the Udacity Agentic AI Nanodegree program.