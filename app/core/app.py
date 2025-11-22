from app.utils.config import config
from app.utils.logger import logger
from app.utils.telegram import telegram
from app.utils.supabase import supabase

class App:
    def __init__(self):
        # Example config loading
        self.stop_loss = config.api_configs.get("app.stop_loss", 2.0)
        self.take_profit = config.api_configs.get("app.take_profit", 5.0)

    def run(self):
        logger.info("📈 Starting App")
        
        # Log lifecycle
        supabase.insert_event("start", {"type": "app"})
        telegram.send_sync("🚀 App Started")

        try:
            self._validate_config()
            
            logger.info(f"App Settings: Stop Loss {self.stop_loss}%, Take Profit {self.take_profit}%")
            logger.info("Initializing App...")
            
            # Mock logic
            logger.info("App Initialized")
            logger.info("Executing app logic (Mock)...")
            
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
        # Example validation using Pydantic config would be better, 
        # but here we check if specific keys exist in the generic dict if needed
        pass
