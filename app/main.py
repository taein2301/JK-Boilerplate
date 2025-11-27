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

    if app_name == "jaupbitts":
        from app.core.jaupbitts import JaupbittsApp

        JaupbittsApp().run()
    elif app_name == "upbit-trader":
        from app.core.upbit_trader import UpbitTraderApp

        UpbitTraderApp().run()
    elif app_name == "upbit-trader":
        from app.core.upbit_trader import UpbitTraderApp

        UpbitTraderApp().run()
    else:
        logger.warning(f"Unknown app: {app_name}")

    logger.info(f"App {app_name} finished")


def run_batch(
    batch_name: str = typer.Argument(
        ..., help="Name of the batch to run (e.g., my-batch)"
    ),
    env: str = typer.Option(..., help="Environment (dev/prod)"),
):
    """
    Run a batch job.
    """
    # Update config name to match the running batch
    config.name = batch_name
    config.env = env

    from app.utils.logger import configure_file_logging

    configure_file_logging(batch_name)

    logger.info(f"Starting batch: {batch_name} in {env} mode")

    if batch_name == "my-batch":
        from app.utils.batch import BatchJob

        batch_instance = BatchJob()
        batch_instance.run()
    else:
        logger.warning(f"Unknown batch: {batch_name}")

    logger.info(f"Batch {batch_name} finished")


# Entry points for pyproject.toml scripts
def app_entry():
    typer.run(run_app)


def batch_entry():
    typer.run(run_batch)


if __name__ == "__main__":
    # Default behavior if run directly: show help or run app
    typer.run(run_app)
