#!/usr/bin/env python3
"""Helper script to update main.py with new app/batch routing."""

import sys
import re


def update_main_py(app_or_batch: str, name: str, class_name: str) -> bool:
    """
    Update app/main.py with new routing code.

    Args:
        app_or_batch: Either "app" or "batch"
        name: The name of the app/batch (e.g., "my-app")
        class_name: The class name (e.g., "MyAppApp")

    Returns:
        True if successful, False otherwise
    """
    main_py_path = "app/main.py"

    try:
        with open(main_py_path, 'r') as f:
            content = f.read()

        if app_or_batch == "app":
            function_name = "run_app"
            param_name = "app_name"
        else:
            function_name = "run_batch"
            param_name = "batch_name"

        # Create the new code block
        # Convert kebab-case to snake_case for module import
        module_name = name.replace("-", "_")
        new_code = f'''    elif {param_name} == "{name}":
        from app.core.{module_name} import {class_name}

        {class_name}().run()
'''

        # Simple line-by-line approach
        lines = content.split('\n')
        new_lines = []
        in_target_function = False
        added = False

        for i, line in enumerate(lines):
            # Check if we're entering the target function
            if line.startswith(f'def {function_name}('):
                in_target_function = True
            # Check if we're leaving the function (next function definition)
            elif in_target_function and line.startswith('def ') and not line.startswith(f'def {function_name}('):
                in_target_function = False

            # If we're in the target function and found the else block
            if in_target_function and line.strip() == 'else:' and not added:
                # Add the new elif before the else
                new_lines.append(new_code.rstrip())
                added = True

            new_lines.append(line)

        if not added:
            print(f"⚠️  Could not find the else block in {function_name}")
            return False

        # Write back
        with open(main_py_path, 'w') as f:
            f.write('\n'.join(new_lines))

        return True

    except Exception as e:
        print(f"❌ Error updating {main_py_path}: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 update_main.py <app|batch> <name> <ClassName>")
        sys.exit(1)

    app_or_batch = sys.argv[1]
    name = sys.argv[2]
    class_name = sys.argv[3]

    if app_or_batch not in ["app", "batch"]:
        print("First argument must be 'app' or 'batch'")
        sys.exit(1)

    if update_main_py(app_or_batch, name, class_name):
        print(f"✅ Successfully updated app/main.py with {name} routing")
        sys.exit(0)
    else:
        print(f"❌ Failed to update app/main.py")
        sys.exit(1)
