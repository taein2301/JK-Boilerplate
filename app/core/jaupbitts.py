from app.utils.app import App
from app.utils.logger import logger


class JaupbittsApp(App):
    def run(self):
        super().run()

        logger.info("jaupbitts App is running!")
        # Add your business logic here
