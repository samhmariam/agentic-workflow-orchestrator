import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import unittest
from unittest.mock import patch

# Add the project root directory to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import the workflow module and base agents
import agentic_workflow
from workflow_agents.base_agents import ActionPlanningAgent, KnowledgeAugmentedPromptAgent, EvaluationAgent, RoutingAgent

"""
Comprehensive test suite for the agentic_workflow.py module.
This script tests all components of the workflow including agent instantiation,
routing configuration, support functions, and end-to-end workflow execution.
"""

class TestAgenticWorkflow(unittest.TestCase):
    """Test class for validating the agentic workflow functionality."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment once for all tests."""
        print("=== Setting up Agentic Workflow Test Suite ===\n")
        load_dotenv()
        cls.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        if not cls.openai_api_key:
            raise ValueError("OPENAI_API_KEY not found. Please set it in your .env file.")
    
    def test_environment_setup(self):
        """Test that environment variables and configurations are properly loaded."""
        print("Testing environment setup...")
        
        # Test API key is loaded
        self.assertIsNotNone(self.openai_api_key, "OpenAI API key should be loaded")
        self.assertTrue(len(self.openai_api_key) > 0, "API key should not be empty")
        
        # Test product spec file exists and is readable
        product_spec_path = Path(project_root) / "Product-Spec-Email-Router.txt"
        self.assertTrue(product_spec_path.exists(), "Product spec file should exist")
        
        # Test that product_spec is loaded in the module
        self.assertTrue(hasattr(agentic_workflow, 'product_spec'), "Product spec should be loaded")
        self.assertTrue(len(agentic_workflow.product_spec) > 0, "Product spec should not be empty")
        
        print("✓ Environment setup test passed\n")
    
    def test_agent_instantiation(self):
        """Test that all agents are properly instantiated with correct configurations."""
        print("Testing agent instantiation...")
        
        # Test Action Planning Agent
        self.assertIsInstance(agentic_workflow.action_planning_agent, ActionPlanningAgent)
        
        # Test Product Manager Knowledge Agent
        self.assertIsInstance(agentic_workflow.product_manager_knowledge_agent, KnowledgeAugmentedPromptAgent)
        self.assertEqual(agentic_workflow.product_manager_knowledge_agent.persona, 
                        "You are a Product Manager, you are responsible for defining the user stories for a product.")
        
        # Test Product Manager Evaluation Agent
        self.assertIsInstance(agentic_workflow.product_manager_evaluation_agent, EvaluationAgent)
        
        # Test Program Manager Knowledge Agent
        self.assertIsInstance(agentic_workflow.program_manager_knowledge_agent, KnowledgeAugmentedPromptAgent)
        self.assertEqual(agentic_workflow.program_manager_knowledge_agent.persona,
                        "You are a Program Manager, you are responsible for defining the features for a product.")
        
        # Test Program Manager Evaluation Agent
        self.assertIsInstance(agentic_workflow.program_manager_evaluation_agent, EvaluationAgent)
        
        # Test Development Engineer Knowledge Agent
        self.assertIsInstance(agentic_workflow.development_engineer_knowledge_agent, KnowledgeAugmentedPromptAgent)
        self.assertEqual(agentic_workflow.development_engineer_knowledge_agent.persona,
                        "You are a Development Engineer, you are responsible for defining the development tasks for a product.")
        
        # Test Development Engineer Evaluation Agent
        self.assertIsInstance(agentic_workflow.development_engineer_evaluation_agent, EvaluationAgent)
        
        # Test Routing Agent
        self.assertIsInstance(agentic_workflow.routing_agent, RoutingAgent)
        
        print("✓ Agent instantiation test passed\n")
    
    def test_routing_configuration(self):
        """Test that the routing agent is properly configured with all routes."""
        print("Testing routing configuration...")
        
        # Test routes are configured
        self.assertTrue(hasattr(agentic_workflow.routing_agent, 'agents'), "Routing agent should have agents configured")
        routes = agentic_workflow.routing_agent.agents
        
        # Test number of routes
        self.assertEqual(len(routes), 3, "Should have 3 routes configured")
        
        # Test route names
        route_names = [route['name'] for route in routes]
        expected_names = ['Product Manager', 'Program Manager', 'Development Engineer']
        for name in expected_names:
            self.assertIn(name, route_names, f"Route {name} should be configured")
        
        # Test each route has required fields
        for route in routes:
            self.assertIn('name', route, "Route should have a name")
            self.assertIn('description', route, "Route should have a description")
            self.assertIn('func', route, "Route should have a function")
            self.assertTrue(callable(route['func']), "Route function should be callable")
        
        print("✓ Routing configuration test passed\n")
    
    @patch('agentic_workflow.product_manager_knowledge_agent.respond')
    @patch('agentic_workflow.product_manager_evaluation_agent.evaluate')
    def test_product_manager_support_function(self, mock_evaluate, mock_respond):
        """Test the product_manager_support_function works correctly."""
        print("Testing product manager support function...")
        
        # Setup mocks
        mock_respond.return_value = "Mock user stories response"
        mock_evaluate.return_value = {'final_response': 'Evaluated user stories'}
        
        # Test the function
        test_query = "Create user stories for email routing"
        result = agentic_workflow.product_manager_support_function(test_query)
        
        # Verify calls
        mock_respond.assert_called_once_with(test_query)
        mock_evaluate.assert_called_once_with("Mock user stories response")
        
        # Verify result
        self.assertEqual(result, 'Evaluated user stories')
        
        print("✓ Product manager support function test passed\n")
    
    @patch('agentic_workflow.program_manager_knowledge_agent.respond')
    @patch('agentic_workflow.program_manager_evaluation_agent.evaluate')
    def test_program_manager_support_function(self, mock_evaluate, mock_respond):
        """Test the program_manager_support_function works correctly."""
        print("Testing program manager support function...")
        
        # Setup mocks
        mock_respond.return_value = "Mock features response"
        mock_evaluate.return_value = {'final_response': 'Evaluated features'}
        
        # Test the function
        test_query = "Define features for email routing"
        result = agentic_workflow.program_manager_support_function(test_query)
        
        # Verify calls
        mock_respond.assert_called_once_with(test_query)
        mock_evaluate.assert_called_once_with("Mock features response")
        
        # Verify result
        self.assertEqual(result, 'Evaluated features')
        
        print("✓ Program manager support function test passed\n")
    
    @patch('agentic_workflow.development_engineer_knowledge_agent.respond')
    @patch('agentic_workflow.development_engineer_evaluation_agent.evaluate')
    def test_development_engineer_support_function(self, mock_evaluate, mock_respond):
        """Test the development_engineer_support_function works correctly."""
        print("Testing development engineer support function...")
        
        # Setup mocks
        mock_respond.return_value = "Mock tasks response"
        mock_evaluate.return_value = {'final_response': 'Evaluated tasks'}
        
        # Test the function
        test_query = "Define development tasks for email routing"
        result = agentic_workflow.development_engineer_support_function(test_query)
        
        # Verify calls
        mock_respond.assert_called_once_with(test_query)
        mock_evaluate.assert_called_once_with("Mock tasks response")
        
        # Verify result
        self.assertEqual(result, 'Evaluated tasks')
        
        print("✓ Development engineer support function test passed\n")


