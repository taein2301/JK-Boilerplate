from app.utils.app import App
from app.utils.logger import logger

class Test-appApp(App):
    def run(self):
        super().run()
        
        logger.info("test-app App is running!")
        # Add your business logic here
        
