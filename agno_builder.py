import os
import json

# --- Template for agent.py ---
AGENT_PY_TEMPLATE = """\
import json
import os

# Agent Template - Iteration 1 (Restoring _load_config)
class AgnoAgent:
    def __init__(self, agent_name, config_path="config.json"): # Added config_path
        self.agent_name = agent_name
        # Ensure config_path is relative to the agent's own directory
        if not os.path.isabs(config_path):
            self.config_path = os.path.join(os.path.dirname(__file__), config_path)
        else:
            self.config_path = config_path

        self.config = self._load_config()
        self.tasks_registry = self._register_tasks() # Added this line
        # print(f"Agent '{{self.agent_name}}' initialized with config: {{self.config}}") # Debug print

    def _load_config(self):
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Configuration file not found at {{self.config_path}}")
            return {{}} # Escaped literal dict
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from {{self.config_path}}")
            return {{}} # Escaped literal dict

    def _register_tasks(self):
        registered = {{}} # Escaped literal dict
        # For now, this will be empty as tasks are directly in the class.
        # This structure is for future expansion (e.g. loading from a tasks module)
        # We'll adapt it if task methods are directly discovered.

        # Example of discovering methods if tasks are defined in the class:
        for task_name_config in self.config.get("tasks", []): # [] is fine
            method_name = f"task_{{task_name_config}}" # {{var}}
            if hasattr(self, method_name) and callable(getattr(self, method_name)):
                registered[task_name_config] = getattr(self, method_name)
        return registered

    def list_available_tasks(self):
        # In this iteration, tasks_registry might not be populated yet via __init__
        # For now, let's assume it will be.
        # if not hasattr(self, 'tasks_registry'): return [] # Safety
        return list(self.tasks_registry.keys())

    def run_task(self, task_name, *args, **kwargs):
        if task_name in self.tasks_registry:
            print(f"Agent '{{self.agent_name}}' executing task: '{{task_name}}'") # Escaped
            try:
                return self.tasks_registry[task_name](*args, **kwargs)
            except Exception as e:
                print(f"Error during task '{{task_name}}' execution: {{e}}") # Escaped
                import traceback # Added for debugging in generated agent
                traceback.print_exc() # Added for debugging in generated agent
                return None
        else:
            # Escaped all f-string variables
            print(f"Task '{{task_name}}' not found or not enabled for agent '{{self.agent_name}}'. Available: {{self.list_available_tasks()}}")
            return None

    def run(self):
        print(f"Agent '{{self.agent_name}}' started.") # Escaped
        tasks_to_run = self.config.get("tasks_to_run_on_start", []) # [] is fine
        if not tasks_to_run:
            print(f"Agent '{{self.agent_name}}' has no tasks configured to run on start.") # Escaped
        else:
            for task_name in tasks_to_run:
                # Params from task_specific_configs are for the task's internal use,
                # not necessarily direct arguments for run_on_start calls.
                # Tasks should fetch their own config from self.config if needed when called with no args.
                self.run_task(task_name) # Call with no explicit args from here for startup tasks

        print(f"Agent '{{self.agent_name}}' finished its startup run.") # Escaped


    # {greet_task_method}
    # {echo_task_method}

# This is the original commented-out main block from the full AGENT_PY_TEMPLATE
# if __name__ == "__main__":
#     # The agent_name will be set by the builder based on user input
#     agent = AgnoAgent(agent_name="{{agent_name}}") # Escaped for template
#     agent.run()
"""

GREET_TASK_METHOD_TEMPLATE = """
    def task_greet(self, name=None):
        default_name = "World"
        task_configs = self.config.get("task_specific_configs", {{}}).get("greet", {{}})

        name_to_greet = name if name is not None else task_configs.get("default_name", default_name)

        message = f"Hello, {{name_to_greet}}! I am agent '{{self.agent_name}}'."
        print(message)
        return message
"""

ECHO_TASK_METHOD_TEMPLATE = """
    def task_echo(self, message="Default echo message"):
        echo_message = f"Agent '{{self.agent_name}}' echoes: {{message}}" # Escaped f-string vars
        print(echo_message)
        return echo_message
"""