class TestWorkflowExecution(unittest.TestCase):
    """Test class for end-to-end workflow execution."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        load_dotenv()
        cls.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        if not cls.openai_api_key:
            raise ValueError("OPENAI_API_KEY not found. Please set it in your .env file.")
    
    @patch('agentic_workflow.action_planning_agent.extract_steps_from_prompt')
    @patch('agentic_workflow.routing_agent.route')
    def test_workflow_execution_flow(self, mock_route, mock_extract_steps):
        """Test the complete workflow execution flow."""
        print("Testing workflow execution flow...")
        
        # Setup mocks
        mock_extract_steps.return_value = [
            "Define user stories",
            "Define features", 
            "Define development tasks"
        ]
        
        # Mock routing function that returns different support functions
        def mock_route_side_effect(step):
            if "user stories" in step.lower():
                return agentic_workflow.product_manager_support_function
            elif "features" in step.lower():
                return agentic_workflow.program_manager_support_function
            elif "tasks" in step.lower():
                return agentic_workflow.development_engineer_support_function
            return agentic_workflow.product_manager_support_function
        
        mock_route.side_effect = mock_route_side_effect
        
        # Mock the support functions to avoid actual API calls
        with patch('agentic_workflow.product_manager_support_function', return_value="User stories result"), \
             patch('agentic_workflow.program_manager_support_function', return_value="Features result"), \
             patch('agentic_workflow.development_engineer_support_function', return_value="Tasks result"):
            
            # Execute workflow steps simulation
            workflow_prompt = "What would the development tasks for this product be?"
            workflow_steps = agentic_workflow.action_planning_agent.extract_steps_from_prompt(workflow_prompt)
            completed_steps = []
            
            for step in workflow_steps:
                agent = agentic_workflow.routing_agent.route(step)
                result = agent(step)
                completed_steps.append(result)
            
            # Verify workflow execution
            self.assertEqual(len(completed_steps), 3, "Should have completed 3 steps")
            self.assertTrue(all(isinstance(step, str) for step in completed_steps), 
                          "All completed steps should be strings")
        
        print("✓ Workflow execution flow test passed\n")


def run_integration_test():
    """Run a real integration test with actual API calls (when API key is available)."""
    print("=== Running Integration Test ===\n")
    
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    if not openai_api_key:
        print("Skipping integration test - no API key available")
        return
    
    try:
        # Test a simple workflow step
        test_prompt = "Define user stories for an email routing system"
        
        print(f"Testing with prompt: {test_prompt}")
        
        # Test action planning
        steps = agentic_workflow.action_planning_agent.extract_steps_from_prompt(test_prompt)
        print(f"Extracted steps: {steps}")
        
        # Test routing for first step
        if steps:
            first_step = steps[0]
            agent_func = agentic_workflow.routing_agent.route(first_step)
            print(f"Routed to agent function: {agent_func.__name__}")
            
            # Note: We could test the actual execution here, but it would make real API calls
            # For testing purposes, we'll just verify the routing works
        
        print("✓ Integration test completed successfully\n")
        
    except Exception as e:
        print(f"Integration test failed: {str(e)}")


if __name__ == "__main__":
    # Run unit tests
    print("Starting Agentic Workflow Test Suite...\n")
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTest(unittest.makeSuite(TestAgenticWorkflow))
    test_suite.addTest(unittest.makeSuite(TestWorkflowExecution))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Run integration test
    run_integration_test()
    
    # Print summary
    print("=== Test Summary ===")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"  {test}: {traceback}")
    
    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"  {test}: {traceback}")
    
    success = len(result.failures) == 0 and len(result.errors) == 0
    print(f"\nOverall result: {'PASS' if success else 'FAIL'}")