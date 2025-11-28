from app.utils.app import App
from app.utils.logger import logger


class UpbitTraderApp(App):
    def run(self):
        super().run()

        logger.info("upbit-trader App is running!")
        # Add your business logic here
