import importlib

import typer

from app.utils.config import config
from app.utils.logger import logger


def run_app(
    app_name: str = typer.Argument(..., help="Name of the app to run (e.g., upbit)"),
    env: str = typer.Option(..., help="Environment (dev/prod)"),
):
    """
    Start a long-running application.
    """
    # Update config name to match the running app
    config.name = app_name
    config.env = env

    from app.utils.logger import configure_file_logging

    configure_file_logging(app_name)

    logger.info(f"Starting app: {app_name} in {env} mode")

    try:
        # Convert kebab-case to snake_case for module name
        module_name = app_name.replace("-", "_")
        # Convert kebab-case to CamelCase for class name
        class_name = "".join(word.capitalize() for word in app_name.split("-")) + "App"

        module = importlib.import_module(f"app.core.{module_name}")
        app_class = getattr(module, class_name)
        app_class().run()
    except ImportError:
        logger.error(f"App module 'app.core.{module_name}' not found for {app_name}")
    except AttributeError:
        logger.error(f"App class '{class_name}' not found in 'app.core.{module_name}'")
    except Exception as e:
        logger.error(f"Error running app {app_name}: {e}")

    logger.info(f"App {app_name} finished")


# Entry points for pyproject.toml scripts
def app_entry():
    typer.run(run_app)


if __name__ == "__main__":
    # Default behavior if run directly: show help or run app
    typer.run(run_app)