MAIN_EXECUTION_BLOCK_TEMPLATE = """
if __name__ == "__main__":
    # This agent_name is specific to this generated agent
    agent = AgnoAgent(agent_name="{agent_name}") # {agent_name} is for this template's .format()
    agent.run()

    # Example of running specific tasks (optional, for testing)
    # if "greet" in agent.list_available_tasks():
    #     agent.run_task("greet")
    # if "echo" in agent.list_available_tasks():
    #     agent.run_task("echo", message="Testing echo from main block.")
"""

def generate_agent_code(agent_spec):
    agent_name = agent_spec['agent_name']
    base_dir = agent_name

    if os.path.exists(base_dir):
        print(f"Error: Directory '{base_dir}' already exists.")
        return False
    try:
        os.makedirs(base_dir)
        print(f"Created directory: {base_dir}") # Added print

        # --- Generate config.json ---
        config_data = {
            "agent_name": agent_name,
            "version": "0.1.0",
            "description": agent_spec.get("description", ""),
            "tasks": agent_spec.get("tasks", []),
            "tasks_to_run_on_start": agent_spec.get("tasks_to_run_on_start", []),
            "task_specific_configs": agent_spec.get("task_specific_configs", {})
        }
        config_filepath = os.path.join(base_dir, "config.json")
        with open(config_filepath, 'w') as f:
            json.dump(config_data, f, indent=4)
        print(f"Generated {config_filepath}") # Restored print

        # --- Generate agent.py ---
        greet_method_code = ""
        if "greet" in agent_spec.get("tasks", []):
            greet_method_code = GREET_TASK_METHOD_TEMPLATE

        echo_method_code = ""
        if "echo" in agent_spec.get("tasks", []):
            echo_method_code = ECHO_TASK_METHOD_TEMPLATE

        main_block_code = MAIN_EXECUTION_BLOCK_TEMPLATE.format(agent_name=agent_name)

        # This is the key formatting call
        agent_py_content = AGENT_PY_TEMPLATE.format(
            greet_task_method=greet_method_code,
            echo_task_method=echo_method_code
        )
        agent_py_content += "\n" + main_block_code

        agent_py_filepath = os.path.join(base_dir, "agent.py")
        with open(agent_py_filepath, 'w') as f:
            f.write(agent_py_content)
        print(f"Generated {agent_py_filepath}") # Removed (simplified)

        # --- Generate a README.md (optional but good practice) ---
        readme_content = f"# Agent: {agent_name}\\n\\n"
        readme_content += f"{agent_spec.get('description', 'No description provided.')}\\n\\n"
        readme_content += "## To Run This Agent:\\n"
        readme_content += f"```bash\\ncd {agent_name}\\npython agent.py\\n```\\n"
        readme_filepath = os.path.join(base_dir, "README.md")
        with open(readme_filepath, 'w') as f:
            f.write(readme_content)
        print(f"Generated {readme_filepath}")

        print(f"Agent '{agent_name}' generated successfully in '{base_dir}/'") # Added overall success message
        return True
    except Exception as e:
        print(f"An error occurred during agent generation: {e}") # Restored original error message
        # import traceback # Removed traceback import
        # traceback.print_exc() # Removed traceback print
        if os.path.exists(base_dir) and not os.listdir(base_dir): # Basic cleanup
            try:
                os.rmdir(base_dir)
                print(f"Cleaned up empty directory: {base_dir}")
            except OSError as oe:
                print(f"Error removing directory {base_dir}: {oe}")
        elif os.path.exists(base_dir):
             print(f"Partial files might exist in {base_dir}. Manual cleanup may be required.")
        return False

# Example usage (for direct testing of this simplified builder)
if __name__ == "__main__":
    print("Running agno_builder.py for testing code generation logic.") # s/simplified/agno_builder.py/
    sample_spec = {
        'agent_name': "DebugAgent",
        'tasks': ["greet", "echo"]
    }
    generate_agent_code(sample_spec)

    sample_spec_greet_only = {
        'agent_name': "DebugGreetOnly",
        'tasks': ["greet"]
    }
    generate_agent_code(sample_spec_greet_only)

    sample_spec_no_tasks = {
        'agent_name': "DebugNoTasks",
        'tasks': []
    }
    generate_agent_code(sample_spec_no_tasks)
