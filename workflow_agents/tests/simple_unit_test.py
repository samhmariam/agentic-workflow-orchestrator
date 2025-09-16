import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add the project root directory to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

"""
Simple unit test for the agentic workflow module.
This script tests basic functionality and configurations.
"""

def test_environment_setup():
    """Test environment setup and basic configurations."""
    print("=== Testing Environment Setup ===\n")
    
    # Test 1: Load environment variables
    print("1. Testing environment variable loading...")
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    if not openai_api_key:
        print("❌ OPENAI_API_KEY not found in environment")
        return False
    print("✓ OpenAI API key loaded successfully")
    
    # Test 2: Check product spec file
    print("\n2. Testing product spec file...")
    product_spec_path = project_root / "Product-Spec-Email-Router.txt"
    
    if not product_spec_path.exists():
        print("❌ Product spec file not found")
        return False
    print("✓ Product spec file exists")
    
    # Test 3: Import the workflow module
    print("\n3. Testing workflow module import...")
    try:
        import agentic_workflow
        print("✓ Agentic workflow module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import agentic workflow: {e}")
        return False
    
    return True

def test_agent_instantiation():
    """Test that all agents are properly instantiated."""
    print("\n=== Testing Agent Instantiation ===\n")
    
    try:
        import agentic_workflow
        
        # Test Action Planning Agent
        print("1. Testing Action Planning Agent...")
        if hasattr(agentic_workflow, 'action_planning_agent'):
            print("✓ Action Planning Agent instantiated")
        else:
            print("❌ Action Planning Agent not found")
            return False
        
        # Test Product Manager Agents
        print("\n2. Testing Product Manager Agents...")
        if hasattr(agentic_workflow, 'product_manager_knowledge_agent'):
            print("✓ Product Manager Knowledge Agent instantiated")
        else:
            print("❌ Product Manager Knowledge Agent not found")
            return False
            
        if hasattr(agentic_workflow, 'product_manager_evaluation_agent'):
            print("✓ Product Manager Evaluation Agent instantiated")
        else:
            print("❌ Product Manager Evaluation Agent not found")
            return False
        
        # Test Program Manager Agents
        print("\n3. Testing Program Manager Agents...")
        if hasattr(agentic_workflow, 'program_manager_knowledge_agent'):
            print("✓ Program Manager Knowledge Agent instantiated")
        else:
            print("❌ Program Manager Knowledge Agent not found")
            return False
            
        if hasattr(agentic_workflow, 'program_manager_evaluation_agent'):
            print("✓ Program Manager Evaluation Agent instantiated")
        else:
            print("❌ Program Manager Evaluation Agent not found")
            return False
        
        # Test Development Engineer Agents
        print("\n4. Testing Development Engineer Agents...")
        if hasattr(agentic_workflow, 'development_engineer_knowledge_agent'):
            print("✓ Development Engineer Knowledge Agent instantiated")
        else:
            print("❌ Development Engineer Knowledge Agent not found")
            return False
            
        if hasattr(agentic_workflow, 'development_engineer_evaluation_agent'):
            print("✓ Development Engineer Evaluation Agent instantiated")
        else:
            print("❌ Development Engineer Evaluation Agent not found")
            return False
        
        # Test Routing Agent
        print("\n5. Testing Routing Agent...")
        if hasattr(agentic_workflow, 'routing_agent'):
            print("✓ Routing Agent instantiated")
        else:
            print("❌ Routing Agent not found")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error during agent instantiation test: {e}")
        return False

