import re
from agno_builder import generate_agent_code # Assuming agno_builder.py is in the same directory or PYTHONPATH

# Define available tasks that the builder knows about
AVAILABLE_TASKS = {
    "greet": "Greets a user.",
    "echo": "Echoes a given message."
    # Future tasks can be added here
}

def get_valid_agent_name():
    """Prompts user for an agent name and validates it."""
    while True:
        agent_name = input("Enter a name for your new agent (e.g., 'MyDataProcessor', 'WebScraperAgent'): ").strip()
        if not agent_name:
            print("Agent name cannot be empty.")
        elif not re.match(r"^[a-zA-Z0-9_-]+$", agent_name):
            print("Agent name can only contain letters, numbers, underscores, and hyphens.")
        else:
            return agent_name

def get_agent_description():
    """Prompts user for an optional agent description."""
    return input("Enter a brief description for your agent (optional): ").strip()

def select_tasks():
    """Allows user to select tasks from AVAILABLE_TASKS."""
    if not AVAILABLE_TASKS:
        print("No tasks available to select.")
        return []

    print("\\nAvailable tasks:")
    task_options = list(AVAILABLE_TASKS.keys())
    for i, task_name in enumerate(task_options):
        print(f"{i+1}. {task_name} ({AVAILABLE_TASKS[task_name]})")

    selected_tasks = []
    while True:
        choice_str = input(f"Enter the numbers of the tasks you want to include, separated by commas (e.g., '1,2'), or leave blank for none: ").strip()
        if not choice_str:
            break
        try:
            selected_indices = [int(x.strip()) - 1 for x in choice_str.split(',')]
            valid_selection = True
            current_selection = []
            for idx in selected_indices:
                if 0 <= idx < len(task_options):
                    current_selection.append(task_options[idx])
                else:
                    print(f"Invalid selection: {idx+1}. Please choose from available task numbers.")
                    valid_selection = False
                    break
            if valid_selection:
                selected_tasks = list(dict.fromkeys(current_selection)) # Remove duplicates, preserve order
                break
        except ValueError:
            print("Invalid input. Please enter numbers separated by commas.")
    print(f"Selected tasks: {selected_tasks if selected_tasks else 'None'}")
    return selected_tasks

def select_tasks_to_run_on_start(chosen_tasks):
    """Allows user to select which of the chosen tasks should run on start."""
    if not chosen_tasks:
        return []

    print("\\nWhich of the selected tasks should run when the agent starts?")
    for i, task_name in enumerate(chosen_tasks):
        print(f"{i+1}. {task_name}")

    selected_on_start = []
    while True:
        choice_str = input(f"Enter numbers, separated by commas, or leave blank if none should run on start: ").strip()
        if not choice_str:
            break
        try:
            selected_indices = [int(x.strip()) - 1 for x in choice_str.split(',')]
            valid_selection = True
            current_selection_on_start = []
            for idx in selected_indices:
                if 0 <= idx < len(chosen_tasks):
                    current_selection_on_start.append(chosen_tasks[idx])
                else:
                    print(f"Invalid selection: {idx+1}. Please choose from the list of your selected tasks.")
                    valid_selection = False
                    break
            if valid_selection:
                selected_on_start = list(dict.fromkeys(current_selection_on_start)) # Remove duplicates
                break
        except ValueError:
            print("Invalid input. Please enter numbers separated by commas.")
    print(f"Tasks to run on start: {selected_on_start if selected_on_start else 'None'}")
    return selected_on_start

def get_task_specific_configs(chosen_tasks):
    """Gets specific configurations for selected tasks."""
    configs = {}
    if "greet" in chosen_tasks:
        print("\\nThe 'greet' task can have a default name for greetings.")
        default_name = input("Enter a default name (or press Enter for 'World'): ").strip()
        if default_name: # Only add to config if user provided something
            configs["greet"] = {"default_name": default_name}
    # Add more task-specific config prompts here as needed
    return configs

def confirm_generation(agent_spec):
    """Displays the agent spec and asks for confirmation."""
    print("\\n--- Agent Specification Summary ---")
    print(f"Agent Name: {agent_spec['agent_name']}")
    print(f"Description: {agent_spec['description']}")
    print(f"Tasks: {', '.join(agent_spec['tasks']) if agent_spec['tasks'] else 'None'}")
    print(f"Tasks to run on start: {', '.join(agent_spec['tasks_to_run_on_start']) if agent_spec['tasks_to_run_on_start'] else 'None'}")
    if agent_spec['task_specific_configs']:
        print("Task-Specific Configs:")
        for task, cfg in agent_spec['task_specific_configs'].items():
            print(f"  {task}: {cfg}")
    print("---------------------------------")

    while True:
        confirm = input(f"Proceed to generate agent '{agent_spec['agent_name']}'? (yes/no): ").strip().lower()
        if confirm == "yes":
            return True
        elif confirm == "no":
            return False
        else:
            print("Please answer 'yes' or 'no'.")

def main():
    print("Welcome to the Agno Agent Builder CLI!")
    print("Let's create a new agent.")

    agent_name = get_valid_agent_name()
    agent_description = get_agent_description()

    chosen_tasks = select_tasks()

    tasks_to_run_on_start = []
    if chosen_tasks:
        tasks_to_run_on_start = select_tasks_to_run_on_start(chosen_tasks)

    task_specific_configs = {}
    if chosen_tasks:
        task_specific_configs = get_task_specific_configs(chosen_tasks)

    agent_spec = {
        'agent_name': agent_name,
        'description': agent_description,
        'tasks': chosen_tasks,
        'tasks_to_run_on_start': tasks_to_run_on_start,
        'task_specific_configs': task_specific_configs
    }

    if confirm_generation(agent_spec):
        print(f"\\nGenerating agent '{agent_name}'...")
        success = generate_agent_code(agent_spec)
        if success:
            print(f"Agent '{agent_name}' generated successfully!")
            print(f"You can find it in the '{agent_name}' directory.")
            print(f"To run it: cd {agent_name} && python agent.py")
        else:
            print(f"Agent generation for '{agent_name}' failed. Please check the error messages above.")
    else:
        print("Agent generation cancelled by user.")

    print("\\nExiting Agno Agent Builder CLI.")

if __name__ == "__main__":
    main()
