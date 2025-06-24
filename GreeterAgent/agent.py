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
        # print(f"Agent '{self.agent_name}' initialized with config: {self.config}") # Debug print

    def _load_config(self):
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Configuration file not found at {self.config_path}")
            return {} # Escaped literal dict
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from {self.config_path}")
            return {} # Escaped literal dict

    def _register_tasks(self):
        registered = {} # Escaped literal dict
        # For now, this will be empty as tasks are directly in the class.
        # This structure is for future expansion (e.g. loading from a tasks module)
        # We'll adapt it if task methods are directly discovered.

        # Example of discovering methods if tasks are defined in the class:
        for task_name_config in self.config.get("tasks", []): # [] is fine
            method_name = f"task_{task_name_config}" # {var}
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
            print(f"Agent '{self.agent_name}' executing task: '{task_name}'") # Escaped
            try:
                return self.tasks_registry[task_name](*args, **kwargs)
            except Exception as e:
                print(f"Error during task '{task_name}' execution: {e}") # Escaped
                return None
        else:
            # Escaped all f-string variables
            print(f"Task '{task_name}' not found or not enabled for agent '{self.agent_name}'. Available: {self.list_available_tasks()}")
            return None

    def run(self):
        print(f"Agent '{self.agent_name}' started.") # Escaped
        tasks_to_run = self.config.get("tasks_to_run_on_start", []) # [] is fine
        if not tasks_to_run:
            print(f"Agent '{self.agent_name}' has no tasks configured to run on start.") # Escaped
        else:
            for task_name in tasks_to_run:
                # Params from task_specific_configs are for the task's internal use,
                # not necessarily direct arguments for run_on_start calls.
                # Tasks should fetch their own config from self.config if needed when called with no args.
                self.run_task(task_name) # Call with no explicit args from here for startup tasks

        print(f"Agent '{self.agent_name}' finished its startup run.") # Escaped


    #
    def task_greet(self, name=None):
        default_name = "World"
        task_configs = self.config.get("task_specific_configs", {{}}).get("greet", {{}})

        name_to_greet = name if name is not None else task_configs.get("default_name", default_name)

        message = f"Hello, {{name_to_greet}}! I am agent '{{self.agent_name}}'."
        print(message)
        return message

    #

# This is the original commented-out main block from the full AGENT_PY_TEMPLATE
# if __name__ == "__main__":
#     # The agent_name will be set by the builder based on user input
#     agent = AgnoAgent(agent_name="{agent_name}") # Escaped for template
#     agent.run()


if __name__ == "__main__":
    # This agent_name is specific to this generated agent
    agent = AgnoAgent(agent_name="GreeterAgent") # GreeterAgent is for this template's .format()
    agent.run()

    # Example of running specific tasks (optional, for testing)
    # if "greet" in agent.list_available_tasks():
    #     agent.run_task("greet")
    # if "echo" in agent.list_available_tasks():
    #     agent.run_task("echo", message="Testing echo from main block.")
