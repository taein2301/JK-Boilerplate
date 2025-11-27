from app.utils.config import config
from app.utils.logger import logger
from app.utils.telegram import telegram
from app.utils.supabase import supabase

class App:
    def __init__(self):
        pass

    def run(self):
        logger.info("📈 Starting App")
        
        # Log lifecycle
        supabase.insert_event("start", {"type": "app"})
        telegram.send_sync("🚀 App Started")

        try:
            self._validate_config()
            
            logger.info("Initializing App...")
            
            # Subclasses should implement their logic here
            
            logger.info("🎯 App execution finished")
            
        except Exception as e:
            logger.error(f"App Error: {e}")
            telegram.send_sync(f"🚨 App Failed: {e}")
            supabase.insert_event("abnormal_stop", {"error": str(e)})
            raise
        finally:
            supabase.insert_event("stop", {"type": "app"})
            telegram.send_sync("🏁 App Stopped")

    def _validate_config(self):
        # Override this method to validate config
        pass