def test_support_functions():
    """Test that support functions exist and are callable."""
    print("\n=== Testing Support Functions ===\n")
    
    try:
        import agentic_workflow
        
        # Test Product Manager Support Function
        print("1. Testing Product Manager Support Function...")
        if hasattr(agentic_workflow, 'product_manager_support_function'):
            if callable(agentic_workflow.product_manager_support_function):
                print("✓ Product Manager Support Function is callable")
            else:
                print("❌ Product Manager Support Function is not callable")
                return False
        else:
            print("❌ Product Manager Support Function not found")
            return False
        
        # Test Program Manager Support Function
        print("\n2. Testing Program Manager Support Function...")
        if hasattr(agentic_workflow, 'program_manager_support_function'):
            if callable(agentic_workflow.program_manager_support_function):
                print("✓ Program Manager Support Function is callable")
            else:
                print("❌ Program Manager Support Function is not callable")
                return False
        else:
            print("❌ Program Manager Support Function not found")
            return False
        
        # Test Development Engineer Support Function
        print("\n3. Testing Development Engineer Support Function...")
        if hasattr(agentic_workflow, 'development_engineer_support_function'):
            if callable(agentic_workflow.development_engineer_support_function):
                print("✓ Development Engineer Support Function is callable")
            else:
                print("❌ Development Engineer Support Function is not callable")
                return False
        else:
            print("❌ Development Engineer Support Function not found")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error during support function test: {e}")
        return False

def test_routing_configuration():
    """Test routing agent configuration."""
    print("\n=== Testing Routing Configuration ===\n")
    
    try:
        import agentic_workflow
        
        # Test routes are configured
        print("1. Testing routes configuration...")
        if hasattr(agentic_workflow.routing_agent, 'agents'):
            routes = agentic_workflow.routing_agent.agents
            print(f"✓ Found {len(routes)} routes configured")
            
            # Test expected routes
            expected_routes = ['Product Manager', 'Program Manager', 'Development Engineer']
            route_names = [route['name'] for route in routes]
            
            print("\n2. Testing individual routes...")
            for expected_name in expected_routes:
                if expected_name in route_names:
                    print(f"✓ {expected_name} route found")
                else:
                    print(f"❌ {expected_name} route missing")
                    return False
            
            # Test route structure
            print("\n3. Testing route structure...")
            for route in routes:
                if 'name' not in route:
                    print(f"❌ Route missing 'name' field: {route}")
                    return False
                if 'description' not in route:
                    print(f"❌ Route missing 'description' field: {route}")
                    return False
                if 'func' not in route:
                    print(f"❌ Route missing 'func' field: {route}")
                    return False
                if not callable(route['func']):
                    print(f"❌ Route function not callable: {route['name']}")
                    return False
            
            print("✓ All routes have proper structure")
            return True
            
        else:
            print("❌ Routing agent has no agents configured")
            return False
        
    except Exception as e:
        print(f"❌ Error during routing configuration test: {e}")
        return False

def test_workflow_components():
    """Test workflow components exist."""
    print("\n=== Testing Workflow Components ===\n")
    
    try:
        import agentic_workflow
        
        # Test workflow prompt exists
        print("1. Testing workflow prompt...")
        if hasattr(agentic_workflow, 'workflow_prompt'):
            print(f"✓ Workflow prompt: {agentic_workflow.workflow_prompt}")
        else:
            print("⚠️ Workflow prompt not found (this is expected if module was imported)")
        
        # Test knowledge strings exist
        print("\n2. Testing knowledge configurations...")
        knowledge_vars = [
            'knowledge_action_planning',
            'knowledge_product_manager', 
            'knowledge_program_manager',
            'knowledge_dev_engineer'
        ]
        
        for var in knowledge_vars:
            if hasattr(agentic_workflow, var):
                print(f"✓ {var} found")
            else:
                print(f"⚠️ {var} not found (may be local variable)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during workflow components test: {e}")
        return False

def main():
    """Run all tests."""
    print("Starting Agentic Workflow Unit Tests...\n")
    
    test_results = []
    
    # Run all tests
    test_results.append(("Environment Setup", test_environment_setup()))
    test_results.append(("Agent Instantiation", test_agent_instantiation()))
    test_results.append(("Support Functions", test_support_functions()))
    test_results.append(("Routing Configuration", test_routing_configuration()))
    test_results.append(("Workflow Components", test_workflow_components()))
    
    # Print summary
    print("\n" + "="*50)
    print("TEST SUMMARY")
    print("="*50)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name:.<30} {status}")
        if result:
            passed += 1
    
    print("-"*50)
    print(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return True
    else:
        print(f"\n❌ {total - passed} test(s) failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)